from tkinter import *
import stockManager as sm

title = "Averages"

screenWidth = 1500
screenHeight = 700

fontSize = 12
fontType = 'Arial'

backgroundColor = '#F9F5E7'
foregroundColor = '#A75D5D'

btnBackgroundColor = '#D3756B'
btnForegroundColor = '#F9F5E7'
hoverBtnBackgroundColor = '#F0997D'
hoverBtnForegroundColor = '#F9F5E7'


def createScreen(window):
    createStocksBtn(window, 0, 0, 10, 10)


def createStocksBtn(window, row, column, padY, padX):
    stockBtn = Menubutton(window, text="Select Stock", fg=btnForegroundColor, bg=btnBackgroundColor,
                          activeforeground=hoverBtnForegroundColor, activebackground=hoverBtnBackgroundColor,
                          font=(fontType, fontSize))
    stockBtn.grid(row=row, column=column, pady=padY, padx=padX)

    stocksMenu = Menu(stockBtn, tearoff=0)
    stocks = sm.getStocksList()
    for stock in stocks:
        stocksMenu.add_command(label=stock, command=lambda: showAverage(stock, window, row, column + 1, padY, padX))

    stockBtn['menu'] = stocksMenu

def showAverage(stock, window, row, column, padY, padX):
    average = sm.getAverage(stock)
    txt = f'{stock} : {average}'
    outputLabel = Label(window, text=txt, foreground=foregroundColor, font=(fontType, fontSize))
    outputLabel.grid(row=row, column=column + 1, pady=padY, padx=padX)
