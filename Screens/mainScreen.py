from tkinter import *
import stockManager as sm

title = "Stock Market Portfolio Tracking"

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

infLabel = Label


def createScreen(frame):
    frame.config(bg=backgroundColor)
    infPart(frame)


def crtInfLabel():
    global infLabel
    infLabel = Label(text="", font=(fontType, fontSize + 15, 'bold'))
    infLabel.config(bg=backgroundColor)
    infLabel.place(relx=0.25, rely=0.1, relwidth=0.5, relheight=0.8)


def infPart(frame):
    # Update Btn
    updateBtn = Button(frame, text="Update", font=(fontType, fontSize))
    updateBtn.config(fg=btnForegroundColor, bg=btnBackgroundColor,
                     activeforeground=hoverBtnForegroundColor, activebackground=hoverBtnBackgroundColor)
    updateBtn.config(command=update)
    updateBtn.place(relx=0.88, rely=0.03, relwidth=0.1, relheight=0.05)

    # Update For Split Btn
    updateBtn = Button(frame, text="Update For Split", font=(fontType, fontSize))
    updateBtn.config(fg=btnForegroundColor, bg=btnBackgroundColor,
                     activeforeground=hoverBtnForegroundColor, activebackground=hoverBtnBackgroundColor)
    updateBtn.config(command=sm.updateAllStocksForSplit)
    updateBtn.place(relx=0.88, rely=0.1, relwidth=0.1, relheight=0.05)

    # Information Part
    crtInfLabel()
    updateInfLabel()


def updateInfLabel():
    global infLabel

    inf = sm.getPortfolioInf()

    principalInvested = inf['Principal Invested']
    currentTotal = inf['Current Total']
    profit = inf['Profit']
    changePerc = inf['Change Percentage']
    txt = f'Principal Invested : {principalInvested} \n\n Current Total : {currentTotal}' \
          f' \n\n Profit : {profit} \n\n Change Percentage : {changePerc}'

    color = 'green' if profit >= 0 else 'red'

    infLabel.config(text=txt)
    infLabel.config(fg=color)


def update():
    sm.updateInformations()
    updateInfLabel()
