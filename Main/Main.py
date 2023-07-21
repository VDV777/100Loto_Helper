from enum import Enum, IntEnum

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QGridLayout
from screeninfo import get_monitors

from CustomWidgets.EventNotofication.EventNotification import EventNotification
from CustomWidgets.PushButton.PushButton_Circle_1 import PushButton_Circle_1
from Main.MenuNavigator import MenuNavigator
from Main.Menu_Analytics.Menu_Analitics import Menu_Analytics
from Main.StartMenu.StartMenu import StartMenu


class Main(QWidget):

    def __init__(self):
        super(Main, self).__init__()

        self.__lay_main: QGridLayout = QGridLayout(self)

        self.__setWidgetSettings()
        self.__initWidgets()

    def __setWidgetSettings(self):

        for monitor in get_monitors():
            if monitor.is_primary:
                self.setGeometry(0, 0, (monitor.width / 2).__int__(), (monitor.height / 2).__int__())
                self.move((monitor.width / 2).__int__() - (monitor.width / 2 / 2).__int__(), (monitor.height / 2).__int__() - (monitor.height / 2 / 2).__int__())

        self.setStyleSheet('''
        Main
        {
        background-color: #303030;
        }
        ''')

        self.show()

    def __initWidgets(self):

        self.__menuNavigator = MenuNavigator()

        self.__startMenu = StartMenu()
        self.__startMenu.setBackgroundColor('#6749d7')

        self.__analyticMenu = Menu_Analytics()
        self.__analyticMenu.hide()
        self.__analyticMenu.setBackgroundColor('#6749d7')

        self.__pb_back = PushButton_Circle_1(iconPath='back.png', iconMarginIndent=20, isMirroredIcon=True)
        self.__pb_back.clicked.connect(self.__e_pb_back_clicked)
        self.__pb_back.setBorderSettings(newColor_pressed='cyan')
        self.__pb_back.setDisabled(True)
        self.__pb_next = PushButton_Circle_1(iconPath='back.png', iconMarginIndent=20)
        self.__pb_next.clicked.connect(self.__e_pb_next_clicked)
        self.__pb_next.setBorderSettings(newColor_pressed='cyan')

        self.__addWidgetsToLayout()

    def __addWidgetsToLayout(self):

        self.__lay_main.addWidget(self.__startMenu, 1, 1, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.__lay_main.addWidget(self.__analyticMenu, 1, 1, 1, 1, Qt.AlignmentFlag.AlignCenter)

        self.__lay_main.addWidget(self.__pb_back, 2, 0, 1, 1, Qt.AlignmentFlag.AlignLeft)
        self.__lay_main.addWidget(self.__pb_next, 2, 2, 1, 1, Qt.AlignmentFlag.AlignRight)

    def __e_pb_back_clicked(self) -> None:

        self.__menuNavigator.previousMenu()

        if self.__menuNavigator.menu == MenuNavigator.START:
            self.__pb_back.setDisabled(True)
            self.__pb_next.setDisabled(False)
            self.__startMenu.show()
            self.__analyticMenu.hide()
            self.__analyticMenu.clearAllWidgets()

    def __e_pb_next_clicked(self) -> None:
        try:
            self.__menuNavigator.nextMenu()

            if self.__startMenu.bIsReady and self.__menuNavigator.menu == MenuNavigator.ANALYTIC:
                self.__startMenu.hide()
                self.__pb_next.setDisabled(True)
                self.__pb_back.setDisabled(False)
                self.__analyticMenu.show()
                self.__analyticMenu.widgetTicketInfo.createWidget(self.__startMenu.ticketPreview.sidesCount, self.__startMenu.ticketPreview.valuesCountToGuess, self.__startMenu.ticketPreview.digitsMaxValues)
                self.__analyticMenu.addCombinationsAnalytics(self.__analyticMenu.widgetTicketInfo.ticketPreview)
            else:
                EventNotification().animation_start('Заполните все поля')

        except Exception as e:
            print(e)




