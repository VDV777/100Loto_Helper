import re
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
from Main.MenuElements.Widget_Combination import Widget_Combination
from Main.MenuElements.Widget_CombinationsList import Widget_CombinationsList
from Main.MenuElements.Widget_PlotStatistic import Widget_PlotStatistic
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

    # w = Widget_CombinationsList()
    # w.show()
    #
    # w.addCombination('1,2,3,4 + 5,6,3,2')
    # w.addCombination('1,2,3,4 + 5,6,3,1')
    # w.addCombination('1,2,3,4 + 5,6,3,3')
    # w.addCombination('1,2,3,4 + 5,6,3,4')
    # w.addCombination('1,2,3,4 + 5,6,3,5')
    # w.addCombination('1,2,3,4 + 5,6,3,6')
    # w.addCombination('1,2,3,4 + 5,6,3,7')
    # w.addCombination('1,2,3,4 + 5,6,3,8')
    # w.addCombination('1,2,3,4 + 5,6,3,9')
    # w.addCombination('1,2,3,4 + 5,6,3,10')


    # w = Widget_Ticket(2, [4, 4], [20, 20])
    # w.show()
    #
    # wps = Widget_PlotStatistic()
    # wps.show()
    # wps.add_combination('1,2,3,4')
    # wps.add_combination('10,20,30,40')

    # wps.updatePlot([1, 1, 2, 3, 4, 5, 5, 5, 6])

    mainMenu = Main()



    sys.exit(qApp.exec())
