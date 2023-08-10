from itertools import combinations

import numpy as np
import pandas as pd
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QGroupBox, QWidget, QGridLayout

from Main.MenuElements.Widget_TicketSideCell import Widget_TicketSideCell


class Widget_TicketSide(QGroupBox):

    def __init__(self, title: str, digitsMaxValue: int, valuesCountToGuess: int, parent: QWidget = None):
        super(Widget_TicketSide, self).__init__(title, parent)

        self.__lay_main: QGridLayout = QGridLayout()
        self.setLayout(self.__lay_main)

        self.__fontSetting: str = ''
        self.__borderSetting: str = ''
        self.__backgroundSetting: str = ''

        self.__maxValueOfDigits: int = digitsMaxValue
        self.__name = title
        self.__cells: list[Widget_TicketSideCell] = list()
        self.__valuesCountToGuess: int = valuesCountToGuess

        self.__setWidgetSettings()

        self.addCells(digitsMaxValue)

    def __setWidgetSettings(self):

        self.setMinimumSize(200, 200)

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def addCells(self, maxDigit: int) -> None:

        row = 0
        column = 0

        for digit in range(1, maxDigit + 1):

            cell: Widget_TicketSideCell = Widget_TicketSideCell(digit)
            cell.setBackgroundColor(newColorDefault='white', newColorHover='grey', newColorChecked='green', newColorDisable='red', newColorPressed='green')
            cell.setFontSettings(newFontSize=12, newFontName='Consolas', newFontColor='black', newFontWeight=800)
            cell.setBorderSettings(newColor_default='white', newColor_hover='yellow', newColor_checked='green', newColor_disable='red', newColor_pressed='black', borderSize_default=1, borderSize_hover=2, borderSize_checked=2, borderSize_disable=2, borderSize_pressed=2)
            self.__lay_main.addWidget(cell, row, column, 1, 1, Qt.AlignmentFlag.AlignCenter)
            self.__cells.append(cell)
            column += 1

            if digit % 5 == 0:
                row += 1
                column = 0

    def clearAllCells(self) -> None:

        for cell in self.__cells:
            self.__lay_main.removeWidget(cell)

        self.__cells.clear()

    def setCheckedCells(self, cellsNumbers: list[int]) -> None:

        for cell in self.__cells:
            if cell.digit in cellsNumbers:
                cell.setChecked(True)

    def setDisabledCells(self, cellsNumbers: list[int]) -> None:

        for cell in self.__cells:
            if cell.digit in cellsNumbers:
                cell.setDisabled(True)

    def setAllCellsDefault(self):

        for cell in self.__cells:
            cell.setDisabled(False)
            cell.setChecked(False)

    def disableWidget(self, bFlag: bool = True) -> None:

        if bFlag:
            for cell in self.__cells:

                if cell.isChecked():
                    cell.setBackgroundColor(newColorDisable='green')
                    cell.setBorderSettings(newColor_disable='black')
                    cell.setDisabled(True)
                else:
                    cell.setBackgroundColor(newColorDisable='white')
                    cell.setBorderSettings(newColor_disable='black')
                    cell.setDisabled(True)

            self.setDisabled(True)
        else:
            self.setDisabled(False)

    def getEnabledCellsCount(self) -> int:

        enabledCells: int = 0
        for cell in self.__cells:
            if cell.isChecked():
                enabledCells += 1

        return enabledCells

    def getEnabledCells(self) -> list[int]:

        enabledCells: list[int] = []
        for cell in self.__cells:
            if cell.isChecked():
                enabledCells.append(cell.digit)
        return enabledCells

    def getEnabledCells_str(self) -> str:

        return ', '.join(str(item) for item in self.getEnabledCells())

    @property
    def valuesCountToGuess(self) -> int:

        return self.__valuesCountToGuess

    @valuesCountToGuess.setter
    def valuesCountToGuess(self, newValuesCount: int) -> None:

        self.__valuesCountToGuess = newValuesCount

    @property
    def maxValueOfDigits(self) -> int:
        return self.__maxValueOfDigits

    @maxValueOfDigits.setter
    def maxValueOfDigits(self, newDigitsMaxValue: int) -> None:

        self.__maxValueOfDigits = newDigitsMaxValue
        self.clearAllCells()
        self.addCells(newDigitsMaxValue)

    @property
    def sideName(self) -> str:
        return self.__name

    @sideName.setter
    def sideName(self, newSideName: str) -> None:
        self.__name = newSideName
        self.setTitle(self.__name)

    @property
    def cells(self) -> list[Widget_TicketSideCell]:
        return self.__cells

    def combinationsCount(self) -> int:

        rangeForCombinations: list[int] = np.arange(1, self.maxValueOfDigits + 1, 1).tolist()

        arrVariants = np.array(list(combinations(rangeForCombinations, self.valuesCountToGuess)))

        df: pd.DataFrame = pd.DataFrame(data=arrVariants, index=None)

        # df['sum'] = df[:].sum(axis=1, numeric_only=True)

        # df = df.drop_duplicates(subset=['sum'], ignore_index=True)
        #
        # df = df.loc[:, :self.__valuesCountToGuess - 1]

        return df.index.__len__()

    def combinations(self) -> pd.DataFrame:

        rangeForCombinations: list[int] = np.arange(1, self.maxValueOfDigits + 1, 1).tolist()

        arrVariants = np.array(list(combinations(rangeForCombinations, self.valuesCountToGuess)))

        df: pd.DataFrame = pd.DataFrame(data=arrVariants, index=None)

        # df['sum'] = df[:].sum(axis=1, numeric_only=True)

        # df = df.drop_duplicates(subset=['sum'], ignore_index=True)
        #
        # df = df.loc[:, :self.__valuesCountToGuess - 1]

        return df

    # # Генерируем все комбинации из 20 цифр от 1 до 20, содержащие 4 цифры
    # combinations_list = list(combinations(range(1, 21), 4))
    #
    # # Создаем множество для уникальных комбинаций на каждой стороне билета
    # unique_combinations = set(combinations_list)
    #
    # # Общее количество уникальных комбинаций на лотерейном билете
    # total_combinations = len(unique_combinations) ** 2

    def setBackgroundColor(self, newColorDefault: str = 'white') -> None:

        self.__backgroundSetting = str(
            f'{self.__class__.__name__}'
            '{'
            f'background-color: {newColorDefault};'
            '}'
        )

        self.setStyleSheet(self.__backgroundSetting + self.__fontSetting + self.__borderSetting)

    def setFontSettings(self, newFontSize: int = 14, newFontColor: str = 'black', newFontName: str = 'Consolas', newFontWeight: int = 400, textAlign: str = 'center') -> None:

        self.__fontSetting = str(
            f'{self.__class__.__name__}'
            '{'
            f'font: {newFontSize}pt {newFontName};'
            f'color : {newFontColor};'
            f'font-weight: {newFontWeight};'
            f'text-align: {textAlign};'
            'margin-top: 1.0em;'
            '}'
            f'{self.__class__.__name__}:title'
            '{'
            'subcontrol-origin: margin;'
            'subcontrol-position: top center;'
            'padding-left: -5px;'
            # 'padding-right: 10px;'
            '}'
        )

        self.setStyleSheet(self.__backgroundSetting + self.__fontSetting + self.__borderSetting)

    def setBorderSettings(self, newColor_default: str = 'white', borderSize_default: int = 1) -> None:

        self.__borderSetting = str(
            f'{self.__class__.__name__}'
            '{'
            f'border: {borderSize_default}px solid {newColor_default};'
            '}'
        )

        self.setStyleSheet(self.__backgroundSetting + self.__fontSetting + self.__borderSetting)
