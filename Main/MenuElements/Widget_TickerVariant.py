import itertools
import random
import re

import pandas as pd
from PyQt6.QtCore import Qt, QRectF
from PyQt6.QtGui import QBrush, QColor, QFont
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QListWidget, QPushButton, QCheckBox, \
    QVBoxLayout, QListWidgetItem

from CustomWidgets.Label.Label_1 import Label_1
from CustomWidgets.LineEdit.LineEdit_AllSymbols import LineEdit_AllSymbols
from CustomWidgets.LineEdit.LineEdit_IntOnly import LineEdit_IntOnly
import pyqtgraph as pg

from Main.MenuElements.Widget_Ticket import Widget_Ticket
from Main.MenuElements.Widget_TicketSide import Widget_TicketSide


class Widget_TicketVariant(QWidget):

    def __init__(self, ticket: Widget_Ticket, parent: QWidget = None):
        super(Widget_TicketVariant, self).__init__(parent)

        self.__ticket = ticket
        self.__df_combinations: pd.DataFrame = self.__ticket.ticket_combinations().copy()
        self.__df_combinations['Hidden'] = False
        self.__df_combinations['Picked'] = False
        self.__df_combinations['Excluded'] = False
        self.__df_combinations['ID'] = self.__df_combinations.index

        self.__lay_main = QVBoxLayout()
        self.__lay_variantManager = QHBoxLayout()
        self.__lay_variants = QHBoxLayout()
        self.__lay_plot = QHBoxLayout()
        self.setLayout(self.__lay_main)

        self.__backgroundSetting = ''

        self.__lw_variants = QListWidget()
        self.__lw_variants.itemDoubleClicked.connect(self.__e_lw_variants_clicked)
        self.__lw_variants.setStyleSheet('QListWidget''{''background-color: #333333''}')

        self.__pb_mixVariants = QPushButton('Mix')
        self.__pb_mixVariants.clicked.connect(self.__e_pb_mixVariants_clicked)

        self.__pb_reset = QPushButton('Reset')
        self.__pb_reset.clicked.connect(self.__e_pb_reset_clicked)

        self.__lbl_variantFilter = Label_1()
        self.__lbl_variantFilter.setText('Скрыть варианты, которые включают цифры:')
        self.__lbl_variantFilter.setFontSettings(newFontWeight=1000, newFontColor='white', newFontSize=12)
        self.__le_variantFilter = LineEdit_AllSymbols()
        self.__le_variantFilter.textChanged.connect(self.__e_le_variantFilter_changed)

        self.__plot = pg.PlotWidget()
        self.__plot.setBackground('#333333')

        self.__setWidgetSettings()
        self.__addWidgetsToLayout()
        self.__addVariants()

    def __setWidgetSettings(self):
        self.setBackgroundColor('#6749d7')
        self.show()

    def __addWidgetsToLayout(self):

        self.__lay_main.addLayout(self.__lay_variantManager)
        self.__lay_main.addLayout(self.__lay_variants)
        self.__lay_main.addLayout(self.__lay_plot)

        self.__lay_variantManager.addWidget(self.__pb_mixVariants)
        self.__lay_variantManager.addWidget(self.__pb_reset)
        self.__lay_variantManager.addWidget(self.__lbl_variantFilter)
        self.__lay_variantManager.addWidget(self.__le_variantFilter)

        self.__lay_variants.addWidget(self.__lw_variants)

        # self.__lay_plot.addWidget(self.__plot)

    def enabledVariant(self, valuesToGuess: list[int]) -> bool:

        listValueToGuess = ', '.join(str(x) for x in valuesToGuess)

        i = 0
        for row in self.__df_combinations.itertuples(index=False):

            variantList = row[:self.__ticket.valuesCountToGuess]  # (1,2,3)
            variantOfValues = ', '.join(str(x) for x in variantList)  # (1,2,3) to '1,2,3'

            if listValueToGuess == variantOfValues:
                if row.Picked is True:
                    return False
                else:
                    self.__df_combinations.at[i, 'Picked'] = True
                    itemID = self.__df_combinations.at[i, 'ID']
                    item = self.__lw_variants.item(itemID)
                    item.setBackground(QBrush(QColor('red')))
                    self.__updatePlot()
                    return True
            i += 1

    def __addVariants(self) -> None:

        for row in self.__df_combinations.itertuples(index=False):

            variantList = row[:self.__ticket.valuesCountToGuess]  # (1,2,3)
            variantOfValues = ', '.join(str(x) for x in variantList)  # (1,2,3) to '1,2,3'

            item = QListWidgetItem(variantOfValues)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item.setForeground(QBrush(QColor('white')))
            item.setFont(QFont('Consolas', 12, 800, False))

            self.__lw_variants.addItem(item)

    def __e_pb_reset_clicked(self):
        self.__resetToDefault()

    def __resetToDefault(self):

        self.__lw_variants.clear()

        for row in self.__df_combinations.itertuples(index=False):
            variantList = row[:self.__ticket.valuesCountToGuess]  # (1,2,3)
            variantOfValues = ', '.join(str(x) for x in variantList)  # (1,2,3) to '1,2,3'

            item = QListWidgetItem(variantOfValues)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item.setForeground(QBrush(QColor('white')))
            item.setFont(QFont('Consolas', 12, 800, False))

            self.__lw_variants.addItem(item)

        self.__df_combinations['Hidden'] = False
        self.__df_combinations['Picked'] = False
        self.__df_combinations['Excluded'] = False

        self.__plot.clear()

    def __e_pb_mixVariants_clicked(self):
        self.__mixVariants()

    def __mixVariants(self):

        self.__lw_variants.clear()

        df_shuffled = self.__df_combinations.sample(frac=1).reset_index(drop=True)

        for row in df_shuffled.itertuples(index=False):
            variantList = row[:self.__ticket.valuesCountToGuess]  # (1,2,3)
            variantOfValues = ', '.join(str(x) for x in variantList)  # (1,2,3) to '1,2,3'

            item = QListWidgetItem(variantOfValues)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item.setForeground(QBrush(QColor('white')))
            item.setFont(QFont('Consolas', 12, 800, False))
            item.setBackground(QBrush(QColor('red'))) if row.Picked else item.setBackground(QBrush(QColor('#333333')))
            self.__lw_variants.addItem(item)

            item.setBackground(QBrush(QColor('red'))) if row.Picked else item.setBackground(QBrush(QColor('#333333')))
            item.setHidden(True) if row.Excluded is True else item.setHidden(False)

    def __e_le_variantFilter_changed(self, text: str):

        digitsExcludeListStr = [num for num in text.split(',')]
        digitsExcludeListInt = []
        for symbol in digitsExcludeListStr:
            if symbol.isdigit():
                digitsExcludeListInt.append(int(symbol))

        self.__df_combinations.loc[self.__df_combinations.loc[:, :self.__ticket.valuesCountToGuess - 1].isin(digitsExcludeListInt).any(axis=1), ['Excluded', 'Hidden']] = True
        self.__df_combinations.loc[~self.__df_combinations.loc[:, :self.__ticket.valuesCountToGuess - 1].isin(digitsExcludeListInt).any(axis=1), ['Excluded', 'Hidden']] = False

        self.__lw_variants.clear()

        for row in self.__df_combinations.itertuples(index=False):
            variantList = row[:self.__ticket.valuesCountToGuess]  # (1,2,3)
            variantOfValues = ', '.join(str(x) for x in variantList)  # (1,2,3) to '1,2,3'

            item = QListWidgetItem(variantOfValues)
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item.setForeground(QBrush(QColor('white')))
            item.setFont(QFont('Consolas', 12, 800, False))
            self.__lw_variants.addItem(item)

            item.setBackground(QBrush(QColor('red'))) if row.Picked else item.setBackground(QBrush(QColor('#333333')))
            item.setHidden(True) if row.Excluded is True else item.setHidden(False)

    def __e_lw_variants_clicked(self, item: QListWidgetItem) -> None:

        rowIndex = self.__lw_variants.row(item)
        index = (self.__df_combinations.loc[self.__df_combinations['ID'] == rowIndex]).index.values[0]

        if item.background() == QColor('red'):
            item.setBackground(QBrush(QColor('#333333')))
            self.__df_combinations.at[index, 'Picked'] = False
        else:
            item.setBackground(QBrush(QColor('red')))
            self.__df_combinations.at[index, 'Picked'] = True

        self.__updatePlot()

    def __updatePlot(self):

        df_filter: pd.DataFrame = self.__df_combinations.loc[self.__df_combinations['Picked'] == True].reset_index(drop=True)

        # Выбор области данных между столбцами 1 и 3
        data_subset: pd.DataFrame = df_filter.iloc[:, :self.__ticket.valuesCountToGuess]

        # Преобразование области данных в список
        values_list = list(itertools.chain.from_iterable(data_subset.values.tolist()))

        # Вычисление частоты повторений значений
        values, counts = zip(*[(x, values_list.count(x)) for x in set(values_list)])
        self.__plot.clear()
        bar_chart = pg.BarGraphItem(x=values, height=counts, width=0.5, brush='#6749d7', pen='white')
        # Создание экземпляра TextItem с текстом
        text_item = pg.TextItem(text='Всего выбрано комбинаций: ' + data_subset.index.__len__().__str__(), anchor=(0, 0), color=(255, 255, 255))
        self.__plot.addItem(bar_chart)
        self.__plot.addItem(text_item)

    def setBackgroundColor(self, newColorDefault: str = 'white') -> None:

        self.__backgroundSetting = str(
            f'{self.__class__.__name__}'
            '{'
            f'background-color: {newColorDefault};'
            'margin:0px; border:5px solid black'
            '}'
        )

        self.setStyleSheet(self.__backgroundSetting)

