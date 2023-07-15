import os
import pandas as pd


def addNewStock(stock):
    newStock = pd.DataFrame(stock)
    stockName = newStock['Stock'].values[0]

    historyExcelPath = 'Files\\Total\\xlsx Files\\order_history.xlsx'
    stockExcelPath = f'Files\\Stocks\\xlsx Files\\{stockName}.xlsx'

    historyCsvPath = 'Files\\Total\\csv Files\\order_history.csv'
    stockCsvPath = f'Files\\Stocks\\csv Files\\{stockName}.csv'

    fieldNames = ['Date', 'Type', 'Stock', 'Price', 'Lot', 'Total']

    if not os.path.exists(historyExcelPath):
        df = pd.DataFrame(columns=fieldNames)
        df.to_excel(historyExcelPath, index=False)

    if not os.path.exists(stockExcelPath):
        df = pd.DataFrame(columns=fieldNames)
        df.to_excel(stockExcelPath, index=False)

    if not os.path.exists(historyCsvPath):
        df = pd.DataFrame(columns=fieldNames)
        df.to_csv(historyCsvPath, index=False)

    if not os.path.exists(stockCsvPath):
        df = pd.DataFrame(columns=fieldNames)
        df.to_csv(stockCsvPath, index=False)

    newStock.reset_index(drop=True, inplace=True)

    df_history = pd.read_excel(historyExcelPath)
    df_history.reset_index(drop=True, inplace=True)
    df_history = pd.concat([df_history, newStock])
    df_history.to_excel(historyExcelPath, index=False)
    df_history.to_csv(historyCsvPath, index=False)

    df_stock = pd.read_excel(stockExcelPath)
    df_stock.reset_index(drop=True, inplace=True)
    if len(df_stock) == 0:
        df_stock = pd.concat([df_stock, newStock])
    else:
        df_stock = pd.concat([df_stock[0:-1], newStock])

    df_stock = updateMeanRow(df_stock)
    df_stock.to_excel(stockExcelPath, index=False)
    df_stock.to_csv(stockCsvPath, index=False)


def updateMeanRow(df):
    lot_sum = df['Lot'].sum()
    total_sum = df['Total'].sum()
    average = total_sum / lot_sum
    total_df = pd.DataFrame({'Date': ['-'], 'Type': ['Total'], 'Stock': [df['Stock'].values[0]],
                             'Price': [average], 'Lot': [lot_sum], 'Total': [total_sum]})

    df.reset_index(drop=True, inplace=True)
    total_df.reset_index(drop=True, inplace=True)
    df = pd.concat([df, total_df])

    return df


def getAverage(stock):
    stockCsvPath = f'Files\\Stocks\\csv Files\\{stock}.csv'
    df = pd.read_csv(stockCsvPath)
    return df.iloc[-1]['Price']


def getStocksList():
    historyCsvPath = 'Files\\Total\\csv Files\\order_history.csv'
    df = pd.read_csv(historyCsvPath)
    stocks = []
    for i in df.index:
        stock = df['Stock'][i]
        if stock not in stocks:
            stocks.append(stock)

    return stocks
