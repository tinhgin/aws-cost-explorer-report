#!/usr/bin/env python3

import boto3
import click

from calendar import monthrange
import datetime
from dateutil.relativedelta import relativedelta
from prettytable import PrettyTable

# define table layout
pt = PrettyTable()

pt.field_names = [
    'Account ID',
    'Account Name',
    'Unblended Cost',
    'Blended Cost',
]

pt.align = "l"
pt.align["Amount"] = "r"


def get_cost_and_usage(ce_client: object, start: str, end: str) -> list:
    cu = []

    while True:
        data = ce_client.get_cost_and_usage(
            TimePeriod={
                'Start': start,
                'End':  end,
            },
            Granularity='MONTHLY',
            Metrics=[
                'UnblendedCost',
                'BlendedCost'
            ],
            GroupBy=[
                {
                    'Type': 'DIMENSION',
                    'Key': 'LINKED_ACCOUNT',
                }
            ],
        )

        cu += data['ResultsByTime']
        token = data.get('NextPageToken')

        if not token:
            break

    return cu


def fill_table_content(results: list, org_client: object) -> None:
    unblended_cost_total = 0
    blended_cost_total = 0
    for result_by_time in results:
        for group in result_by_time['Groups']:
            unblended_cost = float(group['Metrics']['UnblendedCost']['Amount'])
            blended_cost = float(group['Metrics']['BlendedCost']['Amount'])

            unblended_cost_total += unblended_cost
            blended_cost_total += blended_cost

            account_id = group['Keys'][0]

            account_name = org_client.describe_account(AccountId=account_id)['Account']['Name']

            pt.add_row([
                account_id,
                account_name,
                unblended_cost,
                blended_cost,
            ])
    print("Unblended Cost Total: {}".format(unblended_cost_total))
    print("Blended Cost Total: {}".format(blended_cost_total))


@click.command()
@click.option('-S', '--start', help='start date (default: 1st date of current month)')
@click.option('-E', '--end', help='end date (default: last date of current month)')
def report(start: str, end: str) -> None:
    # set start/end to last month if not specify
    if not start or not end:
        start = (datetime.date.today() - relativedelta(months=+1)).replace(day=1).strftime('%Y-%m-%d')  # 1st day of month a month ago
        end = datetime.date.today().replace(day=1).strftime('%Y-%m-%d')

    # cost explorer
    ce_client = boto3.client('ce')

    # organizations
    org_client = boto3.client('organizations')

    results = get_cost_and_usage(ce_client, start, end)
    fill_table_content(results, org_client)

    print(pt)


if __name__ == '__main__':
    report()
