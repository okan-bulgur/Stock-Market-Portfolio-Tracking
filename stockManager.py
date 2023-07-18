import os
import pandas as pd
from yahoo_fin.stock_info import *


def addNewStock(stock):
    newStock = pd.DataFrame(stock)
    stockName = newStock['Stock'].values[0]
    newStock.reset_index(drop=True, inplace=True)

    historyExcelPath = 'Files\\Total\\xlsx Files\\order_history.xlsx'
    stockExcelPath = f'Files\\Stocks\\xlsx Files\\{stockName}.xlsx'
    allStocksExcelPath = 'Files\\Total\\xlsx Files\\all_stocks.xlsx'

    historyCsvPath = 'Files\\Total\\csv Files\\order_history.csv'
    stockCsvPath = f'Files\\Stocks\\csv Files\\{stockName}.csv'
    allStocksCsvPath = 'Files\\Total\\csv Files\\all_stocks.csv'

    fieldNames = ['Date', 'Type', 'Stock', 'Price', 'Lot', 'Total']
    fieldNames2 = ['Stock', 'Lot', 'Average', 'Total', 'Price', 'Current Total', 'Profit', 'Change Percentage']

    createFilesIfNotExist(historyCsvPath, historyExcelPath, fieldNames)
    createFilesIfNotExist(stockCsvPath, stockExcelPath, fieldNames)
    createFilesIfNotExist(allStocksCsvPath, allStocksExcelPath, fieldNames2)

    addStock_TotalHistoryFile(historyCsvPath, historyExcelPath, newStock)
    addStock_StockFile(stockCsvPath, stockExcelPath, newStock)
    addStock_AllStockFile(allStocksCsvPath, allStocksExcelPath, stockName)


def createFilesIfNotExist(pathCsv, pathExcel, fieldNames):
    if not os.path.exists(pathCsv):
        df = pd.DataFrame(columns=fieldNames)
        df.to_excel(pathExcel, index=False)
        df.to_csv(pathCsv, index=False)


def addStock_TotalHistoryFile(pathCsv, pathExcel, newStock):
    df = pd.read_excel(pathExcel)
    df.reset_index(drop=True, inplace=True)
    df = pd.concat([df, newStock])
    df.to_excel(pathExcel, index=False)
    df.to_csv(pathCsv, index=False)


def addStock_StockFile(pathCsv, pathExcel, newStock):
    df = pd.read_excel(pathExcel)
    df.reset_index(drop=True, inplace=True)

    if len(df) == 0:
        df_stock = pd.concat([df, newStock])
    else:
        df_stock = pd.concat([df[0:-1], newStock])

    df = updateMeanRow(df_stock)
    df.to_excel(pathExcel, index=False)
    df.to_csv(pathCsv, index=False)


def addStock_AllStockFile(pathCsv, pathExcel, stockName):
    df = pd.read_excel(pathExcel)
    df.reset_index(drop=True, inplace=True)
    newStock = getInformation(stockName)

    lot = newStock['Lot']
    average = round(newStock['Average'], 2)
    total = newStock['Principal Invested']
    price = round(get_live_price(stockName), 2)
    currentTotal = round(price * lot, 2)
    profit = round(currentTotal - total, 2)
    change = f'{round((currentTotal - total) * 100 / total, 2)}%'

    updatedStock = {'Stock': [stockName], 'Lot': [lot], 'Average': [average], 'Total': [total], 'Price': [price],
                    'Current Total': [currentTotal], 'Profit': [profit], 'Change Percentage': [change]}
    updatedStock_df = pd.DataFrame(updatedStock)

    check = False
    for i in df.index:
        stock = df['Stock'][i]
        if stock == stockName:
            df.iloc[i] = updatedStock_df
            check = True

    if not check:
        if len(df) == 0:
            df = pd.concat([df, updatedStock_df])
        else:
            df = pd.concat([df[0:-1], updatedStock_df])

    #df_style = df.style.applymap(paintRow, subset=['Change Percentage'])

    df = updateTotalRow(df)

    df.to_excel(pathExcel, index=False)
    df.to_csv(pathCsv, index=False)


def updateTotalRow(df):
    total_sum = df['Total'].sum()
    currentTotal_sum = df['Current Total'].sum()
    profit_sum = df['Profit'].sum()
    totalChange = f'{round((currentTotal_sum - total_sum) * 100 / total_sum, 2)}%'

    total_df = pd.DataFrame({'Stock': ['-'], 'Lot': ['-'],
                             'Average': ['-'], 'Total': [total_sum],
                             'Price': ['-'], 'Current Total': [currentTotal_sum],
                             'Profit': [profit_sum], 'Change Percentage': [totalChange]})

    df.reset_index(drop=True, inplace=True)
    total_df.reset_index(drop=True, inplace=True)
    df = pd.concat([df, total_df])

    return df


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


def getInformation(stock):
    stockCsvPath = f'Files\\Stocks\\csv Files\\{stock}.csv'
    if not os.path.exists(stockCsvPath):
        return
    df = pd.read_csv(stockCsvPath)
    information = {
        'Stock': df.iloc[-1]['Stock'],
        'Average': df.iloc[-1]['Price'],
        'Lot': df.iloc[-1]['Lot'],
        'Principal Invested': df.iloc[-1]['Total']
    }
    return information


def getStocksList():
    historyCsvPath = 'Files\\Total\\csv Files\\order_history.csv'
    stocks = []

    if os.path.exists(historyCsvPath):
        df = pd.read_csv(historyCsvPath)
        for i in df.index:
            stock = df['Stock'][i]
            if stock not in stocks:
                stocks.append(stock)

    return stocks


"""
def paintRow(val):
    val = float(val.strip('%'))
    color = 'paleturquoise2'
    if val < 0:
        color = 'lightcoral'
    elif val > 0:
        color = 'palegreen'
    return f'background-color: {color}'
"""