import os

import numpy as np
import pandas as pd
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QLabel, QPushButton, QGroupBox, QFileDialog, QTableWidget, QTableWidgetItem

from CustomWidgets.Label.Label_1 import Label_1
from CustomWidgets.LineEdit.LineEdit_IntOnly import LineEdit_IntOnly
from Main.MenuElements.Widget_Ticket import Widget_Ticket


class StartMenu(QWidget):

    def __init__(self, parent: QWidget = None):
        super(StartMenu, self).__init__(parent)

        self.__lay_main = QGridLayout()
        self.__lay_main.setSpacing(20)
        self.setLayout(self.__lay_main)

        self.__backgroundSetting: str = ''

        self.bIsReady = False
        # side count
        self.__lbl_sideCount = Label_1()
        self.__lbl_sideCount.setFontSettings(newFontWeight=1000, newFontColor='white', newFontSize=12)
        self.__lbl_sideCount.setText('Введите количество сторон в билете')
        self.__le_sideCount = LineEdit_IntOnly()
        self.__le_sideCount.setMaxLength(1)
        self.__le_sideCount.textChanged.connect(self.e_le_sideCount_textChanged)
        # max value
        self.__lbl_maxValue = Label_1()
        self.__lbl_maxValue.hide()
        self.__lbl_maxValue.setFontSettings(newFontWeight=1000, newFontColor='white', newFontSize=12)
        self.__lbl_maxValue.setText('Введите максимальное значение чисел для каждой стороны билета')
        self.__list_le_maxValue: list[LineEdit_IntOnly] = list()
        # count values to guess
        self.__lbl_countValuesToGuess = Label_1()
        self.__lbl_countValuesToGuess.hide()
        self.__lbl_countValuesToGuess.setFontSettings(newFontWeight=1000, newFontColor='white', newFontSize=12)
        self.__lbl_countValuesToGuess.setText('Укажите какое количество цифр необходимо угадать для каждой стороны билета')
        self.__list_le_countValuesToGuess: list[LineEdit_IntOnly] = list()
        # ticket preview
        self.ticketPreview: Widget_Ticket = None

        self.__addWidgetsToLayout()

        self.__setWidgetSettings()

        self.show()

    def __setWidgetSettings(self):

        self.setMinimumSize(500, 300)

        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)

    def __addWidgetsToLayout(self):

        self.__lay_main.addWidget(self.__lbl_sideCount, 0, 0, 1, 3, Qt.AlignmentFlag.AlignCenter)
        self.__lay_main.addWidget(self.__le_sideCount, 1, 0, 1, 3, Qt.AlignmentFlag.AlignCenter)
        self.__lay_main.addWidget(self.__lbl_maxValue, 2, 0, 1, 3, Qt.AlignmentFlag.AlignCenter)
        self.__lay_main.addWidget(self.__lbl_countValuesToGuess, 4, 0, 1, 3, Qt.AlignmentFlag.AlignCenter)

    def e_le_sideCount_textChanged(self, text: str):

        if text == '':

            self.__lbl_countValuesToGuess.hide()
            self.__clear_le_countValuesToGuess()
            self.__lay_main.removeWidget(self.ticketPreview)
            self.ticketPreview = None

            self.__lbl_maxValue.hide()
            self.__clear_le_maxValues()
        else:

            self.__lbl_countValuesToGuess.hide()
            self.__clear_le_countValuesToGuess()
            self.__lay_main.removeWidget(self.ticketPreview)
            self.ticketPreview = None

            self.__lbl_maxValue.hide()
            self.__clear_le_maxValues()

            for sideCount in range(int(text)):
                le_maxValue = LineEdit_IntOnly()
                le_maxValue.setMaxLength(2)
                le_maxValue.textChanged.connect(self.e_le_maxValue_textChanged)
                self.__lay_main.addWidget(le_maxValue, 3, sideCount, 1, 1, Qt.AlignmentFlag.AlignCenter)
                self.__list_le_maxValue.append(le_maxValue)
            self.__lbl_maxValue.show()

    def e_le_maxValue_textChanged(self, text: str) -> None:

        if self.__isMaxValuesEmpty():
            self.__lbl_countValuesToGuess.hide()
            self.__clear_le_countValuesToGuess()
            self.__lay_main.removeWidget(self.ticketPreview)
            self.ticketPreview = None
        else:
            self.__lbl_countValuesToGuess.hide()
            self.__clear_le_countValuesToGuess()
            self.__lay_main.removeWidget(self.ticketPreview)
            self.ticketPreview = None

            self.__lbl_countValuesToGuess.show()

            for index, le_maxValue in enumerate(self.__list_le_maxValue):

                le = LineEdit_IntOnly()
                le.setMaxLength(1)
                le.textChanged.connect(self.__e_le_countValuesToGuess_textChanged)
                self.__lay_main.addWidget(le, 5, index, 1, 1, Qt.AlignmentFlag.AlignCenter)
                self.__list_le_countValuesToGuess.append(le)

    def __clear_le_maxValues(self):

        for le in self.__list_le_maxValue:
            le.disconnect()
            self.__lay_main.removeWidget(le)
        self.__list_le_maxValue.clear()

    def __isMaxValuesEmpty(self) -> bool:

        for le in self.__list_le_maxValue:

            if le.text() == '':
                return True

        return False

    def __e_le_countValuesToGuess_textChanged(self, text: str) -> None:

        if self.__isCountValuesToGuessEmpy():

            if self.ticketPreview is not None:

                self.__lay_main.removeWidget(self.ticketPreview)
                self.ticketPreview = None
                self.bIsReady = False
        else:
            maxValues: list[int] = []
            countValuesToGuess: list[int] = []

            for le_maxValue, le_countValuesToGuess in zip(self.__list_le_maxValue, self.__list_le_countValuesToGuess):
                maxValues.append(int(le_maxValue.text()))
                countValuesToGuess.append(int(le_countValuesToGuess.text()))

            self.ticketPreview = Widget_Ticket(int(self.__le_sideCount.text()), countValuesToGuess, maxValues)
            self.__lay_main.addWidget(self.ticketPreview, 7, 0, 1, 3, Qt.AlignmentFlag.AlignCenter)
            self.ticketPreview.show()
            self.bIsReady = True

    def __clear_le_countValuesToGuess(self):

        for le in self.__list_le_countValuesToGuess:
            le.disconnect()
            self.__lay_main.removeWidget(le)
        self.__list_le_countValuesToGuess.clear()

    def __isCountValuesToGuessEmpy(self) -> bool:

        for value in self.__list_le_countValuesToGuess:

            if value.text() == '':
                return True

        return False

    def setBackgroundColor(self, newColorDefault: str = 'white') -> None:

        self.__backgroundSetting = str(
            f'{self.__class__.__name__}'
            '{'
            f'background-color: {newColorDefault};'
            'margin:0px; border:5px solid black'
            '}'
        )

        self.setStyleSheet(self.__backgroundSetting)


