import tkinter
from tkinter import *
from tkinter import messagebox, filedialog
from tkcalendar import Calendar
from functools import partial
from yahoo_fin.stock_info import *

import stockManager as stockM

title = "New Transaction"

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

date = None
type = None
name = None
price = None
lot = None
commission = None

filePath = None


def createInputsArea(window):
    manuelFrame = Frame(window)
    pdfFrame = Frame(window)

    manuelFrame.place(relx=0, rely=0, relwidth=0.5, relheight=1)
    pdfFrame.place(relx=0.5, rely=0, relwidth=0.5, relheight=1)

    createManuelArea(manuelFrame)
    createPdfArea(pdfFrame)


def createManuelArea(window):
    createTypeBtn(window, 0, 0, 10, 10)
    createCalendarBtn(window, 1, 0, 10, 10)
    createNameBox(window, 2, 0, 10, 10)
    createPriceBox(window, 4, 0, 10, 10)
    createLotBox(window, 6, 0, 10, 10)
    createCommissionBox(window, 8, 0, 10, 10)
    createNewTransactionBtn(window, 10, 0, 10, 10)


def createPdfArea(window):
    createPdfElements(window)


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
    name = inputBox.get().upper()
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


def createCommissionBox(window, row, column, padY, padX):
    headerLabel = Label(window, text="Enter Commision", foreground=foregroundColor, font=(fontType, fontSize))
    headerLabel.grid(row=row, column=column, pady=padY, padx=padX)

    inputBox = Entry(window)
    inputBox.grid(row=row + 1, column=column, pady=padY, padx=padX - padX / 2)

    outputLabel = Label(window, text="", foreground=foregroundColor, font=(fontType, fontSize))
    outputLabel.grid(row=row + 1, column=column + 2, pady=padY, padx=padX)

    enterBtn = Button(window, text="✓", fg=btnForegroundColor, bg=btnBackgroundColor,
                      activeforeground=hoverBtnForegroundColor, activebackground=hoverBtnBackgroundColor,
                      font=(fontType, fontSize))
    enterBtn.config(command=partial(getCommission, inputBox, outputLabel))
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


def getCommission(inputBox, outputLabel):
    try:
        global commission
        commission = float(inputBox.get())
        if commission <= 0:
            raise ValueError
        outputLabel.config(text=commission)
    except ValueError:
        tkinter.messagebox.showwarning(title="Error", message="Invalid Commission Amount")


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

    try:
        get_live_price(name)
    except:
        tkinter.messagebox.showwarning(title="Error", message=f"There are no stock named {name}")
        return

    if type == 'Sell':
        if stockM.checkValidLotAmount(name, lot):
            lot *= -1
        else:
            tkinter.messagebox.showwarning(title="Error", message="There are not enough lot for sell")
            return

    stock = {'Date': [date], 'Type': [type], 'Stock': [name], 'Price': [price], 'Lot': [lot], 'Total': [round(price * lot, 3)], 'Commission': [commission], 'Update Date': [date]}
    stockM.addNewStock(stock)


def getPdfPath(txtArea, type):
    global filePath
    if type == 'Folder':
        filePath = filedialog.askdirectory()
    else:
        filePath = filedialog.askopenfilename()

    if filePath == "":
        return

    stockM.processingPdfInf(filePath, type)
    stockM.showPdfInf(txtArea)


def createPdfElements(window):
    txtArea = Text(window, wrap='none', bg='#FAF8F1', fg=foregroundColor, font=(fontType, fontSize + 5), state='disabled')
    txtArea.place(relx=0, rely=0.2, relheight=0.7, relwidth=1)

    scrollbar_y = Scrollbar(txtArea, command=txtArea.yview)
    scrollbar_x = Scrollbar(txtArea, orient=HORIZONTAL, command=txtArea.xview)
    txtArea.config(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
    scrollbar_y.pack(side=RIGHT, fill=Y)
    scrollbar_x.pack(side=BOTTOM, fill=X)

    approveBtn = Button(window, text="Approve ✓", font=(fontType, fontSize))
    approveBtn.config(fg=btnForegroundColor, bg=btnBackgroundColor,
                      activeforeground=hoverBtnForegroundColor,
                      activebackground=hoverBtnBackgroundColor)
    approveBtn.config(command=stockM.approvePdfInf)
    approveBtn.place(relx=0.1, rely=0.9, relheight=0.1, relwidth=0.3)

    cancelBtn = Button(window, text="Cancel", font=(fontType, fontSize))
    cancelBtn.config(fg=btnForegroundColor, bg=btnBackgroundColor,
                     activeforeground=hoverBtnForegroundColor,
                     activebackground=hoverBtnBackgroundColor)
    cancelBtn.config(command=partial(stockM.cancelPdfInf, txtArea))
    cancelBtn.place(relx=0.6, rely=0.9, relheight=0.1, relwidth=0.3)

    fileBtn = Button(window, text="Select Pdf By File", font=(fontType, fontSize))
    fileBtn.config(fg=btnForegroundColor, bg=btnBackgroundColor,
                   activeforeground=hoverBtnForegroundColor,
                   activebackground=hoverBtnBackgroundColor)
    fileBtn.config(command=partial(getPdfPath, txtArea, 'File'))
    fileBtn.place(relx=0.1, rely=0.1, relheight=0.05, relwidth=0.3)

    folderBtn = Button(window, text="Select Pdf By Folder", font=(fontType, fontSize))
    folderBtn.config(fg=btnForegroundColor, bg=btnBackgroundColor,
                     activeforeground=hoverBtnForegroundColor,
                     activebackground=hoverBtnBackgroundColor)
    folderBtn.config(command=partial(getPdfPath, txtArea, 'Folder'))
    folderBtn.place(relx=0.6, rely=0.1, relheight=0.05, relwidth=0.3)
