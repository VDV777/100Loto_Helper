import itertools

import pandas as pd
from PyQt6.QtWidgets import QWidget, QHBoxLayout
import pyqtgraph as pg


class Widget_PlotStatistic(QWidget):

    def __init__(self, parent: QWidget = None):
        super(Widget_PlotStatistic, self).__init__(parent)

        self.__lay_main: QHBoxLayout = QHBoxLayout()
        self.setLayout(self.__lay_main)

        self.__plot = pg.PlotWidget()
        self.__plot.setBackground('#333333')
        self.__lay_main.addWidget(self.__plot)

        self.__df_combinations: pd.DataFrame = pd.DataFrame(columns=['combination'], dtype=str)

    def add_combination(self, combination: str) -> None:

        self.__df_combinations = pd.concat([self.__df_combinations, pd.DataFrame(data=[{'combination': combination}], dtype=str)])

        listOfValues: list[int] = [int(num) for row in self.__df_combinations['combination'] for num in row.split(',')]

        # Вычисление частоты повторений значений
        values, counts = zip(*[(x, listOfValues.count(x)) for x in set(listOfValues)])
        bar_chart = pg.BarGraphItem(x=values, height=counts, width=0.5, brush='#6749d7', pen='white')
        # Создание экземпляра TextItem с текстом
        text_item = pg.TextItem(text='Всего выбрано комбинаций: ' + self.__df_combinations.__len__().__str__(), anchor=(0, 0), color=(255, 255, 255))
        # Создаем plot заново
        self.__plot.clear()
        self.__plot.addItem(bar_chart)
        self.__plot.addItem(text_item)

    def __update(self):

        if self.__df_combinations.empty:
            self.__plot.clear()
            return

        listOfValues: list[int] = [int(num) for row in self.__df_combinations['combination'] for num in row.split(',')]

        # Вычисление частоты повторений значений
        values, counts = zip(*[(x, listOfValues.count(x)) for x in set(listOfValues)])
        bar_chart = pg.BarGraphItem(x=values, height=counts, width=0.5, brush='#6749d7', pen='white')
        # Создание экземпляра TextItem с текстом
        text_item = pg.TextItem(text='Всего выбрано комбинаций: ' + self.__df_combinations.__len__().__str__(),
                                anchor=(0, 0), color=(255, 255, 255))
        # Создаем plot заново
        self.__plot.clear()
        self.__plot.addItem(bar_chart)
        self.__plot.addItem(text_item)

    def remove_combination(self, combination: str):

        self.__df_combinations = self.__df_combinations[self.__df_combinations['combination'] != combination]
        self.__update()

    def clear(self) -> None:

        self.__df_combinations = pd.DataFrame(columns=['combination'], dtype=str)
        self.__plot.clear()
