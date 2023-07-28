import os

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
    addStock_AllStockFile(allStocksCsvPath, allStocksExcelPath, newStock)


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
        df_stock = pd.concat([df[:-1], newStock])

    df = updateMeanRow(df_stock)
    df.to_excel(pathExcel, index=False)
    df.to_csv(pathCsv, index=False)


def addStock_AllStockFile(pathCsv, pathExcel, newStock):
    df = pd.read_excel(pathExcel)
    df.reset_index(drop=True, inplace=True)
    stockName = newStock['Stock'].values[0]
    stock = getInformationByStock(stockName)

    lot = float(stock['Lot']) + float(newStock['Lot'].values[0])
    total = stock['Principal Invested'] + newStock['Total'].values[0]
    average = round(total / lot, 2)
    price = round(get_live_price(stockName), 2)
    currentTotal = round(price * lot, 2)
    profit = round(currentTotal - total, 2)
    change = f'{round((currentTotal - total) * 100 / total, 2)}%'

    print(
        f"Lot: {lot} total: {total} average: {average} price: {price} currentTotal: {currentTotal} profit: {profit} change: {change}")

    updatedStock = {'Stock': [stockName], 'Lot': [lot], 'Average': [average], 'Total': [total], 'Price': [price],
                    'Current Total': [currentTotal], 'Profit': [profit], 'Change Percentage': [change]}
    updatedStock_df = pd.DataFrame(updatedStock)
    print(updatedStock_df)

    check = False
    for i in df.index:
        stock = df.loc[i, 'Stock']
        if stock == stockName:
            df.loc[i] = updatedStock_df.loc[0]
            df = df.drop(df.index[-1])
            check = True
            break

    if not check:
        if len(df) == 0:
            df = pd.concat([df, updatedStock_df])
        else:
            print("df[:-1] ", df[:-1])
            print("total_df ", updatedStock_df)
            df = pd.concat([df[:-1], updatedStock_df])
            print("df ", df)
            print("df[:-1] ", df[:-1])

    df = updateTotalRow(df)

    print("df3: ", df)

    df.to_excel(pathExcel, index=False)
    df.to_csv(pathCsv, index=False)


def updateTotalRow(df):

    total_sum = round(df['Total'].sum(), 2)
    currentTotal_sum = round(df['Current Total'].sum(), 2)
    profit_sum = round(df['Profit'].sum(), 2)
    totalChange = f'{round((currentTotal_sum - total_sum) * 100 / total_sum, 2)}%'

    total_df = pd.DataFrame(
        {
            'Stock': ['-'], 'Lot': ['-'],
            'Average': ['-'], 'Total': [total_sum],
            'Price': ['-'], 'Current Total': [currentTotal_sum],
            'Profit': [profit_sum], 'Change Percentage': [totalChange]
        }
    )

    df.reset_index(drop=True, inplace=True)
    total_df.reset_index(drop=True, inplace=True)

    print("df1: ", df)

    df = pd.concat([df, total_df])

    print("df2: ", df)

    return df


def updateMeanRow(df):
    lot_sum = df['Lot'].sum()
    total_sum = df['Total'].sum()
    average = round(total_sum / lot_sum, 2)
    total_df = pd.DataFrame({'Date': ['-'], 'Type': ['Total'], 'Stock': [df['Stock'].values[0]],
                             'Price': [average], 'Lot': [lot_sum], 'Total': [total_sum]})

    df.reset_index(drop=True, inplace=True)
    total_df.reset_index(drop=True, inplace=True)
    df = pd.concat([df, total_df])

    return df


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


def updateCurrentPrices(csvPath, excelPath):
    df = pd.read_csv(csvPath)
    for i in df.index:
        stock = df.iloc[i]['Stock']
        if stock == '-':
            break

        df.at[i, 'Price'] = round(get_live_price(stock), 2)

    df.to_excel(excelPath, index=False)
    df.to_csv(csvPath, index=False)


def updateInformations():
    stockCsvPath = 'Files\\Total\\csv Files\\all_stocks.csv'
    stockExcelPath = 'Files\\Total\\xlsx Files\\all_stocks.xlsx'
    if not os.path.exists(stockCsvPath):
        return

    updateCurrentPrices(stockCsvPath, stockExcelPath)

    df = pd.read_csv(stockCsvPath)
    for i in df.index:
        stock = df.iloc[i]['Stock']
        if stock == '-':
            break
        lot = float(df.iloc[i]['Lot'])
        total = df.iloc[i]['Total']

        price = round(get_live_price(stock), 2)
        currentTotal = round(price * lot, 2)
        profit = round(currentTotal - total, 2)
        changePerc = round((currentTotal - total) * 100 / total, 2)

        df.at[i, 'Price'] = price
        df.at[i, 'Current Total'] = currentTotal
        df.at[i, 'Profit'] = profit
        df.at[i, 'Change Percentage'] = f'{changePerc}%'

    df.to_excel(stockExcelPath, index=False)
    df.to_csv(stockCsvPath, index=False)


def getInformationByStock(stock):
    information = {
        'Stock': 0,
        'Lot': 0,
        'Average': 0,
        'Principal Invested': 0,
        'Current Total': 0,
        'Profit': 0,
        'Change Percentage': 0
    }

    updateInformations()
    stockCsvPath = f'Files\\Total\\csv Files\\all_stocks.csv'

    if not os.path.exists(stockCsvPath):
        return information

    df = pd.read_csv(stockCsvPath)

    for i in df.index:
        if df.iloc[i]['Stock'] == stock:
            information = {
                'Stock': df.iloc[i]['Stock'],
                'Lot': df.iloc[i]['Lot'],
                'Average': df.iloc[i]['Average'],
                'Principal Invested': df.iloc[i]['Total'],
                'Current Total': df.iloc[i]['Current Total'],
                'Profit': df.iloc[i]['Profit'],
                'Change Percentage': df.iloc[i]['Change Percentage']
            }
            break
    return information


def getInformation():
    information = {
        'Principal Invested': 0,
        'Current Total': 0,
        'Profit': 0,
        'Change Percentage': 0
    }

    updateInformations()

    stockCsvPath = f'Files\\Total\\csv Files\\all_stocks.csv'

    if not os.path.exists(stockCsvPath):
        return information

    df = pd.read_csv(stockCsvPath)
    information = {
        'Principal Invested': df.iloc[-1]['Total'],
        'Current Total': df.iloc[-1]['Current Total'],
        'Profit': df.iloc[-1]['Profit'],
        'Change Percentage': df.iloc[-1]['Change Percentage']
    }
    return information


def checkValidLotAmount(stockName, lot):
    stockCsvPath = f'Files\\Stocks\\csv Files\\{stockName}.csv'
    if not os.path.exists(stockCsvPath):
        return False
    df = pd.read_csv(stockCsvPath)

    return df.iloc[-1]['Lot'] >= lot