# class _100_LOTO(QWidget):
#
#     def __init__(self):
#         super(_100_LOTO, self).__init__()
#
#         self.lay_main = QVBoxLayout()
#         self.setLayout(self.lay_main)
#
#         self.lay_menuSettings = QGridLayout()
#         self.lbl_filePath = QLabel()
#
#         self.tw_tickets = QTableWidget()
#         self.tw_tickets.setColumnCount(8)
#         self.tw_tickets.setHorizontalHeaderLabels(['Дата розыгрыша', 'Цифра 1', 'Цифра 2', 'Цифра 3', 'Цифра 4', 'Цифра 5', 'Цифра 6', 'Цифра 7'])
#
#         self.tw_mostRepeatedValues = QTableWidget()
#         self.tw_mostRepeatedValues.setColumnCount(2)
#         self.tw_mostRepeatedValues.setHorizontalHeaderLabels(['Число', 'Количество повторений'])
#
#         # self.lbl_maxValue = QLabel('Максимальное значение')
#         # self.lbl_valuesCount = QLabel('Количество чисел')
#         # self.le_digitMinValue = QLineEdit()
#         # self.le_digitMinValue.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         # self.le_digitMinValue.setValidator(QIntValidator(1, 999))
#         # self.le_digitMaxValue = QLineEdit()
#         # self.le_digitMaxValue.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         # self.le_digitMaxValue.setValidator(QIntValidator(1, 999))
#         # self.le_digitsCount = QLineEdit()
#         # self.le_digitsCount.setAlignment(Qt.AlignmentFlag.AlignCenter)
#         # self.le_digitsCount.setValidator(QIntValidator(1, 999))
#         self.pb_save = QPushButton('Загрузить')
#         self.pb_save.clicked.connect(self.load)
#         # self.pb_load = QPushButton('Загрузить')
#         # self.pb_load.clicked.connect(self.load)
#         # self.pb_generate = QPushButton('Сгенерировать')
#         # self.pb_generate.clicked.connect(self.generate)
#
#         self.lay_menuSettings.addWidget(self.lbl_filePath, 1, 1, 1, 1, Qt.AlignmentFlag.AlignCenter)
#         # self.lay_menuSettings.addWidget(self.lbl_maxValue, 1, 2, 1, 1, Qt.AlignmentFlag.AlignCenter)
#         # self.lay_menuSettings.addWidget(self.lbl_valuesCount, 1, 3, 1, 1, Qt.AlignmentFlag.AlignCenter)
#         # self.lay_menuSettings.addWidget(self.le_digitMinValue, 2, 1, 1, 1, Qt.AlignmentFlag.AlignCenter)
#         # self.lay_menuSettings.addWidget(self.le_digitMaxValue, 2, 2, 1, 1, Qt.AlignmentFlag.AlignCenter)
#         # self.lay_menuSettings.addWidget(self.le_digitsCount, 2, 3, 1, 1, Qt.AlignmentFlag.AlignCenter)
#         self.lay_menuSettings.addWidget(self.pb_save, 1, 2, 1, 1, Qt.AlignmentFlag.AlignCenter)
#         # self.lay_menuSettings.addWidget(self.pb_load, 2, 5, 1, 1, Qt.AlignmentFlag.AlignCenter)
#         # self.lay_menuSettings.addWidget(self.pb_generate, 2, 6, 1, 1, Qt.AlignmentFlag.AlignCenter)
#
#         self.lay_digits = QGridLayout()
#         self.gb_digit = QGroupBox()
#         self.gb_digit.setTitle('Аналитика')
#
#         self.lay_digitsSurface = QGridLayout()
#         self.gb_digit.setLayout(self.lay_digitsSurface)
#         self.lay_digitsSurface.addWidget(self.tw_tickets)
#         self.lay_digitsSurface.addWidget(self.tw_mostRepeatedValues)
#         self.lay_digits.addWidget(self.gb_digit)
#
#         self.lay_main.addLayout(self.lay_menuSettings)
#         self.lay_main.addLayout(self.lay_digits)
#
#         # self.list_pbDigits = list()
#         self.df: pd.DataFrame = None
#
#         self.show()
#
#     def save(self):
#         print('save')
#
#     def load(self):
#         try:
#             file, _ = QFileDialog.getOpenFileName(self, 'Open File', './', "DB (*.xlsx *.xls *scv);;Text files (*.txt);;Any()")
#
#             if file:
#                 self.lbl_filePath.setText(file)
#
#                 self.df = pd.read_excel(os.path.abspath(file), index_col=None)
#                 # df_copy = pd.to_datetime(self.df['Дата розыгрыша'])
#                 df_copy: pd.DataFrame = self.df.iloc[:, 1:9]
#                 df_copy.index = self.df['Дата розыгрыша']
#                 s_matchCount: pd.Series = None
#                 for column in df_copy:
#                     if s_matchCount is None:
#                         s_matchCount = pd.Series(df_copy[column].to_list())
#                     else:
#                         s_matchCount = pd.concat([s_matchCount, pd.Series(df_copy[column].to_list())], ignore_index=True)
#
#                 self.create_digitsRating(s_matchCount.value_counts())
#
#                 self.createNewTableFromDF(df_copy)
#
#         except Exception as e:
#             print(e)
#
#     def createNewTableFromDF(self, df: pd.DataFrame):
#         self.clearTable(self.tw_tickets)
#
#         for i in range(df.index.__len__()):
#             self.tw_tickets.insertRow(i)
#             item = QTableWidgetItem(df.index[i].__str__())
#             item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
#             self.tw_tickets.setItem(i, 0, item)
#             for j in range(df.columns.__len__()):
#                 item = QTableWidgetItem(df.iloc[i][j].__str__())
#                 item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
#                 self.tw_tickets.setItem(i, j + 1, item)
#
#     def create_digitsRating(self, series: pd.Series):
#
#         self.clearTable(self.tw_mostRepeatedValues)
#
#         i = 0
#         for index, val in series.items():
#             # print(index, val)
#             self.tw_mostRepeatedValues.insertRow(i)
#             item_1 = QTableWidgetItem(index.__str__())
#             item_1.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
#             item_2 = QTableWidgetItem(val.__str__())
#             item_2.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
#             self.tw_mostRepeatedValues.setItem(i, 0, item_1)
#             self.tw_mostRepeatedValues.setItem(i, 1, item_2)
#             i += 1
#
#     def clearTable(self, table):
#         for i in range(table.rowCount()):
#             table.removeRow(i)
#
#     def generate(self):
#
#         for i in reversed(range(self.lay_digitsSurface.count())):
#             self.lay_digitsSurface.removeItem(self.lay_digitsSurface.itemAt(i))
#
#         minValue = int(self.le_digitMinValue.text())
#         maxValue = int(self.le_digitMaxValue.text())
#         digitsCount = int(self.le_digitsCount.text())
#         rr = np.arange(minValue, maxValue + 1)
#         np.random.shuffle(rr)
#
#         for i in range(minValue, maxValue, digitsCount):
#             pb = QPushButton(rr[i:i+digitsCount].__str__())
#             pb.setCheckable(True)
#             pb.setStyleSheet('''
#             :checked { background-color: red;}
#             ''')
#             self.lay_digitsSurface.addWidget(pb)
