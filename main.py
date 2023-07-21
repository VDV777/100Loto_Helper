import sys
from itertools import combinations

import numpy as np
import pandas as pd
from PyQt6.QtCore import Qt, QEvent, QObject
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import QApplication, QTableWidgetItem, QTableWidget, QHeaderView, QListWidget, QListWidgetItem, \
    QWidget, QHBoxLayout, QMainWindow
import pyqtgraph as pg

from CustomWidgets.EventNotofication.EventNotification import EventNotification
from CustomWidgets.Table.Table_1 import Table_1
from Main.Main import Main
from Main.MenuElements.Widget_TickerVariant import Widget_TicketVariant
from Main.MenuElements.Widget_Ticket import Widget_Ticket
from Main.MenuElements.Widget_TicketSide import Widget_TicketSide


# def calculate_combinations():
#     numbers = list(range(1, 21))  # Список чисел от 1 до 20
#     combinations_dict = {}
#
#     # Генерация всех возможных комбинаций из 4 чисел
#     for comb in combinations(numbers, 4):
#         sum_comb = sum(comb)  # Сумма чисел комбинации
#
#         # Проверка суммы комбинации на уникальность
#         if sum_comb not in combinations_dict:
#             combinations_dict[sum_comb] = comb
#
#     unique_combinations = list(combinations_dict.values())
#
#     return unique_combinations
#
#
# result = calculate_combinations()
# print("Количество комбинаций:", len(result))
# print("Уникальные комбинации:", result)
#
# from itertools import product
#
# # Пример использования
# list1 = [[1, 2], [3, 4]]
# list2 = [[5, 6], [7, 8]]
# list3 = [list1, list2]


# print(list(product(list3)))

if __name__ == '__main__':

    qApp = QApplication(sys.argv)

    # ei = EventNotification()
    #
    # mm = Main()
    # mm.show()
    #
    # d = {1: '1'}
    # d.setdefault(2, '2')
    # d.sorted()

    # df = pd.DataFrame(data=[{'0': 5, '1': 6, '2': 7, '3': 8}, {'0': 0, '1': 1, '2': 2, '3': 3}], columns=['0', '1', '2', '3'], index=None)
    # print(df)
    # print(df.values.tolist())
    # print(pd.DataFrame(df.values.tolist()))

    # wts = Widget_TicketSide('', 20, 4)
    # wts.show()
    #
    # print(wts.combinations())
    # wtv = Widget_TicketVariant()
    # wtv.addVariants(wts.maxValueOfDigits, wts.valuesCountToGuess, wts.combinations())
    # wtv.show()
    # qtw = Table_1(df)
    #
    # qtw.setBackgroundColor(newWidgetColor='white', newHeaderColor='green', newHeaderHoverColor='yellow', newHeaderPressedColor='blue',  newCellColor='white', newCellHoverColor='yellow', newCellSelectedColor='purple', newCornerButtonColor='white')
    # qtw.show()

    mainMenu = Main()

    # elementsSum = []
    # elementsSumWithIndex = []
    # for index, element in enumerate(arrVariants):
    #
    #     print(index, element)
    #
    #     elementsSumWithIndex.append([index, element.sum()])
    #     elementsSum.append(element.sum())
    #
    # print(arrVariants.__len__(), elementsSum.__len__(), set(elementsSum).__len__())

    # qTab = QTabWidget()
    # qTab.show()
    # qTab.addTab(QWidget(), 'Tab_1')
    # qTab.addTab(QWidget(), 'Tab_2')

    # main = QWidget()
    # main.show()
    # lay = QGridLayout()
    # main.setLayout(lay)
    # sp1 = QSplitter(Qt.Orientation.Horizontal)
    # w1 = QFrame()
    # w1.setFrameShape(QFrame.Shape.StyledPanel)
    # w2 = QFrame()
    # w2.setFrameShape(QFrame.Shape.StyledPanel)
    # sp1.addWidget(w1)
    # sp1.addWidget(w2)
    #
    # lay.addWidget(sp1)

    # _100_loto = _100_LOTO()

    sys.exit(qApp.exec())
