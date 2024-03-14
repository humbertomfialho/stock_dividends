import pandas as pd
import os
from PyPDF2 import PdfReader
from extract.stocks import extract_stocks_from_pdf
from extract.financial import extract_financial_from_pdf
from data.insert import insert_values

def read_pdf_negotiation(pdf_path):
    operation = pd.DataFrame()
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)
        financial = extract_financial_from_pdf(reader)
        for page_num in range(len(reader.pages)):
            operation = pd.concat([operation, extract_stocks_from_pdf(reader, page_num)], ignore_index=True)
        insert_values(operation, 'Operation')
        insert_values(financial, 'Negotiation')
    return

def pdf_files():
    this_folder = os.getcwd()
    negotiation_pdf = os.listdir(this_folder + '/pdf')
    negotiation_pdf.sort()
    for i in negotiation_pdf:
        read_pdf_negotiation(this_folder + '/pdf/' + i)
    return

if __name__ == "__main__":
    pdf_files()
