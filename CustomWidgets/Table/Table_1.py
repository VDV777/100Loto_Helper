import pandas as pd
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTableWidget, QWidget, QHeaderView, QTableWidgetItem, QAbstractItemView


class Table_1(QTableWidget):

    def __init__(self, df: pd.DataFrame, parent: QWidget = None):
        super(Table_1, self).__init__(parent)

        self.__borderSetting: str = ''
        self.__fontSetting: str = ''
        self.__backgroundSetting: str = ''

        self.__df: pd.DataFrame = df.copy()
        self.__createNewTable()
        self.horizontalHeader().sectionDoubleClicked.connect(self.__e_column_sectionDoubleClicked)

        self.setSortingEnabled(True)
        self.horizontalHeader().setSortIndicatorShown(True)

        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.verticalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.horizontalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        self.verticalHeader().setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setCornerButtonEnabled(True)

        self.setEditableItems(False)

    def __createNewTable(self):

        self.clear()
        self.setColumnCount(self.__df.columns.__len__())
        self.setHorizontalHeaderLabels(self.__df.columns)

        for i in range(self.__df.index.__len__()):
            self.insertRow(i)
            for j in range(self.__df.columns.__len__()):
                item = QTableWidgetItem(self.__df.iloc[i][j].__str__())
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.setItem(i, j, item)

        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

    def editTable(self, df: pd.DataFrame) -> None:

        self.clear()
        self.__df = df

        self.clear()
        self.setColumnCount(self.__df.columns.__len__())
        self.setHorizontalHeaderLabels(self.__df.columns)

        for i in range(self.__df.index.__len__()):
            self.insertRow(i)
            for j in range(self.__df.columns.__len__()):
                item = QTableWidgetItem(self.__df.iloc[i][j].__str__())
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
                self.setItem(i, j, item)

        self.resizeColumnsToContents()
        self.resizeRowsToContents()

    def clear(self) -> None:
        for i in range(self.rowCount()):
            self.removeRow(i)

    def setEditableItems(self, bEdit: bool = True) -> None:

        if bEdit:
            self.setEditTriggers(QTableWidget.EditTrigger.AllEditTriggers)
        else:
            self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)

    def selectedOnlyRows(self, bFlag: bool = True) -> None:

        if bFlag:
            self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        else:
            self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectItems)

    def selectedOnlyColumns(self, bFlag: bool = True) -> None:

        if bFlag:
            self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectColumns)
        else:
            self.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectItems)

    @property
    def df(self) -> pd.DataFrame:
        return self.__df

    def __e_column_sectionDoubleClicked(self, columnID: int) -> None:
        # if self.horizontalHeader().sortIndicatorOrder()
        # self.sortByColumn(columnID, self.horizontalHeader().sortIndicatorOrder())
        # print(self.horizontalHeader().sortIndicatorOrder())
        ...

    def setBackgroundColor(self, newWidgetColor: str = 'white', newHeaderColor: str = 'white', newHeaderHoverColor: str = 'grey', newHeaderPressedColor: str = 'grey', newCellColor: str = 'white', newCellHoverColor: str = 'grey', newCellSelectedColor: str = 'grey', newCornerButtonColor: str = 'white') -> None:

        self.__backgroundSetting = str(

            f'{self.__class__.__name__}'
            '{'
            f'background-color: {newWidgetColor};'
            '}'
            
            f'{self.__class__.__name__} QHeaderView:section'
            '{'
            f'background-color: {newHeaderColor};'
            '}'
            f'{self.__class__.__name__} QHeaderView:section:hover'
            '{'
            f'background-color: {newHeaderHoverColor};'
            '}'
            f'{self.__class__.__name__} QHeaderView:section:pressed'
            '{'
            f'background-color: {newHeaderPressedColor};'
            '}'
            
            f'{self.__class__.__name__}:item'
            '{'
            f'background-color: {newCellColor};'
            '}'
            f'{self.__class__.__name__}:item:hover'
            '{'
            f'background-color: {newCellHoverColor};'
            '}'
            f'{self.__class__.__name__}:item:selected'
            '{'
            f'background-color: {newCellSelectedColor};'
            '}'

            f'{self.__class__.__name__} QTableCornerButton:section'
            '{'
            f'background-color: {newCornerButtonColor};'
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
            f'{self.__class__.__name__} QHeaderView:section'
            '{'
            f'font: {newFontSize}pt {newFontName};'
            f'color : {newFontColor};'
            f'font-weight: {newFontWeight};'
            f'text-align: {textAlign};'
            'margin-top: 1.0em;'
            '}'
        )

        self.setStyleSheet(self.__backgroundSetting + self.__fontSetting + self.__borderSetting)

    def setBorderSettings(self, widgetBorderColor: str = 'white', widgetBorderSize: int = 0, newCellsBorderColor: str = 'black', newCellsBorderSize: int = 0, newHeaderBorderColor: str = 'black', newHeaderBorderSize: int = 0) -> None:

        self.__borderSetting = str(
            f'{self.__class__.__name__}'
            '{'
            f'border: {widgetBorderSize}px solid {widgetBorderColor};'
            '}'
            f'{self.__class__.__name__}:item'
            '{'
            f'border: {newCellsBorderSize}px solid {newCellsBorderColor};'
            '}'
            f'{self.__class__.__name__} QHeaderView'
            '{'
            f'border: {newHeaderBorderSize}px solid {newHeaderBorderColor};'
            '}'
        )

        self.setStyleSheet(self.__backgroundSetting + self.__fontSetting + self.__borderSetting)
