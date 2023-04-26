import os

import numpy as np
import pandas as pd
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QWidget, QGridLayout, QVBoxLayout, QLineEdit, QLabel, QPushButton, QGroupBox, QSizePolicy, \
    QScrollArea, QFileDialog, QTableWidget, QTableWidgetItem, QListWidget, QTableView


class _100_LOTO(QWidget):

    def __init__(self):
        super(_100_LOTO, self).__init__()

        self.lay_main = QVBoxLayout()
        self.setLayout(self.lay_main)

        self.lay_menuSettings = QGridLayout()
        self.lbl_filePath = QLabel()

        self.tw_tickets = QTableWidget()
        self.tw_tickets.setColumnCount(8)
        self.tw_tickets.setHorizontalHeaderLabels(['Дата розыгрыша', 'Цифра 1', 'Цифра 2', 'Цифра 3', 'Цифра 4', 'Цифра 5', 'Цифра 6', 'Цифра 7'])

        self.tw_mostRepeatedValues = QTableWidget()
        self.tw_mostRepeatedValues.setColumnCount(2)
        self.tw_mostRepeatedValues.setHorizontalHeaderLabels(['Число', 'Количество повторений'])

        # self.lbl_maxValue = QLabel('Максимальное значение')
        # self.lbl_valuesCount = QLabel('Количество чисел')
        # self.le_digitMinValue = QLineEdit()
        # self.le_digitMinValue.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.le_digitMinValue.setValidator(QIntValidator(1, 999))
        # self.le_digitMaxValue = QLineEdit()
        # self.le_digitMaxValue.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.le_digitMaxValue.setValidator(QIntValidator(1, 999))
        # self.le_digitsCount = QLineEdit()
        # self.le_digitsCount.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # self.le_digitsCount.setValidator(QIntValidator(1, 999))
        self.pb_save = QPushButton('Загрузить')
        self.pb_save.clicked.connect(self.load)
        # self.pb_load = QPushButton('Загрузить')
        # self.pb_load.clicked.connect(self.load)
        # self.pb_generate = QPushButton('Сгенерировать')
        # self.pb_generate.clicked.connect(self.generate)

        self.lay_menuSettings.addWidget(self.lbl_filePath, 1, 1, 1, 1, Qt.AlignmentFlag.AlignCenter)
        # self.lay_menuSettings.addWidget(self.lbl_maxValue, 1, 2, 1, 1, Qt.AlignmentFlag.AlignCenter)
        # self.lay_menuSettings.addWidget(self.lbl_valuesCount, 1, 3, 1, 1, Qt.AlignmentFlag.AlignCenter)
        # self.lay_menuSettings.addWidget(self.le_digitMinValue, 2, 1, 1, 1, Qt.AlignmentFlag.AlignCenter)
        # self.lay_menuSettings.addWidget(self.le_digitMaxValue, 2, 2, 1, 1, Qt.AlignmentFlag.AlignCenter)
        # self.lay_menuSettings.addWidget(self.le_digitsCount, 2, 3, 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.lay_menuSettings.addWidget(self.pb_save, 1, 2, 1, 1, Qt.AlignmentFlag.AlignCenter)
        # self.lay_menuSettings.addWidget(self.pb_load, 2, 5, 1, 1, Qt.AlignmentFlag.AlignCenter)
        # self.lay_menuSettings.addWidget(self.pb_generate, 2, 6, 1, 1, Qt.AlignmentFlag.AlignCenter)

        self.lay_digits = QGridLayout()
        self.gb_digit = QGroupBox()
        self.gb_digit.setTitle('Аналитика')

        self.lay_digitsSurface = QGridLayout()
        self.gb_digit.setLayout(self.lay_digitsSurface)
        self.lay_digitsSurface.addWidget(self.tw_tickets)
        self.lay_digitsSurface.addWidget(self.tw_mostRepeatedValues)
        self.lay_digits.addWidget(self.gb_digit)

        self.lay_main.addLayout(self.lay_menuSettings)
        self.lay_main.addLayout(self.lay_digits)

        # self.list_pbDigits = list()
        self.df: pd.DataFrame = None

        self.show()

    def save(self):
        print('save')

    def load(self):
        try:
            file, _ = QFileDialog.getOpenFileName(self, 'Open File', './', "DB (*.xlsx *.xls *scv);;Text files (*.txt);;Any()")

            if file:
                self.lbl_filePath.setText(file)

                self.df = pd.read_excel(os.path.abspath(file), index_col=None)
                # df_copy = pd.to_datetime(self.df['Дата розыгрыша'])
                df_copy: pd.DataFrame = self.df.iloc[:, 1:9]
                df_copy.index = self.df['Дата розыгрыша']
                s_matchCount: pd.Series = None
                for column in df_copy:
                    if s_matchCount is None:
                        s_matchCount = pd.Series(df_copy[column].to_list())
                    else:
                        s_matchCount = pd.concat([s_matchCount, pd.Series(df_copy[column].to_list())], ignore_index=True)

                self.create_digitsRating(s_matchCount.value_counts())

                self.createNewTableFromDF(df_copy)

        except Exception as e:
            print(e)

    def createNewTableFromDF(self, df: pd.DataFrame):
        self.clearTable(self.tw_tickets)

        for i in range(df.index.__len__()):
            self.tw_tickets.insertRow(i)
            item = QTableWidgetItem(df.index[i].__str__())
            item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.tw_tickets.setItem(i, 0, item)
            for j in range(df.columns.__len__()):
                item = QTableWidgetItem(df.iloc[i][j].__str__())
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.tw_tickets.setItem(i, j + 1, item)

    def create_digitsRating(self, series: pd.Series):

        self.clearTable(self.tw_mostRepeatedValues)

        i = 0
        for index, val in series.items():
            # print(index, val)
            self.tw_mostRepeatedValues.insertRow(i)
            item_1 = QTableWidgetItem(index.__str__())
            item_1.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            item_2 = QTableWidgetItem(val.__str__())
            item_2.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.tw_mostRepeatedValues.setItem(i, 0, item_1)
            self.tw_mostRepeatedValues.setItem(i, 1, item_2)
            i += 1

    def clearTable(self, table):
        for i in range(table.rowCount()):
            table.removeRow(i)

    def generate(self):

        for i in reversed(range(self.lay_digitsSurface.count())):
            self.lay_digitsSurface.removeItem(self.lay_digitsSurface.itemAt(i))

        minValue = int(self.le_digitMinValue.text())
        maxValue = int(self.le_digitMaxValue.text())
        digitsCount = int(self.le_digitsCount.text())
        rr = np.arange(minValue, maxValue + 1)
        np.random.shuffle(rr)

        for i in range(minValue, maxValue, digitsCount):
            pb = QPushButton(rr[i:i+digitsCount].__str__())
            pb.setCheckable(True)
            pb.setStyleSheet('''
            :checked { background-color: red;}
            ''')
            self.lay_digitsSurface.addWidget(pb)
