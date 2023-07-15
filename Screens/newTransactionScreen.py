import tkinter
from tkinter import *
from tkinter import messagebox
from tkcalendar import Calendar
from functools import partial
import stockManager as stockM


title = "New Transaction"

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

date = None
type = None
name = None
price = None
lot = None


def createInputsArea(window):
    createTypeBtn(window, 0, 0, 10, 10)
    createCalendarBtn(window, 1, 0, 10, 10)
    createNameBox(window, 2, 0, 10, 10)
    createPriceBox(window, 4, 0, 10, 10)
    createLotBox(window, 6, 0, 10, 10)
    createNewTransactionBtn(window, 8, 0, 10, 10)


def createCalendarBtn(window, row, column, padY, padX):
    outputLabel = Label(window, text="", foreground=foregroundColor, font=(fontType, fontSize))
    outputLabel.grid(row=row, column=column + 1, pady=padY, padx=padX)

    calendarBtn = Button(window, text="Select Date", fg=btnForegroundColor, bg=btnBackgroundColor,
                         activeforeground=hoverBtnForegroundColor, activebackground=hoverBtnBackgroundColor,
                         font=(fontType, fontSize))
    calendarBtn.config(command=partial(createCalendar, window, outputLabel))
    calendarBtn.grid(row=row, column=column, pady=padY, padx=padX)


def createCalendar(window, outputLabel):
    calendarWindow = Toplevel(window)
    calendarWindow.title("Date")
    calendarWindow.resizable(False, False)
    calendar = Calendar(calendarWindow, selectmode="day", date_pattern="yyyy-mm-dd")

    btn = Button(calendarWindow, text="Select Date", command=partial(getDate, calendar, outputLabel),
                 fg=btnForegroundColor, bg=btnBackgroundColor,
                 activeforeground=hoverBtnForegroundColor, activebackground=hoverBtnBackgroundColor,
                 font=(fontType, fontSize))
    btn.pack(side=BOTTOM, fill=BOTH)

    calendar.pack()


def getDate(calendar, outputLabel):
    global date
    date = calendar.get_date()
    outputLabel.config(text=date)


def createTypeBtn(window, row, column, padY, padX):
    typeBtn = Menubutton(window, text="Select Type", fg=btnForegroundColor, bg=btnBackgroundColor,
                         activeforeground=hoverBtnForegroundColor, activebackground=hoverBtnBackgroundColor,
                         font=(fontType, fontSize))
    typeBtn.grid(row=row, column=column, pady=padY, padx=padX)

    types = Menu(typeBtn, tearoff=0)
    types.add_command(label="Buy", command=lambda: setType("Buy", window, row, column, padY, padX))
    types.add_command(label="Sell", command=lambda: setType("Sell", window, row, column, padY, padX))

    typeBtn['menu'] = types


def setType(value, window, row, column, padY, padX):
    global type
    type = value
    outputLabel = Label(window, text=type, foreground=foregroundColor, font=(fontType, fontSize))
    outputLabel.grid(row=row, column=column + 1, pady=padY, padx=padX)


def createNameBox(window, row, column, padY, padX):
    headerLabel = Label(window, text="Enter Stock", foreground=foregroundColor, font=(fontType, fontSize))
    headerLabel.grid(row=row, column=column, pady=padY, padx=padX)

    inputBox = Entry(window)
    inputBox.grid(row=row + 1, column=column, pady=padY, padx=padX - padX / 2)

    outputLabel = Label(window, text="", foreground=foregroundColor, font=(fontType, fontSize))
    outputLabel.grid(row=row + 1, column=column + 2, pady=padY, padx=padX)

    enterBtn = Button(window, text="✓", fg=btnForegroundColor, bg=btnBackgroundColor,
                      activeforeground=hoverBtnForegroundColor, activebackground=hoverBtnBackgroundColor,
                      font=(fontType, fontSize))
    enterBtn.config(command=partial(getName, inputBox, outputLabel))
    enterBtn.grid(row=row + 1, column=column + 1, pady=padY, padx=padX)


def getName(inputBox, outputLabel):
    global name
    name = inputBox.get()
    outputLabel.config(text=name)


def createPriceBox(window, row, column, padY, padX):
    headerLabel = Label(window, text="Enter Price", foreground=foregroundColor, font=(fontType, fontSize))
    headerLabel.grid(row=row, column=column, pady=padY, padx=padX)

    inputBox = Entry(window)
    inputBox.grid(row=row + 1, column=column, pady=padY, padx=padX - padX / 2)

    outputLabel = Label(window, text="", foreground=foregroundColor, font=(fontType, fontSize))
    outputLabel.grid(row=row + 1, column=column + 2, pady=padY, padx=padX)

    enterBtn = Button(window, text="✓", fg=btnForegroundColor, bg=btnBackgroundColor,
                      activeforeground=hoverBtnForegroundColor, activebackground=hoverBtnBackgroundColor,
                      font=(fontType, fontSize))
    enterBtn.config(command=partial(getPrice, inputBox, outputLabel))
    enterBtn.grid(row=row + 1, column=column + 1, pady=padY, padx=padX)


def getPrice(inputBox, outputLabel):
    try:
        global price
        price = float(inputBox.get())
        if price <= 0:
            raise ValueError
        outputLabel.config(text=price)
    except ValueError:
        tkinter.messagebox.showwarning(title="Error", message="Invalid Price")


def createLotBox(window, row, column, padY, padX):
    headerLabel = Label(window, text="Enter Lot", foreground=foregroundColor, font=(fontType, fontSize))
    headerLabel.grid(row=row, column=column, pady=padY, padx=padX)

    inputBox = Entry(window)
    inputBox.grid(row=row + 1, column=column, pady=padY, padx=padX - padX / 2)

    outputLabel = Label(window, text="", foreground=foregroundColor, font=(fontType, fontSize))
    outputLabel.grid(row=row + 1, column=column + 2, pady=padY, padx=padX)

    enterBtn = Button(window, text="✓", fg=btnForegroundColor, bg=btnBackgroundColor,
                      activeforeground=hoverBtnForegroundColor, activebackground=hoverBtnBackgroundColor,
                      font=(fontType, fontSize))
    enterBtn.config(command=partial(getLot, inputBox, outputLabel))
    enterBtn.grid(row=row + 1, column=column + 1, pady=padY, padx=padX)


def getLot(inputBox, outputLabel):
    try:
        global lot
        lot = int(inputBox.get())
        if lot <= 0:
            raise ValueError
        outputLabel.config(text=lot)
    except ValueError:
        tkinter.messagebox.showwarning(title="Error", message="Invalid Lot Amount")


def createNewTransactionBtn(window, row, column, padY, padX):
    enterBtn = Button(window, text="Create", fg=btnForegroundColor, bg=btnBackgroundColor,
                      activeforeground=hoverBtnForegroundColor, activebackground=hoverBtnBackgroundColor,
                      font=(fontType, fontSize))
    enterBtn.config(command=createNewTransaction)
    enterBtn.grid(row=row, column=column, pady=padY, padx=padX)


def createNewTransaction():
    global lot

    if (date is None) or (type is None) or (name is None) or (price is None) or (lot is None):
        tkinter.messagebox.showwarning(title="Error", message="Enter all values")
        return

    if type == 'Sell':
        lot *= -1

    stock = {'Date': [date], 'Type': [type], 'Stock': [name], 'Price': [price], 'Lot': [lot], 'Total': [price * lot]}
    stockM.addNewStock(stock)
