import numpy as np

import pandas as pd
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import QWidget, QPushButton, QHBoxLayout

from CustomWidgets.Label.Label_1 import Label_1


class Widget_Combination(QWidget):

    remove = pyqtSignal(str)

    def __init__(self, parent: QWidget = None, combination: str = ''):
        super(Widget_Combination, self).__init__(parent)

        self.__borderSetting = ''
        self.__backgroundSetting = ''

        self.__lay_main: QHBoxLayout = QHBoxLayout()
        self.setLayout(self.__lay_main)

        self.__lbl_combination: Label_1 = Label_1()
        self.__lbl_combination.setFontSettings(newFontColor='black', newFontSize=14, newFontWeight=800)
        self.__lbl_combination.setText(combination)

        self.__pb_deleteCombination: QPushButton = QPushButton('Х')
        self.__pb_deleteCombination.setMaximumWidth(75)
        self.__pb_deleteCombination.clicked.connect(self.__e_pb_deleteCombination_clicked)

        self.__lay_main.addWidget(self.__lbl_combination, alignment=Qt.AlignmentFlag.AlignCenter)
        self.__lay_main.addWidget(self.__pb_deleteCombination, alignment=Qt.AlignmentFlag.AlignCenter)

        self.setMaximumHeight(100)

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.setBackgroundColor('#00ff99')
        self.setBorderSettings(newColor_default='black')

    def setCombination(self, combination: str) -> None:
        """1,2,3,4 + 5,8,12,24"""
        self.__lbl_combination.setText(combination)

    def __e_pb_deleteCombination_clicked(self) -> None:
        self.remove.emit(self.__lbl_combination.text())
        self.delete()

    def delete(self) -> None:
        self.__lay_main.removeWidget(self.__lbl_combination)
        self.__lay_main.removeWidget(self.__pb_deleteCombination)
        self.deleteLater()
        
    def setBackgroundColor(self, newColorDefault: str = 'white') -> None:

        self.__backgroundSetting = str(
            f'{self.__class__.__name__}'
            '{'
            f'background-color: {newColorDefault};'
            'margin:0px; border: 5px solid black'
            '}'
        )

        self.setStyleSheet(self.__backgroundSetting)
        
    def setBorderSettings(self, newColor_default: str = 'white', borderSize_default: int = 1) -> None:

        self.__borderSetting = str(
            f'{self.__class__.__name__}'
            '{'
            f'border: {borderSize_default}px solid {newColor_default};'
            '}'
        )

        self.setStyleSheet(self.__backgroundSetting + self.__borderSetting)

