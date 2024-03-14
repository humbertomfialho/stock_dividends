import pandas as pd
from re import sub
from extract.support import validate_signal, fix_stock_name

def create_stocks_df():
    columns_stocks = [
        'id_negotiation', 'type_negotiation', 'buy_sell', 'market_type', 'stock_name',
        'quantity', 'price', 'total_value', 'credit_debit'
    ]
    dtypes = {
        'id_negotiation': 'int64', 
        'type_negotiation': 'str', 
        'buy_sell': 'str', 
        'market_type': 'str', 
        'stock_name': 'str',
        'quantity': 'int64', 
        'price': 'float64', 
        'total_value': 'float64', 
        'credit_debit': 'str'
    }
    return pd.DataFrame(columns=columns_stocks), dtypes

def extract_stocks_from_pdf(reader_pdf, page_num_pdf):
    negotiation_df, dtypes_df = create_stocks_df()
    stocks_row = 0
    i = 13 if page_num_pdf == 0 else 1

    text = reader_pdf.pages[page_num_pdf].extract_text().split('\n')
    if text[i] == '1-BOVESPA':
        i += 1
    
    while text[i-1] != 'NOTA DE NEGOCIAÇÃO':
        count = 0
        if text[i - 1] == 'Negócios realizados':
            break

        while(text[count+i] != '1-BOVESPA'):
            count += 1
            if text[count+i] == 'NOTA DE NEGOCIAÇÃO' or text[count+i] == 'Negócios realizados':
                break

        stock_name = str()
        if count in [7,8,9,10]:
            negotiation_df.loc[stocks_row, 'type_negotiation'] = text[i-1]
            negotiation_df.loc[stocks_row, 'buy_sell'] = text[i]
            negotiation_df.loc[stocks_row, 'market_type'] = text[i+1]
            
            while not text[i+2].isdigit():
                if ('#' in text[i+2]):
                    i += 1
                    break
                stock_name += text[i+2]
                i += 1

            i += 2
            negotiation_df.loc[stocks_row, 'stock_name'] = fix_stock_name(stock_name)
            negotiation_df.loc[stocks_row, 'quantity'] = text[i]
            negotiation_df.loc[stocks_row, 'price'] = text[i+1].replace(',', '.')
            negotiation_df.loc[stocks_row, 'total_value'] = validate_signal(text, i+2)
            negotiation_df.loc[stocks_row, 'credit_debit'] = text[i+3]
            negotiation_df.loc[stocks_row, 'id_negotiation'] = text[text.index('Nr. nota')+1]
            i += 5
            stocks_row += 1

        elif count == 11:
            negotiation_df.loc[stocks_row, 'type_negotiation'] = text[i]
            negotiation_df.loc[stocks_row, 'buy_sell'] = text[i+1]
            negotiation_df.loc[stocks_row, 'market_type'] = text[i+2]
            
            while not text[i+3].isdigit():
                if '#' in text[i+3]:
                    i += 3
                    break
                stock_name += text[i+3]
                i += 1

            negotiation_df.loc[stocks_row, 'stock_name'] = fix_stock_name(stock_name)
            negotiation_df.loc[stocks_row, 'quantity'] = text[i]
            negotiation_df.loc[stocks_row, 'price'] = text[i+1].replace(',', '.')
            negotiation_df.loc[stocks_row, 'total_value'] = validate_signal(text, i+2)
            negotiation_df.loc[stocks_row, 'credit_debit'] = text[i+3]
            negotiation_df.loc[stocks_row, 'id_negotiation'] = text[text.index('Nr. nota')+1]
            i += 5
            stocks_row += 1

        else: 
            print(f'{count}: count value isnt correct')

    negotiation_df = negotiation_df.astype(dtypes_df)
    return negotiation_df
