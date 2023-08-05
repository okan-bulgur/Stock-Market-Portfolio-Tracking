from tkinter import Menu


def createMenuBar(sm, window):
    menubar = Menu()
    window.config(menu=menubar)

    fileMenu = Menu(menubar, tearoff=0)
    menubar.add_command(label="Home", command=lambda: sm.openMainScreen())
    menubar.add_command(label="Add New Transaction", command=lambda: sm.openAddNewTransactionScreen())
    menubar.add_command(label="Stocks Informations", command=lambda: sm.openShowAverageScreen())
