# def csv_to_xlsx_pd():
#     csv = pd.read_csv(r'D:\Data\淄博.csv', encoding='utf-8')
#     csv.to_excel(r'D:\Data\淄博.xlsx', sheet_name='data', index=False)


import os
import pandas as pd

file_list = []
data_dir = r'D:\Data'


def csv_to_xlsx_pd(filename):
    csv = pd.read_csv(filename, encoding='utf-8')
    csv.to_excel(filename[:-3] + 'xlsx', sheet_name='data', index=False)


def run():
    for filename in os.listdir(r'd:\Data'):
        if filename.endswith('csv'):
            filename = os.path.join(data_dir, filename)
            csv_to_xlsx_pd(filename)


if __name__ == '__main__':
    run()
