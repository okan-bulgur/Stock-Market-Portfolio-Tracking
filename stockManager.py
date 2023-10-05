import os
import glob
from datetime import datetime
import pandas as pd
import tabula
from tkinter import *
from yahoo_fin.stock_info import *

historyCsvPath = 'Files\\csv Files\\order_history.csv'
allStocksCsvPath = 'Files\\csv Files\\all_stocks.csv'

historyExcelPath = 'Files\\xlsx Files\\order_history.xlsx'
allStocksExcelPath = 'Files\\xlsx Files\\all_stocks.xlsx'

fieldNames_history = ['Date', 'Type', 'Stock', 'Price', 'Lot', 'Total', 'Commission', 'Update Date']
fieldNames_allStocks = ['Stock', 'Lot', 'Average', 'Total', 'Price', 'Current Total', 'Profit', 'Change Percentage',
                        'Commission']

pdfResult = None


def addNewStock(stock):
    newStock = pd.DataFrame(stock)
    newStock.reset_index(drop=True, inplace=True)

    createFilesIfNotExist(historyCsvPath, historyExcelPath, fieldNames_history)
    createFilesIfNotExist(allStocksCsvPath, allStocksExcelPath, fieldNames_allStocks)

    addStock_TotalHistoryFile(historyCsvPath, historyExcelPath, newStock)


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


def getStocksList():
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
    if not os.path.exists(allStocksCsvPath):
        return

    updateCurrentPrices(allStocksCsvPath, allStocksExcelPath)

    df = pd.read_csv(allStocksCsvPath)
    for i in df.index:
        stock = df.iloc[i]['Stock']
        if stock == '-':
            break
        lot = float(df.iloc[i]['Lot'])
        total = df.iloc[i]['Total']

        price = float(df.iloc[i]['Price'])
        currentTotal = round(price * lot, 3)
        profit = round(currentTotal - total, 3)
        changePerc = round((currentTotal - total) * 100 / total, 3)

        df.at[i, 'Price'] = price
        df.at[i, 'Current Total'] = currentTotal
        df.at[i, 'Profit'] = profit
        df.at[i, 'Change Percentage'] = f'{changePerc}%'

    df.to_excel(allStocksExcelPath, index=False)
    df.to_csv(allStocksCsvPath, index=False)


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

    if not os.path.exists(allStocksCsvPath):
        return information

    df = pd.read_csv(allStocksCsvPath)

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

    if not os.path.exists(allStocksCsvPath):
        return information

    df = pd.read_csv(allStocksCsvPath)
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

    stock = gk.loc[0]['Stock']
    lot = gk['Lot'].sum()
    total = gk['Total'].sum()
    price = round(get_live_price(stock), 3)
    currentTotal = round(lot * price, 3)
    profit = round(currentTotal - total, 3)
    commission = round(gk['Commission'].sum(), 3)

    if total == 0:
        changePerc = '-'
    else:
        changePerc = f'{round((currentTotal - total) * 100 / total, 3)}%'

    if lot == 0:
        average = 0
        profit = total * -1
        changePerc = f'{0}%'
    else:
        average = round(total / lot, 3)

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
    ind = None
    check = False

    for ind in df.index:
        if df.loc[ind]['Stock'] == '-':
            break
        if df.loc[ind]['Stock'] == stock:
            df_stock = calculateStocksInf(stock)
            df.loc[ind] = df_stock
            df = df[:-1]
            check = True
            break

    if not check:
        df_stock = calculateStocksInf(stock)
        df.loc[df.shape[0]-1] = df_stock

    df = updateTotalRow_AllStockFile(df)
    df.reset_index(drop=True, inplace=True)
    df.to_csv(allStocksCsvPath, index=False)
    df.to_excel(allStocksExcelPath, index=False)


# Stocks Lists Part
def updateStockInfForSplit(stock):
    stockName = stock['Stock'].values[0]
    date = stock['Update Date'].values[0]

    split_ratio = checkIsSplit(stockName, date)
    lot = round(stock['Lot'].values[0] * split_ratio, 3)
    price = round(stock['Price'].values[0] / split_ratio, 3)
    total = round(stock['Lot'].values[0] * stock['Price'].values[0], 3)
    updateDate = datetime.date.today()

    stock_list = [stock['Date'].values[0], stock['Type'].values[0], stock['Stock'].values[0], price,
                  lot, total, stock['Commission'].values[0], updateDate]

    return stock_list


def checkIsSplit(stock, date):
    split_date, split_ratio = getSplitInfos(stock)

    if split_date is None:
        return 1

    date = pd.to_datetime(date, format="%Y-%m-%d")
    split_date = pd.to_datetime(split_date, format="%Y-%m-%d")

    if split_date > date:
        print(f"There are split\nSplit Date: {split_date}, Ratio: {split_ratio}")
        return split_ratio

    return 1


def getSplitInfos(stock):
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
            print(
                f"(*) Split Date: {split_date}, Numerator: {numerator}, Denominator: {denominator}, Ratio: {split_ratio}")

        return split_date, split_ratio

    except KeyError:
        return None, None


def updateSpecificStockForSplit(stockName):
    df = pd.read_csv(historyCsvPath)

    for ind in df.index:
        if df.loc[ind]['Stock'] == stockName:
            data = df.loc[ind]
            data_dict = data.to_dict()
            data_dict = {key: pd.Series([value]) for key, value in data_dict.items()}
            updated_stock = updateStockInfForSplit(data_dict)
            df.loc[ind] = updated_stock

    df.to_csv(historyCsvPath, index=False)
    update_AllStockFile(stockName)


def updateAllStocksForSplit():
    df = pd.read_csv(allStocksCsvPath)

    for ind in df.index:
        if df.loc[ind]['Stock'] == '-':
            break
        updateSpecificStockForSplit(df.loc[ind]['Stock'])


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
    info.iloc[:, 0] = info.iloc[:, 0].apply(
        lambda date: str(pd.to_datetime(date.replace('/', '-'), format="%d-%m-%Y")).split()[0])
    info.iloc[:, 1] = info.iloc[:, 1].apply(lambda name: str(name.split(" - ")[0]) + ".IS")
    info.iloc[:, 2] = info.iloc[:, 2].apply(lambda name: "Buy" if name == "ALIŞ" else "Sell")
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
                 'Commission': [round(commission, 3)],
                 'Update Date': [row['Date']]}

        addNewStock(stock)

    pdfResult = None
