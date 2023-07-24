from tkinter import *
from functools import partial
import stockManager as sm

title = "Informations of the Stocks"

screenWidth = 1500
screenHeight = 700

fontSize = 12
fontType = 'Arial'

backgroundColor = '#FFFBF5'
foregroundColor = '#A75D5D'

btnBackgroundColor = '#D3756B'
btnForegroundColor = '#F9F5E7'
hoverBtnBackgroundColor = '#F0997D'
hoverBtnForegroundColor = '#F9F5E7'

header = Label
txtArea = Text


def createScreen(window):
    mainFrame = Frame(window)
    mainFrame.place(relx=0, rely=0, relheight=1, relwidth=1)

    inputFrame = Frame(mainFrame, bg=backgroundColor)
    inputFrame.place(relx=0, rely=0, relheight=0.4, relwidth=1)

    outputFrame = Frame(mainFrame, bg=backgroundColor)
    outputFrame.place(relx=0, rely=0.4, relheight=0.6, relwidth=1)

    createTextArea(outputFrame)
    createStocksBtn(inputFrame)


def createStocksBtn(frame):
    stocks = sm.getStocksList()
    stocksVar = [IntVar() for _ in stocks]

    column = -1
    rowCycle = 3

    for i, stock in enumerate(stocks):
        btn = Checkbutton(frame, text=stock, variable=stocksVar[i], fg=foregroundColor,
                          bg=backgroundColor, font=(fontType, fontSize, 'bold'))
        row = i % rowCycle
        if row == 0: column += 1
        btn.grid(row=row, column=column, padx=10, pady=10)

    showBtn = Button(frame, text="Show", font=(fontType, fontSize))
    showBtn.config(fg=btnForegroundColor, bg=btnBackgroundColor,
                   activeforeground=hoverBtnForegroundColor, activebackground=hoverBtnBackgroundColor)
    showBtn.config(command=partial(showInformations, stocks, stocksVar))
    showBtn.grid(row=rowCycle+1, column=0, padx=10, pady=10)


def createTextArea(frame):
    global header, txtArea

    header = Label(frame, text="Informations", background=foregroundColor, foreground='#FFC3A1',
                   font=(fontType, fontSize + 8))
    header.place(relx=0, rely=0, relheight=0.1, relwidth=1)

    txtArea = Text(frame, bg='#FAF8F1', fg=foregroundColor, font=(fontType, fontSize + 5), state='disabled')
    txtArea.place(relx=0, rely=0.1, relheight=0.9, relwidth=1)

    scroll_y = Scrollbar(txtArea)
    scroll_y.pack(side=RIGHT, fill=Y)

    txtArea.config(yscrollcommand=scroll_y.set)
    scroll_y.config(command=txtArea.yview)


def showInformations(stocks, stocksVar):
    global txtArea

    txtArea.config(state='normal')
    txtArea.delete(1.0, END)

    selectedStocks = [stock.get() for stock in stocksVar]
    selectedStocks = [stocks[i] for i in range(len(stocks)) if selectedStocks[i] == 1]

    for stock in selectedStocks:
        inf = sm.getInformationByStock(stock)

        stc = inf['Stock']
        lot = inf['Lot']
        average = inf['Average']
        principalInvested = inf['Principal Invested']
        currentTotal = inf['Current Total']
        profit = inf['Profit']
        changePerc = inf['Change Percentage']
        txt = f'●  Stock : {stc} \t Lot : {lot} \t Average : {average} \t Principal Invested : {principalInvested} \t Current Total : {currentTotal}' \
              f' \t Profit : {profit} \t Change Percentage : {changePerc}\n'

        txtArea.insert('end', txt)
        txtArea.config(state='disable')
