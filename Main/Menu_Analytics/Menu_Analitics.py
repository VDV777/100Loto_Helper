from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QGridLayout, QHBoxLayout, QVBoxLayout

from CustomWidgets.EventNotofication.EventNotification import EventNotification
from Main.MenuElements.Widget_TickerVariant import Widget_TicketVariant
from Main.MenuElements.Widget_Ticket import Widget_Ticket
from Main.Menu_Analytics.TicketInfo.Widget_TicketInfo import Widget_TicketInfo


class Menu_Analytics(QWidget):

    def __init__(self, parent: QWidget = None):
        super(Menu_Analytics, self).__init__(parent)

        self.__lay_main = QVBoxLayout()
        self.setLayout(self.__lay_main)

        self.__lay_ticketInfo = QHBoxLayout()
        self.__lay_combinationsAnalytics = QHBoxLayout()

        self.widgetTicketInfo = Widget_TicketInfo()
        self.widgetTicketInfo.pb_addVariant.clicked.connect(self.__e_pb_addVariant_clicked)

        self.lst_widget_ticketVariant: list[Widget_TicketVariant] = []

        self.__backgroundSetting: str = ''

        self.__setWidgetSettings()
        self.__addWidgetsToLayout()

    def __e_pb_addVariant_clicked(self) -> None:

        for side in self.widgetTicketInfo.ticketPreview.getSides():
            if side.getEnabledCellsCount() != side.valuesCountToGuess:
                EventNotification().animation_start('Выбрано не верное количество ячеек', 'red')
                return

        for side, ticketVariant in zip(self.widgetTicketInfo.ticketPreview.getSides(), self.lst_widget_ticketVariant):
            if not ticketVariant.enabledVariant(side.getEnabledCells()):
                EventNotification().animation_start('Такая комбинация уже использована', 'red')
                return

        self.widgetTicketInfo.ticketPreview.setAllCellsToDefault()

    def __setWidgetSettings(self):

        self.setMinimumSize(500, 300)

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)

        self.show()

    def __addWidgetsToLayout(self):

        self.__lay_main.addLayout(self.__lay_ticketInfo)
        self.__lay_main.addLayout(self.__lay_combinationsAnalytics)

        self.__lay_ticketInfo.addWidget(self.widgetTicketInfo)

    def addCombinationsAnalytics(self, widgetTicket: Widget_Ticket):

        for side in widgetTicket.getSides():

            wtv = Widget_TicketVariant(side)
            self.__lay_combinationsAnalytics.addWidget(wtv)
            self.lst_widget_ticketVariant.append(wtv)

    def clearAllWidgets(self):

        self.widgetTicketInfo.clearWidget()
        self.lst_widget_ticketVariant.clear()

        for i in reversed(range(self.__lay_combinationsAnalytics.count())):
            widget = self.__lay_combinationsAnalytics.itemAt(i).widget()
            self.__lay_combinationsAnalytics.removeWidget(widget)

    def setBackgroundColor(self, newColorDefault: str = 'white') -> None:

        self.__backgroundSetting = str(
            f'{self.__class__.__name__}'
            '{'
            f'background-color: {newColorDefault};'
            'margin:0px; border:5px solid black'
            '}'
        )

        self.setStyleSheet(self.__backgroundSetting)