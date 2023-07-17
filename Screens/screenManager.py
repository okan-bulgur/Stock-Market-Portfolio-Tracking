from tkinter import *

from Screens import menuBar
from Screens import newTransactionScreen as nts
from Screens import mainScreen as ms
from Screens import showInformationsScreen as sis


class screenManager:
    window = None
    mainFrame = None

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

    def __init__(self):
        self.window = Tk()
        self.window.title(self.title)
        icon = PhotoImage(file='res\\logo.png')
        self.window.iconphoto(True, icon)
        self.window.geometry(f'{self.screenWidth}x{self.screenHeight}')
        self.openMainScreen()
        menuBar.createMenuBar(self, self.window)
        self.window.mainloop()

    def setTitle(self, title):
        self.title = title

    def openMainScreen(self):
        if self.mainFrame:
            self.mainFrame.forget()
        self.window.title(ms.title)
        self. mainFrame = Frame(self.window)
        ms.createScreen(self. mainFrame)
        self. mainFrame.pack(expand=True, fill=BOTH)

    def openAddNewTransactionScreen(self):
        self.mainFrame.forget()
        self.window.title(nts.title)
        self. mainFrame = Frame(self.window)
        nts.createInputsArea(self.mainFrame)
        self.mainFrame.pack(expand=True, fill=BOTH)

    def openShowAverageScreen(self):
        self.mainFrame.forget()
        self.window.title(sis.title)
        self. mainFrame = Frame(self.window)
        sis.createScreen(self.mainFrame)
        self.mainFrame.pack(expand=True, fill=BOTH)
