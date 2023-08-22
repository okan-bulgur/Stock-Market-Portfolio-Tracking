import os
import glob
from datetime import datetime
import pandas as pd
import tabula
from tkinter import *
from yahoo_fin.stock_info import *

historyCsvPath = 'Files\\Total\\csv Files\\order_history.csv'
allStocksCsvPath = 'Files\\Total\\csv Files\\all_stocks.csv'
stocksListCsvPath = 'Files\\Total\\csv Files\\stocks_list.csv'

historyExcelPath = 'Files\\Total\\xlsx Files\\order_history.xlsx'
allStocksExcelPath = 'Files\\Total\\xlsx Files\\all_stocks.xlsx'
stocksListExcelPath = 'Files\\Total\\xlsx Files\\stocks_list.xlsx'

fieldNames_history = ['Date', 'Type', 'Stock', 'Price', 'Lot', 'Total', 'Commission']
fieldNames_allStocks = ['Stock', 'Lot', 'Average', 'Total', 'Price', 'Current Total', 'Profit', 'Change Percentage',
                        'Commission']
fieldNames_stocksList = ['Stock', 'Update Date']

pdfResult = None


def addNewStock(stock):
    newStock = pd.DataFrame(stock)
    newStock.reset_index(drop=True, inplace=True)

    createFilesIfNotExist(historyCsvPath, historyExcelPath, fieldNames_history)
    createFilesIfNotExist(allStocksCsvPath, allStocksExcelPath, fieldNames_allStocks)
    createFilesIfNotExist(stocksListCsvPath, stocksListExcelPath, fieldNames_stocksList)

    addStock_TotalHistoryFile(historyCsvPath, historyExcelPath, newStock)
    #addStock_AllStockFile(allStocksCsvPath, allStocksExcelPath, newStock)
    addStock_StocksListFile(stocksListCsvPath, stocksListExcelPath, newStock)


def createFilesIfNotExist(pathCsv, pathExcel, fieldNames):
    if not os.path.exists(pathCsv):
        df = pd.DataFrame(columns=fieldNames)
        df.to_excel(pathExcel, index=False)
        df.to_csv(pathCsv, index=False)


def addStock_TotalHistoryFile(pathCsv, pathExcel, newStock):
    df = pd.read_csv(pathCsv)
    df.reset_index(drop=True, inplace=True)
    df = pd.concat([df, newStock])
    df.to_excel(pathExcel, index=False)
    df.to_csv(pathCsv, index=False)
    update_AllStockFile(newStock['Stock'].values[0])


'''
def calculateValues(stock, newStock):
    stockName = newStock['Stock'].values[0]
    lot = float(stock['Lot']) + float(newStock['Lot'].values[0])
    total = round(stock['Principal Invested'] + newStock['Total'].values[0], 3)
    price = round(get_live_price(stockName), 3)
    currentTotal = round(price * lot, 3)
    commission = round(stock['Commission'] + newStock['Commission'].values[0], 3)

    if lot == 0:
        average = 0
        profit = total * -1
        change = f'{0}%'
    else:
        average = round(total / lot, 3)
        profit = round(currentTotal - total, 3)
        change = f'{round((currentTotal - total) * 100 / total, 3)}%'

    updatedStock = {'Stock': [stockName], 'Lot': [lot], 'Average': [average], 'Total': [total], 'Price': [price],
                    'Current Total': [currentTotal], 'Profit': [profit], 'Change Percentage': [change],
                    'Commission': [commission]}

    return updatedStock
'''


'''
def addStock_AllStockFile(pathCsv, pathExcel, newStock):
    df = pd.read_csv(pathCsv)
    df.reset_index(drop=True, inplace=True)
    stockName = newStock['Stock'].values[0]
    stock = getInformationByStock(stockName)

    updatedStock = calculateValues(stock, newStock)
    updatedStock_df = pd.DataFrame(updatedStock)

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
            df = pd.concat([df[:-1], updatedStock_df])

    df = updateTotalRow_AllStockFile(df)

    df.to_excel(pathExcel, index=False)
    df.to_csv(pathCsv, index=False)
'''


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

        df.at[i, 'Price'] = round(get_live_price(stock), 3)

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

        price = round(get_live_price(stock), 3)
        currentTotal = round(price * lot, 3)
        profit = round(currentTotal - total, 3)
        changePerc = round((currentTotal - total) * 100 / total, 3)

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
        'Change Percentage': 0,
        'Commission': 0
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
                'Change Percentage': df.iloc[i]['Change Percentage'],
                'Commission': df.iloc[i]['Commission']
            }
            break
    return information


def getPortfolioInf():
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
    inf = getInformationByStock(stockName)
    if inf['Stock'] == 0:
        return False
    return float(inf['Lot']) >= lot


