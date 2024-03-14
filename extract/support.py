from re import sub

def validate_signal(text_signal, position):
    number = text_signal[position].replace('.', '').replace(',', '.')
    if text_signal[position] == '0,00':
        return number
    if text_signal[position + 2] == 'D' or text_signal[position + 1] == 'D':
        return '-' + number
    return number

def fix_stock_name(text):
    remove_list = ['EX', 'EJ', 'EDJ', 'ED']
    for item in remove_list:
        text = text.replace(item, '')
    text = sub(r' +', ' ', text)
    return text
