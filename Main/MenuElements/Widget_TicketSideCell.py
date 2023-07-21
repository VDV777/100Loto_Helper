from PyQt6.QtCore import QObject, QEvent, Qt
from PyQt6.QtWidgets import QPushButton, QWidget


class Widget_TicketSideCell(QPushButton):

    def __init__(self, digit: int, parent: QWidget = None):
        super(Widget_TicketSideCell, self).__init__(parent)

        self.__digit = digit

        self.setText(digit.__str__())

        self.__fontSetting: str = ''
        self.__borderSetting: str = ''
        self.__backgroundSetting: str = ''

        self.__setWidgetSettings()

    def __setWidgetSettings(self):

        self.setMinimumSize(25, 25)
        self.installEventFilter(self)
        self.setCheckable(True)

    def setBackgroundColor(self, newColorDefault: str = 'white', newColorHover: str = 'grey', newColorChecked: str = 'green', newColorDisable: str = 'red', newColorPressed: str = 'green') -> None:

        self.__backgroundSetting = str(
            f'{self.__class__.__name__}'
            '{'
            f'background-color: {newColorDefault};'
            '}'
            f'{self.__class__.__name__}:hover'
            '{'
            f'background-color: {newColorHover};'
            '}'
            f'{self.__class__.__name__}:checked'
            '{'
            f'background-color: {newColorChecked};'
            '}'
            f'{self.__class__.__name__}:disabled'
            '{'
            f'background-color: {newColorDisable};'
            '}'
            f'{self.__class__.__name__}:pressed'
            '{'
            f'background-color: {newColorPressed};'
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
            '}'
        )

        self.setStyleSheet(self.__backgroundSetting + self.__fontSetting + self.__borderSetting)

    def setBorderSettings(self, newColor_default: str = 'white', newColor_hover: str = 'yellow', newColor_pressed: str = 'green', newColor_disable: str = 'red', newColor_checked: str = 'green',
                          borderSize_default: int = 1, borderSize_hover: int = 2, borderSize_pressed: int = 3, borderSize_disable: int = 1, borderSize_checked: int = 1) -> None:

        self.__borderSetting = str(
           f'{self.__class__.__name__}'
           '{'
           f'border: {borderSize_default}px solid {newColor_default};'
           '}'
           f'{self.__class__.__name__}:hover'
           '{'
           f'border: {borderSize_hover}px solid {newColor_hover};'
           '}'
           f'{self.__class__.__name__}:pressed'
           '{'
           f'border: {borderSize_pressed}px solid {newColor_pressed};'
           '}'
           f'{self.__class__.__name__}:disabled'
           '{'
           f'border: {borderSize_disable}px solid {newColor_disable};'
           '}'
           f'{self.__class__.__name__}:checked'
           '{'
           f'border: {borderSize_checked}px solid {newColor_checked};'
           '}'
        )

        self.setStyleSheet(self.__backgroundSetting + self.__fontSetting + self.__borderSetting)

    @property
    def digit(self) -> int:

        return self.__digit

    def eventFilter(self, obj: QObject, e: QEvent) -> bool:

        if e.type() == e.Type.MouseButtonRelease and e.button() == Qt.MouseButton.RightButton:

            if self.isEnabled():
                self.setChecked(False)
                self.setEnabled(False)
            else:
                self.setEnabled(True)

        return super(Widget_TicketSideCell, self).eventFilter(obj, e)
