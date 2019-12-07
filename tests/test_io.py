"""
Tests I/O disk operations.
"""
from collections import OrderedDict
import requests
from portfolio import portfolio_report


# Note: the portfolio_csv argument found in the tests below
#       is a pytest "fixture". It is defined in conftest.py

# DO NOT edit the provided tests. Make them pass.

def test_read_portfolio(portfolio_csv):
    """
    Given that the read_portfolio is called, assert that
    the data the expected data is returned.
    """
    expected = [
        OrderedDict([
            ('symbol', 'symbol'),
            ('units', 'units'),
            ('cost', 'cost'),
        ]),
        OrderedDict([
            ('symbol', 'APPL'),
            ('units', '100'),
            ('cost', '154.23'),
        ]),
        OrderedDict([
            ('symbol', 'AMZN'),
            ('units', '600'),
            ('cost', '1223.43')
        ])
    ]

    assert portfolio_report.read_portfolio(portfolio_csv) == expected, (
        'Expecting to get the data stored in the portfolio_csv '
        'fixture as a Python data structure.'
    )

def test_save_portfolio(portfolio_csv):
    """
    Given that the save portfolio method is called with the following
    data, assert that a CSV file is written in the expected format.
    The portfolio
    """
    portfolio_report.save_portfolio(portfolio_csv, filename=portfolio_csv)

    expected = """symbol,units,cost,latest_price,book_value,market_value,gain_loss,change\r\n\
APPL,100,154.23,0,15422.999999999998,0.0,-15422.999999999998,-1.0\r\n\
AMZN,600,1223.43,1751.6,734058.0,1050960.0,316902.0,0.4317124804851933\r\n"""
    with open(portfolio_csv, 'r', newline='') as file:
        result = file.read()
        assert result == expected, (
            f'Expecting the file to contain: \n{result}'
        )
