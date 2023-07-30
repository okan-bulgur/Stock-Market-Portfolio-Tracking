import os
import glob

import tabula
from tkinter import *
from yahoo_fin.stock_info import *


historyExcelPath = 'Files\\Total\\xlsx Files\\order_history.xlsx'
allStocksExcelPath = 'Files\\Total\\xlsx Files\\all_stocks.xlsx'

historyCsvPath = 'Files\\Total\\csv Files\\order_history.csv'
allStocksCsvPath = 'Files\\Total\\csv Files\\all_stocks.csv'

fieldNames = ['Date', 'Type', 'Stock', 'Price', 'Lot', 'Total', 'Commission']
fieldNames2 = ['Stock', 'Lot', 'Average', 'Total', 'Price', 'Current Total', 'Profit', 'Change Percentage', 'Commission']


pdfResult = None


def addNewStock(stock):
    newStock = pd.DataFrame(stock)
    stockName = newStock['Stock'].values[0]
    newStock.reset_index(drop=True, inplace=True)

    stockExcelPath = f'Files\\Stocks\\xlsx Files\\{stockName}.xlsx'
    stockCsvPath = f'Files\\Stocks\\csv Files\\{stockName}.csv'

    createFilesIfNotExist(historyCsvPath, historyExcelPath, fieldNames)
    createFilesIfNotExist(stockCsvPath, stockExcelPath, fieldNames)
    createFilesIfNotExist(allStocksCsvPath, allStocksExcelPath, fieldNames2)

    addStock_TotalHistoryFile(historyCsvPath, historyExcelPath, newStock)
    addStock_StockFile(stockCsvPath, stockExcelPath, newStock, historyCsvPath)
    addStock_AllStockFile(allStocksCsvPath, allStocksExcelPath, newStock)


def createFilesIfNotExist(pathCsv, pathExcel, fieldNames):
    if not os.path.exists(pathCsv):
        df = pd.DataFrame(columns=fieldNames)
        df.to_excel(pathExcel, index=False)
        df.to_csv(pathCsv, index=False)


def groupStock(pathCsv):
    df = pd.read_csv(pathCsv)
    gk = df.groupby(['Stock'])
    return gk


def addStock_TotalHistoryFile(pathCsv, pathExcel, newStock):
    df = pd.read_csv(pathCsv)
    df.reset_index(drop=True, inplace=True)
    df = pd.concat([df, newStock])
    df.to_excel(pathExcel, index=False)
    df.to_csv(pathCsv, index=False)


def addStock_StockFile(pathCsv, pathExcel, newStock, historyCsvPath):
    gk = groupStock(historyCsvPath)
    df = gk.get_group((newStock['Stock'].values[0]))
    df.reset_index(drop=True, inplace=True)
    df = updateTotalRow_StockFile(df)
    df.to_excel(pathExcel, index=False)
    df.to_csv(pathCsv, index=False)


def addStock_AllStockFile(pathCsv, pathExcel, newStock):
    df = pd.read_csv(pathCsv)
    df.reset_index(drop=True, inplace=True)
    stockName = newStock['Stock'].values[0]
    stock = getInformationByStock(stockName)

    lot = float(stock['Lot']) + float(newStock['Lot'].values[0])
    total = stock['Principal Invested'] + newStock['Total'].values[0]
    average = round(total / lot, 3)
    price = round(get_live_price(stockName), 3)
    currentTotal = round(price * lot, 3)
    profit = round(currentTotal - total, 3)
    change = f'{round((currentTotal - total) * 100 / total, 3)}%'
    commission = round(stock['Commission'] + newStock['Commission'].values[0], 3)

    updatedStock = {'Stock': [stockName], 'Lot': [lot], 'Average': [average], 'Total': [total], 'Price': [price],
                    'Current Total': [currentTotal], 'Profit': [profit], 'Change Percentage': [change], 'Commission': [commission]}
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


def updateTotalRow_AllStockFile(df):
    total_sum = round(df['Total'].sum(), 3)
    currentTotal_sum = round(df['Current Total'].sum(), 3)
    profit_sum = round(df['Profit'].sum(), 3)
    totalChange = f'{round((currentTotal_sum - total_sum) * 100 / total_sum, 3)}%'
    commission_sum = round(df['Commission'].sum(), 3)

    total_df = pd.DataFrame(
        {
            'Stock': ['-'], 'Lot': ['-'],
            'Average': ['-'], 'Total': [total_sum],
            'Price': ['-'], 'Current Total': [currentTotal_sum],
            'Profit': [profit_sum], 'Change Percentage': [totalChange],
            'Commission': [commission_sum]
        }
    )

    df.reset_index(drop=True, inplace=True)
    total_df.reset_index(drop=True, inplace=True)

    df = pd.concat([df, total_df])

    return df


def updateTotalRow_StockFile(df):
    lot_sum = float(df['Lot'].sum())
    total_sum = float(df['Total'].sum())
    average = round(total_sum / lot_sum, 3)
    commission_sum = round(df['Commission'].sum(), 3)
    total_df = pd.DataFrame({'Date': ['-'], 'Type': ['Total'], 'Stock': [df['Stock'].values[0]],
                             'Price': [average], 'Lot': [lot_sum], 'Total': [total_sum],
                             'Commission': [commission_sum]})

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
    stockCsvPath = f'Files\\Stocks\\csv Files\\{stockName}.csv'
    if not os.path.exists(stockCsvPath):
        return False
    df = pd.read_csv(stockCsvPath)

    return df.iloc[-1]['Lot'] >= lot


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
    info.iloc[:, 0] = info.iloc[:, 0].apply(lambda date: date.replace('/', '-'))
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
