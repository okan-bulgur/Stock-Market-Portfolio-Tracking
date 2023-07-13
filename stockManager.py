import os
import pandas as pd
from csv import DictWriter


def addNewStock(stock):
    fieldNames = ['Date', 'Type', 'Name', 'Price', 'Lot']
    stockName = stock['Name']
    historyPath = 'Files\\Total\\order_history.csv'
    stockPath = f'Files\\Stocks\\{stockName}.csv'

    if not os.path.exists(stockPath):
        df = pd.DataFrame(columns=['Date', 'Type', 'Name', 'Price', 'Lot'])
        df.to_csv(stockPath)
        with open(stockPath, 'w', newline='') as f:
            writer = DictWriter(f, fieldnames=fieldNames)
            writer.writeheader()

    with open(stockPath, 'a', newline='') as f:
        writer = DictWriter(f, fieldnames=fieldNames)
        writer.writerow(stock)

    if not os.path.exists(historyPath):
        df = pd.DataFrame(columns=['Date', 'Type', 'Name', 'Price', 'Lot'])
        df.to_csv(historyPath)
        with open(historyPath, 'w', newline='') as f:
            writer = DictWriter(f, fieldnames=fieldNames)
            writer.writeheader()

    with open(historyPath, 'a', newline='') as f:
        writer = DictWriter(f, fieldnames=fieldNames)
        writer.writerow(stock)