# class Widget_TicketVariant(QWidget):
#
#     def __init__(self, ticketSide: Widget_TicketSide, parent: QWidget = None):
#         super(Widget_TicketVariant, self).__init__(parent)
#
#         self.__ticketSide = ticketSide
#         self.__df_combinations: pd.DataFrame = self.__ticketSide.combinations().copy()
#         self.__df_combinations['Hidden'] = False
#         self.__df_combinations['Picked'] = False
#         self.__df_combinations['Excluded'] = False
#         self.__df_combinations['ID'] = self.__df_combinations.index
#
#         self.__lay_main = QVBoxLayout()
#         self.__lay_variantManager = QHBoxLayout()
#         self.__lay_variants = QHBoxLayout()
#         self.__lay_plot = QHBoxLayout()
#         self.setLayout(self.__lay_main)
#
#         self.__backgroundSetting = ''
#
#         self.__lw_variants = QListWidget()
#         self.__lw_variants.itemDoubleClicked.connect(self.__e_lw_variants_clicked)
#         self.__lw_variants.setStyleSheet('QListWidget''{''background-color: #333333''}')
#
#         self.__pb_mixVariants = QPushButton('Mix')
#         self.__pb_mixVariants.clicked.connect(self.__e_pb_mixVariants_clicked)
#
#         self.__pb_reset = QPushButton('Reset')
#         self.__pb_reset.clicked.connect(self.__e_pb_reset_clicked)
#
#         self.__lbl_variantFilter = Label_1()
#         self.__lbl_variantFilter.setText('Скрыть варианты, которые включают цифры:')
#         self.__lbl_variantFilter.setFontSettings(newFontWeight=1000, newFontColor='white', newFontSize=12)
#         self.__le_variantFilter = LineEdit_AllSymbols()
#         self.__le_variantFilter.textChanged.connect(self.__e_le_variantFilter_changed)
#
#         self.__plot = pg.PlotWidget()
#         self.__plot.setBackground('#333333')
#
#         self.__setWidgetSettings()
#         self.__addWidgetsToLayout()
#         self.__addVariants()
#
#     def __setWidgetSettings(self):
#         self.setBackgroundColor('#6749d7')
#         self.show()
#
#     def __addWidgetsToLayout(self):
#
#         self.__lay_main.addLayout(self.__lay_variantManager)
#         self.__lay_main.addLayout(self.__lay_variants)
#         self.__lay_main.addLayout(self.__lay_plot)
#
#         self.__lay_variantManager.addWidget(self.__pb_mixVariants)
#         self.__lay_variantManager.addWidget(self.__pb_reset)
#         self.__lay_variantManager.addWidget(self.__lbl_variantFilter)
#         self.__lay_variantManager.addWidget(self.__le_variantFilter)
#
#         self.__lay_variants.addWidget(self.__lw_variants)
#
#         self.__lay_plot.addWidget(self.__plot)
#
#     def enabledVariant(self, valuesToGuess: list[int]) -> bool:
#
#         listValueToGuess = ', '.join(str(x) for x in valuesToGuess)
#
#         i = 0
#         for row in self.__df_combinations.itertuples(index=False):
#
#             variantList = row[:self.__ticketSide.valuesCountToGuess]  # (1,2,3)
#             variantOfValues = ', '.join(str(x) for x in variantList)  # (1,2,3) to '1,2,3'
#
#             if listValueToGuess == variantOfValues:
#                 if row.Picked is True:
#                     return False
#                 else:
#                     self.__df_combinations.at[i, 'Picked'] = True
#                     itemID = self.__df_combinations.at[i, 'ID']
#                     item = self.__lw_variants.item(itemID)
#                     item.setBackground(QBrush(QColor('red')))
#                     self.__updatePlot()
#                     return True
#             i += 1
#
#     def __addVariants(self) -> None:
#
#         for row in self.__df_combinations.itertuples(index=False):
#
#             variantList = row[:self.__ticketSide.valuesCountToGuess]  # (1,2,3)
#             variantOfValues = ', '.join(str(x) for x in variantList)  # (1,2,3) to '1,2,3'
#
#             item = QListWidgetItem(variantOfValues)
#             item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
#             item.setForeground(QBrush(QColor('white')))
#             item.setFont(QFont('Consolas', 12, 800, False))
#
#             self.__lw_variants.addItem(item)
#
#     def __e_pb_reset_clicked(self):
#         self.__resetToDefault()
#
#     def __resetToDefault(self):
#
#         self.__lw_variants.clear()
#
#         for row in self.__df_combinations.itertuples(index=False):
#             variantList = row[:self.__ticketSide.valuesCountToGuess]  # (1,2,3)
#             variantOfValues = ', '.join(str(x) for x in variantList)  # (1,2,3) to '1,2,3'
#
#             item = QListWidgetItem(variantOfValues)
#             item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
#             item.setForeground(QBrush(QColor('white')))
#             item.setFont(QFont('Consolas', 12, 800, False))
#
#             self.__lw_variants.addItem(item)
#
#         self.__df_combinations['Hidden'] = False
#         self.__df_combinations['Picked'] = False
#         self.__df_combinations['Excluded'] = False
#
#         self.__plot.clear()
#
#     def __e_pb_mixVariants_clicked(self):
#         self.__mixVariants()
#
#     def __mixVariants(self):
#
#         self.__lw_variants.clear()
#
#         df_shuffled = self.__df_combinations.sample(frac=1).reset_index(drop=True)
#
#         for row in df_shuffled.itertuples(index=False):
#             variantList = row[:self.__ticketSide.valuesCountToGuess]  # (1,2,3)
#             variantOfValues = ', '.join(str(x) for x in variantList)  # (1,2,3) to '1,2,3'
#
#             item = QListWidgetItem(variantOfValues)
#             item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
#             item.setForeground(QBrush(QColor('white')))
#             item.setFont(QFont('Consolas', 12, 800, False))
#             item.setBackground(QBrush(QColor('red'))) if row.Picked else item.setBackground(QBrush(QColor('#333333')))
#             self.__lw_variants.addItem(item)
#
#             item.setBackground(QBrush(QColor('red'))) if row.Picked else item.setBackground(QBrush(QColor('#333333')))
#             item.setHidden(True) if row.Excluded is True else item.setHidden(False)
#
#     def __e_le_variantFilter_changed(self, text: str):
#
#         digitsExcludeListStr = [num for num in text.split(',')]
#         digitsExcludeListInt = []
#         for symbol in digitsExcludeListStr:
#             if symbol.isdigit():
#                 digitsExcludeListInt.append(int(symbol))
#
#         self.__df_combinations.loc[self.__df_combinations.loc[:, :self.__ticketSide.valuesCountToGuess - 1].isin(digitsExcludeListInt).any(axis=1), ['Excluded', 'Hidden']] = True
#         self.__df_combinations.loc[~self.__df_combinations.loc[:, :self.__ticketSide.valuesCountToGuess - 1].isin(digitsExcludeListInt).any(axis=1), ['Excluded', 'Hidden']] = False
#
#         self.__lw_variants.clear()
#
#         for row in self.__df_combinations.itertuples(index=False):
#             variantList = row[:self.__ticketSide.valuesCountToGuess]  # (1,2,3)
#             variantOfValues = ', '.join(str(x) for x in variantList)  # (1,2,3) to '1,2,3'
#
#             item = QListWidgetItem(variantOfValues)
#             item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
#             item.setForeground(QBrush(QColor('white')))
#             item.setFont(QFont('Consolas', 12, 800, False))
#             self.__lw_variants.addItem(item)
#
#             item.setBackground(QBrush(QColor('red'))) if row.Picked else item.setBackground(QBrush(QColor('#333333')))
#             item.setHidden(True) if row.Excluded is True else item.setHidden(False)
#
#     def __e_lw_variants_clicked(self, item: QListWidgetItem) -> None:
#
#         rowIndex = self.__lw_variants.row(item)
#         index = (self.__df_combinations.loc[self.__df_combinations['ID'] == rowIndex]).index.values[0]
#
#         if item.background() == QColor('red'):
#             item.setBackground(QBrush(QColor('#333333')))
#             self.__df_combinations.at[index, 'Picked'] = False
#         else:
#             item.setBackground(QBrush(QColor('red')))
#             self.__df_combinations.at[index, 'Picked'] = True
#
#         self.__updatePlot()
#
#     def __updatePlot(self):
#
#         df_filter: pd.DataFrame = self.__df_combinations.loc[self.__df_combinations['Picked'] == True].reset_index(drop=True)
#
#         # Выбор области данных между столбцами 1 и 3
#         data_subset: pd.DataFrame = df_filter.iloc[:, :self.__ticketSide.valuesCountToGuess]
#
#         # Преобразование области данных в список
#         values_list = list(itertools.chain.from_iterable(data_subset.values.tolist()))
#
#         # Вычисление частоты повторений значений
#         values, counts = zip(*[(x, values_list.count(x)) for x in set(values_list)])
#         self.__plot.clear()
#         bar_chart = pg.BarGraphItem(x=values, height=counts, width=0.5, brush='#6749d7', pen='white')
#         # Создание экземпляра TextItem с текстом
#         text_item = pg.TextItem(text='Всего выбрано комбинаций: ' + data_subset.index.__len__().__str__(), anchor=(0, 0), color=(255, 255, 255))
#         self.__plot.addItem(bar_chart)
#         self.__plot.addItem(text_item)
#
#     def setBackgroundColor(self, newColorDefault: str = 'white') -> None:
#
#         self.__backgroundSetting = str(
#             f'{self.__class__.__name__}'
#             '{'
#             f'background-color: {newColorDefault};'
#             'margin:0px; border:5px solid black'
#             '}'
#         )
#
#         self.setStyleSheet(self.__backgroundSetting)

