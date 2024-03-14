import pandas as pd
from datetime import datetime
from extract.support import validate_signal

def create_financial_df():
    columns_financial = [
        'id', 'date', 'sell', 'buy', 'total_value', 'operation_net_value',
        'settlement_tax', 'total_cblc', 'emolumentos', 'total_bovespa',
        'operational_rate', 'taxes', 'irrf', 'others',
        'total_costs', 'net_value'
    ]
    dtypes = {
        'id': 'int64',
        'date': 'datetime64',
        'sell': 'float64', 
        'buy': 'float64', 
        'total_value': 'float64', 
        'operation_net_value': 'float64',
        'settlement_tax': 'float64', 
        'total_cblc': 'float64', 
        'emolumentos': 'float64', 
        'total_bovespa': 'float64',
        'operational_rate': 'float64', 
        'taxes': 'float64', 
        'irrf': 'float64', 
        'others': 'float64',
        'total_costs': 'float64', 
        'net_value': 'float64'
    }
    return pd.DataFrame(columns=columns_financial), dtypes

def extract_financial_from_pdf(reader_pdf):
    financial_row = 0
    financial_df, dtypes_df = create_financial_df()
    text = reader_pdf.pages[-1].extract_text().split('\n')

    i = text.index('Nr. nota')
    financial_df.loc[financial_row, 'id'] = text[i+1]
    financial_df.loc[financial_row, 'date'] = datetime.strptime(text[i+5], '%d/%m/%Y').strftime('%Y-%m-%d')

    i = text.index('Assessor') + 9
    financial_df.loc[financial_row, 'sell'] = validate_signal(text, i)
    financial_df.loc[financial_row, 'buy'] = validate_signal(text,i+1)
    financial_df.loc[financial_row, 'total_value'] = validate_signal(text,i+6)

    i = text.index('Total CBLC')
    financial_df.loc[financial_row, 'total_cblc'] = validate_signal(text, i-1)
    financial_df.loc[financial_row, 'operation_net_value'] = validate_signal(text, i+2)
    financial_df.loc[financial_row, 'settlement_tax'] = validate_signal(text, i+5)
    
    i = text.index('Total Bovespa / Soma')
    financial_df.loc[financial_row, 'total_bovespa'] = validate_signal(text, i-1)
    financial_df.loc[financial_row, 'emolumentos'] = validate_signal(text, i+8)

    i = text.index('Total Custos / Despesas')
    financial_df.loc[financial_row, 'total_costs'] = validate_signal(text, i-1)
    financial_df.loc[financial_row, 'operational_rate'] = validate_signal(text, i+3)

    i = text.index('Impostos')
    financial_df.loc[financial_row, 'taxes'] = validate_signal(text, i-1)
    i = i+2  if text[i + 1] == 'D' else i+1
    financial_df.loc[financial_row, 'irrf'] = validate_signal(text, i)
    financial_df.loc[financial_row, 'others'] = validate_signal(text, i+2)
    financial_df.loc[financial_row, 'net_value'] = validate_signal(text, i+5)

    financial_df = financial_df.astype(dtypes_df)
    return financial_df