# All Stock File Part

def groupStock(pathCsv, stock):
    df = pd.read_csv(pathCsv)
    gk = df.groupby('Stock')

    for name, group in gk:
        if stock == name:
            return group.reset_index(drop=True)
    return None


def calculateStocksInf(stockName):
    gk = groupStock(historyCsvPath, stockName)
    print(f'gk:\n{gk}')

    stock = gk.loc[0]['Stock']
    lot = gk['Lot'].sum()
    total = gk['Total'].sum()
    average = round(total / lot, 3)
    price = round(get_live_price(stock), 3)
    currentTotal = round(lot * price, 3)
    profit = round(currentTotal - total, 3)
    changePerc = f'{round((currentTotal - total) * 100 / total, 3)}%'
    commission = round(gk['Commission'].sum(), 3)

    if lot == 0:
        average = 0
        profit = total * -1
        changePerc = f'{0}%'

    updatedStock = [stock, lot, average, total, price, currentTotal, profit, changePerc, commission]

    return updatedStock


def updateTotalRow_AllStockFile(df):
    total_sum = round(df[df['Total'] >= 0]['Total'].sum(), 3)
    currentTotal_sum = round(df['Current Total'].sum(), 3)
    profit_sum = round(df['Profit'].sum(), 3)
    if total_sum == 0:
        total_change = 0
    else:
        total_change = f'{round((currentTotal_sum - total_sum) * 100 / total_sum, 3)}%'
    commission_sum = round(df['Commission'].sum(), 3)

    total_df = pd.DataFrame(
        {
            'Stock': ['-'], 'Lot': ['-'],
            'Average': ['-'], 'Total': [total_sum],
            'Price': ['-'], 'Current Total': [currentTotal_sum],
            'Profit': [profit_sum], 'Change Percentage': [total_change],
            'Commission': [commission_sum]
        }
    )

    df.reset_index(drop=True, inplace=True)
    total_df.reset_index(drop=True, inplace=True)
    df = pd.concat([df, total_df])

    return df


def update_AllStockFile(stock):
    if not os.path.exists(allStocksCsvPath):
        return

    df = pd.read_csv(allStocksCsvPath)

    for ind in df.index:
        if df.loc[ind]['Stock'] == '-':
            break
        if df.loc[ind]['Stock'] == stock:
            stock = df.loc[ind]['Stock']
            print("Stock: ", stock)
            df_stock = calculateStocksInf(stock)
            print(f'df_stock:\n{df_stock}')
            df.loc[ind] = df_stock
            print(f'df.loc[ind]:\n{df.loc[ind]}')

    print(f'\n\ndf:\n{df}')
    df = updateTotalRow_AllStockFile(df)
    df.reset_index(drop=True, inplace=True)
    df.to_csv(allStocksCsvPath, index=False)
    df.to_excel(allStocksExcelPath, index=False)


# Stocks Lists Part


def getSplitRatio(stock, date):
    try:
        stock_splits = get_splits(stock)

        split_date = None
        split_ratio = 0

        for split_date, split_event in zip(stock_splits.index, stock_splits['splitRatio']):
            split_ratio = split_event
            split_ratio = split_ratio.split(":")
            numerator = float(split_ratio[0])
            denominator = float(split_ratio[1])
            split_ratio = numerator / denominator
            print(f"Split Date: {split_date}, Numerator: {numerator}, Denominator: {denominator}, Ratio: {split_ratio}")

        date = pd.to_datetime(date, format="%Y-%m-%d")
        split_date = pd.to_datetime(split_date, format="%Y-%m-%d")

        print(f'date: {date}, splitDate: {split_date}')

        if split_date > date:
            print(f"\n\nThere are split.")
            print(f"Split Date: {split_date}, Ratio: {split_ratio}")
            return split_ratio

        return None

    except KeyError:
        return None


def updateStockForSplit(stock, ratio):
    df = pd.read_csv(historyCsvPath)

    for ind in df.index:
        row = df.loc[ind]
        if df.loc[ind]['Stock'] == stock:

            lot = row['Lot'] * ratio
            price = round(row['Price'] / ratio, 3)
            total = row['Lot'] * row['Price']

            df.loc[ind] = [df.loc[ind]['Date'], df.loc[ind]['Type'], df.loc[ind]['Stock'], price, lot, total, df.loc[ind]['Commission']]

    df.to_csv(historyCsvPath, index=False)
    update_AllStockFile(stock)


