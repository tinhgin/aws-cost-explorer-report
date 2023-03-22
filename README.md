# AWS Cost Explorer Pretty Report written in Python

## Prerequisites

- Python 3.10 (or later)


## Setup Requirements

```bash
$ pipenv install
```

or

```bash
$ pip3 install -r requirements.txt
```

## Usage

```bash
$ ./aws-cost-explorer-report.py --help

Usage: aws-cost-explorer-report.py [OPTIONS]

Options:
  -S, --start TEXT    start date (default: 1st date of last month)
  -E, --end TEXT      end date (default: 1st date of current month)
  --help              Show this message and exit.
```

## Examples

check cost explorer report of date range [2023-02-01,2022-03-01]

```bash
$ ./aws-cost-explorer-report.py -S 2023-02-01 -E 2022-03-01

Unblended Cost Total: 2738.1164467
Blended Cost Total: 2988.1440213
+--------------+----------------------------------+------------------+------------------+
| Account ID   | Account Name                     | Unblended Cost   | Blended Cost     |
+--------------+----------------------------------+------------------+------------------+
| 011019xxxxxx | Member Account A                 | 1483.8866948146  | 1639.6404397808  |
| 034053xxxxxx | Member Account B                 | 16.842837053     | 18.110494731     |
| 069554xxxxxx | Member Account C                 | 1237.3869148364  | 1330.3930867926  |
+--------------+----------------------------------+------------------+------------------+
```

# License

[MIT LICENSE](LICENSE)
