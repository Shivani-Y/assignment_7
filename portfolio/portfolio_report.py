"""
Generates performance reports for your stock portfolio.
"""
import csv
import requests


def read_portfolio(input_filename):
    """Returns data from a CSV file"""
    #Read the CSV file with the filename above,
    #       and return the data. Use a DictReader.
    list_row = []
    with open(input_filename, newline='') as file:
        csv_reader = csv.DictReader(file, ['symbol', 'units', 'cost'])
        for row in csv_reader:
            list_row.append(row)
    return list_row

def read_sym(input_filename):
    """Returns data from a CSV file"""
    sym_list = []
    with open(input_filename, newline='') as file:
        csv_reader = csv.DictReader(file, ['symbol', 'units', 'cost'])
        for row in csv_reader:
            sym_list.append(row['symbol'])
    return sym_list

def read_cost(input_filename):
    """Returns data from a CSV file"""
    cost_list = []
    with open(input_filename, newline='') as file:
        csv_reader = csv.DictReader(file, ['symbol', 'units', 'cost'])
        for row in csv_reader:
            cost_list.append(row['cost'])
    return cost_list

def read_units(input_filename):
    """Returns data from a CSV file"""
    unit_list = []
    with open(input_filename, newline='') as file:
        csv_reader = csv.DictReader(file, ['symbol', 'units', 'cost'])
        for row in csv_reader:
            unit_list.append(row['units'])
    return unit_list

def go_to_website(input_filename):
    """goes to website and fetches the latest price of the stock"""
    latest_price_list = ['latest_price']
    symbols = read_sym(input_filename)
    symbols = symbols[1:]
    for sym in symbols:
        token = "pk_3ddbd7ea185c4fffb7c2f21e7cae4118"
        url = 'https://cloud.iexapis.com/stable/stock/'+sym+'/quote?token='+token+''
        response = requests.get(url)
        if response.status_code < 400:
            response = response.json()
            response = response['latestPrice']
            latest_price_list.append(response)
        else:
            latest_price_list.append(0)
            continue
    return latest_price_list

def get_not_found_list(input_filename):
    """goes to website and checks if a ticker exsist or not and add to a list"""
    symbols = read_sym(input_filename)
    symbols = symbols[1:]
    not_found = []
    token = "pk_3ddbd7ea185c4fffb7c2f21e7cae4118"
    for sym in symbols:
        url = 'https://cloud.iexapis.com/stable/stock/'+sym+'/quote?token='+token+''
        response = requests.get(url)
        if response.status_code > 400:
            not_found.append(sym)
    for n_f in not_found:
        print(f'This symbol was not found on the webiste: {n_f}')

def merge(lists):
    """merge lists"""
    return [list(ele) for ele in list(zip(*lists))]

def remove_brakets_from_list(lists):
    """removes the brakets in list"""
    return str(lists).replace('[', '').replace(']', '')

def remove_quotes_from_list(lists):
    """removes quotes from list"""
    return str(lists).replace('\'', '').replace('\'', '')

def remove_space_from_list(lists):
    """removes space from list"""
    return str(lists).replace(' ', '').replace(' ', '')

def get_book_value(input_filename):
    """calculate book_value"""
    get_units_list = read_units(input_filename)
    new_unit_list = get_units_list[1:]
    int_unit_list = map(float, new_unit_list)
    get_cost_list = read_cost(input_filename)
    new_cost_list = get_cost_list[1:]
    int_cost_list = map(float, new_cost_list)
    get_list = [c*u for c, u in zip(int_cost_list, int_unit_list)]
    get_list.insert(0, "book_value")
    return get_list

def get_market_value(input_filename):
    """calculate market_value"""
    get_units_list = read_units(input_filename)
    new_unit_list = get_units_list[1:]
    int_unit_list = map(float, new_unit_list)
    get_latest_price_list = go_to_website(input_filename)
    new_latest_price_list = get_latest_price_list[1:]
    int_latest_price_list = map(float, new_latest_price_list)
    get_list_mv = [u*l for u, l in zip(int_unit_list, int_latest_price_list)]
    get_list_mv.insert(0, "market_value")
    return get_list_mv

def get_gain_loss(input_filename):
    """calculate market_value"""
    get_market_value_list = get_market_value(input_filename)
    new_market_value_list = get_market_value_list[1:]
    int_market_value_list = map(float, new_market_value_list)
    get_book_value_list = get_book_value(input_filename)
    new_book_value_list = get_book_value_list[1:]
    int_book_value_list = map(float, new_book_value_list)
    get_list_gl = [m-b for m, b in zip(int_market_value_list, int_book_value_list)]
    get_list_gl.insert(0, "gain_loss")
    return get_list_gl

def get_gain_loss_percent(input_filename):
    """calculate market_value"""
    gain_loss_list = get_gain_loss(input_filename)
    int_gain_loss_list = gain_loss_list[1:]
    get_book_value_list = get_book_value(input_filename)
    new_book_value_list = get_book_value_list[1:]
    int_book_value_list = map(float, new_book_value_list)
    get_list_gl_percent = []
    for g_l, b_v in zip(int_gain_loss_list, int_book_value_list):
        if g_l == 0 or b_v == 0:
            get_list_gl_percent.append(0)
        else:
            get_list_gl_percent.append(g_l/b_v)
    get_list_gl_percent.insert(0, "change")
    return get_list_gl_percent

def get_data(input_filename):
    """collate data"""
    symbols_list = read_sym(input_filename)
    units_list = read_units(input_filename)
    cost_list = read_cost(input_filename)
    latest_price_list = go_to_website(input_filename)
    book_value_list = get_book_value(input_filename)
    market_value_list = get_market_value(input_filename)
    gain_loss_list = get_gain_loss(input_filename)
    change_list = get_gain_loss_percent(input_filename)
    data_list = [symbols_list, units_list, cost_list, latest_price_list, \
    book_value_list, market_value_list, gain_loss_list, change_list]
    data_write = merge(data_list)
    return data_write

def save_portfolio(input_filename, filename):
    """Saves data to a CSV file"""
    #Save the provided data to the provided filename. Use
    #       a DictWriter
    data = get_data(input_filename)
    with open(filename, 'w', newline='') as file:
        fieldnames = ['sno']
        csv_writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter='\t')
        for ele in data:
            csv_writer.writerow({'sno' : \
            remove_quotes_from_list(remove_space_from_list(remove_brakets_from_list(ele)))})
    get_not_found_list(filename)

def main():
    """
    Entrypoint into program.
    """
    print('getting your data..')
    input_filename = input('Please enter the input file path:')
    output_filename = input('Please enter the output file path:')
    print('getting your data..')
    save_portfolio(input_filename, output_filename)


if __name__ == '__main__':
    main()
