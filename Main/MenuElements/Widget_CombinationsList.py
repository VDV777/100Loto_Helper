import pandas as pd
from PyQt6.QtCore import pyqtSlot, Qt, pyqtSignal
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QScrollArea

from CustomWidgets.EventNotofication.EventNotification import EventNotification
from Main.MenuElements.Widget_Combination import Widget_Combination


class Widget_CombinationsList(QWidget):

    removeCombo = pyqtSignal(str)

    def __init__(self, parent: QWidget = None):
        super(Widget_CombinationsList, self).__init__(parent)

        self.__borderSetting = ''
        self.__fontSetting = ''
        self.__backgroundSetting = ''

        self.__lay_main: QVBoxLayout = QVBoxLayout()
        self.setLayout(self.__lay_main)

        self.__lay_settingsMenu: QHBoxLayout = QHBoxLayout()
        self.__lay_combinationsList: QVBoxLayout = QVBoxLayout()

        self.__lay_main.addLayout(self.__lay_combinationsList)
        self.__lay_main.addLayout(self.__lay_settingsMenu)

        self.__widget = QWidget()
        self.__lay_widget: QVBoxLayout = QVBoxLayout()
        self.__widget.setLayout(self.__lay_widget)

        self.__scrollArea = QScrollArea()
        self.__scrollArea.setMinimumHeight(400)
        self.__scrollArea.setWidgetResizable(True)
        self.__scrollArea.setWidget(self.__widget)
        self.__lay_combinationsList.addWidget(self.__scrollArea)

        self.__pb_clear: QPushButton = QPushButton('Clear')
        self.__pb_clear.clicked.connect(self.e_pb_clear_clicked)
        self.__lay_settingsMenu.addWidget(self.__pb_clear)

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setBackgroundColor('#cc33ff')

        self.__df_CombinationsList = pd.DataFrame(columns=['combination'], dtype=str)

    def e_pb_clear_clicked(self):

        self.__df_CombinationsList = pd.DataFrame(columns=['combination'], dtype=str)

        for i in reversed(range(self.__lay_widget.count())):

            widget = self.__lay_widget.itemAt(i).widget()

            self.__lay_widget.removeWidget(widget)

    def addCombination(self, combination: str) -> bool:

        if (self.__df_CombinationsList.combination == combination).any():
            EventNotification().animation_start('Такая комбинация уже использована', 'red')
            return False

        dfToAdd: pd.DataFrame = pd.DataFrame(data=[{'combination': combination}], columns=['combination'], dtype=str)
        self.__df_CombinationsList = pd.concat([self.__df_CombinationsList, dfToAdd])

        widgetCombination: Widget_Combination = Widget_Combination(combination=combination)
        self.__lay_widget.addWidget(widgetCombination)
        widgetCombination.remove.connect(self.__remove)

        return True

    @pyqtSlot(str)
    def __remove(self, combinationToRemove: str):
        self.__df_CombinationsList = self.__df_CombinationsList[self.__df_CombinationsList['combination'] != combinationToRemove]

        self.removeCombo.emit(combinationToRemove)

    def delete(self):

        self.e_pb_clear_clicked()

        # for i in reversed(range(self.__lay_settingsMenu.count())):
        #     widget = self.__lay_settingsMenu.itemAt(i).widget()
        #
        #     self.__lay_settingsMenu.removeWidget(widget)
        #
        # self.deleteLater()

    def setBackgroundColor(self, newColorDefault: str = 'white') -> None:

        self.__backgroundSetting = str(
            f'{self.__class__.__name__}'
            '{'
            f'background-color: {newColorDefault};'
            'margin:0px; border:5px solid black'
            '}'
        )

        self.setStyleSheet(self.__backgroundSetting)