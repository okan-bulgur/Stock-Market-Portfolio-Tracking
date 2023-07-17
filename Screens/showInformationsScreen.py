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
    createStocksBtn(inputFrame, 0, 0, 10, 10)


def createStocksBtn(frame, row, column, padY, padX):
    stockBtn = Menubutton(frame, text="Select Stock", fg=btnForegroundColor, bg=btnBackgroundColor,
                          activeforeground=hoverBtnForegroundColor, activebackground=hoverBtnBackgroundColor,
                          font=(fontType, fontSize))
    stockBtn.grid(row=row, column=column, pady=padY, padx=padX)

    stocksMenu = Menu(stockBtn, tearoff=0)
    stocks = sm.getStocksList()
    for stock in stocks:
        stocksMenu.add_command(label=stock, command=partial(showAverage, stock, frame, row, column + 1, padY, padX))

    stockBtn['menu'] = stocksMenu


def createTextArea(frame):
    global header, txtArea

    header = Label(frame, text="", background=foregroundColor, foreground='#FFC3A1', font=(fontType, fontSize + 8))
    header.place(relx=0, rely=0, relheight=0.1, relwidth=1)

    txtArea = Text(frame, bg='#FAF8F1', fg=foregroundColor,  font=(fontType, fontSize + 5), state='disabled')
    txtArea.place(relx=0, rely=0.1, relheight=0.9, relwidth=1)

    scroll_y = Scrollbar(txtArea)
    scroll_y.pack(side=RIGHT, fill=Y)

    txtArea.config(yscrollcommand=scroll_y.set)
    scroll_y.config(command=txtArea.yview)


def showAverage(stock, window, row, column, padY, padX):
    global header, txtArea

    inf = sm.getInformation(stock)
    stc = inf['Stock']
    average = inf['Average']
    lot = inf['Lot']
    principalInvested = inf['Principal Invested']
    txt = f'●  Average : {average} \t Lot : {lot} \t Principal Invested : {principalInvested}\n'

    header.config(text=stc)
    txtArea.config(state='normal')
    txtArea.delete('1.0', END)
    txtArea.insert('end', txt)
    txtArea.config(state='disable')

