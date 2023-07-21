from itertools import combinations, product

import numpy as np
import pandas as pd
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QGridLayout

from Main.MenuElements.Widget_TicketSide import Widget_TicketSide


class Widget_Ticket (QWidget):

    def __init__(self, sidesCount: int, valuesCountToGuess: list[int], maxValueOfDigits: list[int], parent: QWidget = None):
        super(Widget_Ticket, self).__init__(parent)

        self.__lay_main: QGridLayout = QGridLayout()
        self.setLayout(self.__lay_main)

        self.__sidesCount: int = sidesCount
        self.__maxValueOfDigits: list[int] = maxValueOfDigits
        self.__valuesCountToGuess: list[int] = valuesCountToGuess
        self.__ticketSides: list[Widget_TicketSide] = []

        self.__createSides(self.__sidesCount, self.__valuesCountToGuess, maxValueOfDigits)

        self.__backgroundSetting: str = ''

        self.__setWidgetSettings()

    def __setWidgetSettings(self):

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.show()

    def __createSides(self, sidesCount: int, valuesCountToGuess: list[int], maxValueOfDigits: list[int]) -> None:

        for side in range(sidesCount):
            ticketSide: Widget_TicketSide = Widget_TicketSide('Сторона_' + side.__str__(), maxValueOfDigits[side], valuesCountToGuess[side])
            ticketSide.setFontSettings(newFontSize=12, newFontColor='white', newFontWeight=800, newFontName='Consolas')
            ticketSide.setBorderSettings(newColor_default='white', borderSize_default=1)
            self.__lay_main.addWidget(ticketSide, 0, side, 1, 1, Qt.AlignmentFlag.AlignCenter)
            self.__ticketSides.append(ticketSide)

    def __clearSides(self) -> None:

        for side in self.__ticketSides:
            side.clearAllCells()
            self.__lay_main.removeWidget(side)

        self.__ticketSides.clear()
        self.__maxValueOfDigits.clear()
        self.__valuesCountToGuess.clear()

    def resetSides(self, sidesCount: int, valuesCountToGuess: list[int], maxValueOfDigits: list[int]):
        self.__clearSides()

        for side in range(sidesCount):
            ticketSide: Widget_TicketSide = Widget_TicketSide('Сторона_' + side.__str__(), maxValueOfDigits[side], valuesCountToGuess[side])
            ticketSide.setFontSettings(newFontSize=12, newFontColor='white', newFontWeight=800, newFontName='Consolas')
            ticketSide.setBorderSettings(newColor_default='white', borderSize_default=1)
            self.__lay_main.addWidget(ticketSide, 0, side, 1, 1, Qt.AlignmentFlag.AlignCenter)
            self.__ticketSides.append(ticketSide)

        self.__sidesCount: int = sidesCount
        self.__maxValueOfDigits: list[int] = maxValueOfDigits
        self.__valuesCountToGuess: list[int] = valuesCountToGuess

    @property
    def sidesCount(self) -> int:
        return self.__sidesCount

    @property
    def digitsMaxValues(self) -> list[int]:
        return self.__maxValueOfDigits

    @property
    def valuesCountToGuess(self) -> list[int]:
        return self.__valuesCountToGuess

    @valuesCountToGuess.setter
    def valuesCountToGuess(self, newValues: list[int]) -> None:
        self.__valuesCountToGuess = newValues

    def getSide(self, sideNumber) -> Widget_TicketSide:

        if sideNumber > self.__ticketSides.__len__():
            return None
        else:
            return self.__ticketSides[sideNumber]

    def getSides(self) -> list[Widget_TicketSide]:
        return self.__ticketSides

    def setCellsSideDefault(self, sideNumber: int) -> None:

        if 0 <= sideNumber <= self.__ticketSides.__len__():
            self.__ticketSides[sideNumber].setAllCellsDefault()

    def setAllCellsToDefault(self) -> None:

        for side in self.__ticketSides:
            side.setAllCellsDefault()

    def setCellsSideChecked(self, sideNumber: int, cells: list[int]) -> None:

        if 0 <= sideNumber <= self.__ticketSides.__len__():
            self.__ticketSides[sideNumber].setCheckedCells(cells)

    def setCellsSideDisabled(self, sideNumber: int, cells: list[int]) -> None:

        if 0 <= sideNumber <= self.__ticketSides.__len__():
            self.__ticketSides[sideNumber].setDisabledCells(cells)

    def ticket_combinationsCountSide(self, sideNumber: int) -> int:

        if sideNumber > self.__ticketSides.__len__():
            return -1

        side: Widget_TicketSide = self.__ticketSides[sideNumber]

        rangeForCombinations: list[int] = np.arange(1, side.maxValueOfDigits, 1).tolist()

        arrVariants = np.array(list(combinations(rangeForCombinations, side.valuesCountToGuess)))

        elementsSum = []
        elementsSumWithIndex = []
        for index, element in enumerate(arrVariants):

            elementsSumWithIndex.append([index, element.sum()])
            elementsSum.append(element.sum())

        return set(elementsSum).__len__()

    def ticket_combinations(self) -> list[int]:

        ticketSideCombinations: list[int] = []

        for ticketSide in self.__ticketSides:
            ticketSideCombinations.append(ticketSide.combinations().values.tolist())

        return list(product(*ticketSideCombinations))

    def ticket_combinationsCount(self) -> int:

        ticketSideCombinations: list[int] = []

        for ticketSide in self.__ticketSides:
            ticketSideCombinations.append(ticketSide.combinations().values.tolist())

        return list(product(*ticketSideCombinations)).__len__()

    def setBackgroundColor(self, newColorDefault: str = 'white') -> None:

        self.__backgroundSetting = str(
            f'{self.__class__.__name__}'
            '{'
            f'background-color: {newColorDefault};'
            '}'
        )

        self.setStyleSheet(self.__backgroundSetting)






