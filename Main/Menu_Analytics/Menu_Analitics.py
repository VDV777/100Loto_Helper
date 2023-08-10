import re
import time

from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtWidgets import QWidget, QGridLayout, QHBoxLayout, QVBoxLayout

from CustomWidgets.EventNotofication.EventNotification import EventNotification
from Main.MenuElements.Widget_CombinationsList import Widget_CombinationsList
from Main.MenuElements.Widget_PlotStatistic import Widget_PlotStatistic
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

        self.__lay_combinationsList = QHBoxLayout()

        self.__lay_plotStatistic = QHBoxLayout()

        self.widgetTicketInfo = Widget_TicketInfo()
        self.widgetTicketInfo.pb_addVariant.clicked.connect(self.__e_pb_addVariant_clicked)

        self.__lst_widget_plotStatistic: list[Widget_PlotStatistic] = []

        self.__w_combinationsList: Widget_CombinationsList = Widget_CombinationsList()
        self.__w_combinationsList.removeCombo.connect(self.__removeComboFromPlot)

        self.__backgroundSetting: str = ''

        self.__setWidgetSettings()
        self.__addWidgetsToLayout()

    def __e_pb_addVariant_clicked(self) -> None:

        for side in self.widgetTicketInfo.ticketPreview.getSides():
            if side.getEnabledCellsCount() != side.valuesCountToGuess:
                EventNotification().animation_start('Выбрано не верное количество ячеек', 'red')
                return

        combination: str = ''
        for side in self.widgetTicketInfo.ticketPreview.getSides():

            if combination != '':
                combination += ' + ' + ', '.join(str(item) for item in side.getEnabledCells())
            else:
                combination += ', '.join(str(item) for item in side.getEnabledCells())

        if not self.__w_combinationsList.addCombination(combination):
            return

        for side, plot in zip(self.widgetTicketInfo.ticketPreview.getSides(), self.__lst_widget_plotStatistic):
            plot.add_combination(side.getEnabledCells_str())

        # if not ticketVariant.enabledVariant(side.getEnabledCells()):
        # EventNotification().animation_start('Такая комбинация уже использована', 'red')
        # return

        # self.__w_combinationsList.addCombination()

        self.widgetTicketInfo.ticketPreview.setAllCellsToDefault()

    def __setWidgetSettings(self):

        self.setMinimumSize(500, 300)

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)

        self.show()

    def __addWidgetsToLayout(self):

        self.__lay_main.addLayout(self.__lay_ticketInfo)
        self.__lay_main.addLayout(self.__lay_combinationsAnalytics)
        self.__lay_main.addLayout(self.__lay_plotStatistic)

        self.__lay_ticketInfo.addWidget(self.widgetTicketInfo)

        self.__lay_combinationsAnalytics.addWidget(self.__w_combinationsList)

    def create_plotsStatistic(self, widgetTicket: Widget_Ticket):

        for side in widgetTicket.getSides():

            wps = Widget_PlotStatistic()
            self.__lay_plotStatistic.addWidget(wps)
            self.__lst_widget_plotStatistic.append(wps)

            # wtv = Widget_TicketVariant(side)
            # self.__lay_combinationsAnalytics.addWidget(wtv)
            # self.lst_widget_ticketVariant.append(wtv)
        # if self.__w_combinationsList is None:
        #     self.__w_combinationsList = Widget_CombinationsList()
        #     self.__lay_combinationsAnalytics.addWidget(self.__w_combinationsList)
        # else:
        #     self.__lay_combinationsAnalytics.addWidget(self.__w_combinationsList)

    @pyqtSlot(str)
    def __removeComboFromPlot(self, combination: str):

        pattern = r'([\d\,]+)'
        matches = re.findall(pattern, combination.replace(' ', ''))

        for match, plot in zip(matches, self.__lst_widget_plotStatistic):
            plot.remove_combination(match.replace(',', ', '))

    def clearAllWidgets(self):

        # сносим билет
        self.widgetTicketInfo.clearWidget()
        # сносим лист со списком комбинаций
        self.__w_combinationsList.delete()
        # сносим ллоты со статистикой
        for plot in self.__lst_widget_plotStatistic:
            self.__lay_plotStatistic.removeWidget(plot)
        self.__lst_widget_plotStatistic.clear()

        # for i in reversed(range(self.__lay_combinationsAnalytics.count())):
        #     widget = self.__lay_combinationsAnalytics.itemAt(i).widget()
        #     self.__lay_combinationsAnalytics.removeWidget(widget)

    def setBackgroundColor(self, newColorDefault: str = 'white') -> None:

        self.__backgroundSetting = str(
            f'{self.__class__.__name__}'
            '{'
            f'background-color: {newColorDefault};'
            'margin:0px; border:5px solid black'
            '}'
        )

        self.setStyleSheet(self.__backgroundSetting)
