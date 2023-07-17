from tkinter import *


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


def createScreen(window):
    label = Label(window, text=title)
    label.pack()