def updateAllStockForSplit():
    if not os.path.exists(stocksListCsvPath):
        return

    df = pd.read_csv(stocksListCsvPath)

    for ind in df.index:
        row = df.loc[ind]
        if row['Updated Date'] == datetime.date.today():
            continue

        ratio = getSplitRatio(row['Stock'], row['Updated Date'])

        if ratio is not None:
            updateStockForSplit(row['Stock'], ratio)

        row['Updated Date'] = datetime.date.today()

    df.to_csv(stocksListCsvPath)
    df.to_excel(stocksListExcelPath)


def addStock_StocksListFile(pathCsv, pathExcel, newStock):
    df = pd.read_csv(pathCsv)
    df.reset_index(drop=True, inplace=True)

    stockName = newStock['Stock'].values[0]
    index = df[df['Stock'] == stockName].index
    ratio = getSplitRatio(stockName, newStock['Date'].values[0])

    if index.empty:
        print(f"Case 1:\nDate: {newStock['Date'].values[0]}")
        newRow = {'Stock': [stockName], 'Update Date': [datetime.date.today()]}
        newRow = pd.DataFrame(newRow)
        df = pd.concat([df, newRow])

    else:
        print(f"Case 2:\nDate: {df.loc[index]['Update Date'].values[0]}")
        df.loc[index]['Update Date'] = datetime.date.today()

    if ratio is not None:
        updateStockForSplit(stockName, ratio)

    df.to_excel(pathExcel, index=False)
    df.to_csv(pathCsv, index=False)


# PDF Part

def extract_relevant_info(table):
    start_index = 0
    for i in range(len(table.iloc[:, 0])):
        if pd.isnull(table.iloc[i, 0]):
            start_index = i + 1
            break
    temp = table.iloc[start_index:-1:, [0, 3, 5, 6, 7, -1]]
    temp = temp.reset_index(drop=True)
    for i in range(len(temp.iloc[:, 0])):
        if pd.isnull(temp.iloc[i, 0]):
            actual = temp.iloc[i + 1]
            actual.iloc[1] = temp.iloc[i, 1]
            temp.iloc[i + 1] = actual
            temp = temp.drop([i, i + 2])
            break
    return temp


def beautify(info):
    info.iloc[:, 0] = info.iloc[:, 0].apply(lambda date: str(pd.to_datetime(date.replace('/', '-'), format="%d-%m-%Y")).split()[0])
    info.iloc[:, 1] = info.iloc[:, 1].apply(lambda name: str(name.split(" - ")[0]) + ".IS")
    info.iloc[:, 2] = info.iloc[:, 2].apply(lambda name: "Buy" if name == "ALIÞ" else "Sell")
    info.columns = range(info.columns.size)
    return info


def processingPdfInf(path, type):
    global pdfResult

    if type == 'Folder':
        pdfs = glob.glob(f"{path}/*.PDF")
    else:
        pdfs = [path]

    tables = [tabula.read_pdf(pdfs[i], pages=1, encoding='latin-1')[0] for i in range(len(pdfs))]
    infos = [extract_relevant_info(table) for table in tables]
    results = [beautify(info) for info in infos]

    pdfResult = pd.concat(results)
    pdfResult.sort_values(by=0, ascending=True)

    columns = {
        0: 'Date',
        1: 'Stock',
        2: 'Type',
        3: 'Lot',
        4: 'Price',
        5: 'Commission'
    }

    pdfResult.columns = [columns[col] for col in pdfResult.columns]


def showPdfInf(txtArea):
    global pdfResult

    txtArea.config(state='normal')
    txtArea.delete(1.0, END)

    txt = ""
    index = 0
    for i, row in pdfResult.iterrows():
        index += 1
        txt = txt + f"{index}) {row['Date']} \t {row['Type']} \t {row['Stock']} \t " \
                    f"{row['Price']} \t {row['Lot']} \t {row['Commission']} \t \n"

    txtArea.insert('end', txt)
    txtArea.config(state='disable')


def cancelPdfInf(txtArea):
    global pdfResult

    pdfResult = None
    txtArea.config(state='normal')
    txtArea.delete(1.0, END)
    txt = ""
    txtArea.insert('end', txt)
    txtArea.config(state='disable')


def approvePdfInf():
    global pdfResult

    if pdfResult is None:
        return

    for i, row in pdfResult.iterrows():
        price = row['Price']
        price = price.replace(',', '.')
        price = float(price)

        lot = row['Lot']
        lot = lot.replace(',', '.')
        lot = float(lot)

        commission = row['Commission']
        commission = commission.replace(',', '.')
        commission = float(commission)

        if row['Type'] == 'Sell':
            lot = lot * -1

        stock = {'Date': [row['Date']], 'Type': [row['Type']], 'Stock': [row['Stock']],
                 'Price': [price], 'Lot': [lot],
                 'Total': [round(price * lot, 3)],
                 'Commission': [round(commission, 3)]}

        addNewStock(stock)

    pdfResult = None