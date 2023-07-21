from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QWidget


class Label_1(QLabel):

    def __init__(self, parent: QWidget = None):
        super(Label_1, self).__init__(parent)

        self.__fontSetting: str = ''
        self.__borderSetting: str = ''
        self.__backgroundSetting: str = ''

    def __setWidgetSettings(self):
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def setBackgroundColor(self, newColorDefault: str = 'white') -> None:

        self.__backgroundSetting = str(
            f'{self.__class__.__name__}'
            '{'
            f'background-color: {newColorDefault};'
            '}'
        )

        self.setStyleSheet(self.__backgroundSetting + self.__fontSetting + self.__borderSetting)

    def setBorderSettings(self, newColor_default: str = 'white', borderSize_default: int = 1, newRadius: float = 5) -> None:

        self.__borderSetting = str(
           f'{self.__class__.__name__}'
           '{'
           f'border: {borderSize_default}px solid {newColor_default};'
           '}'
           f'{self.__class__.__name__}'
           '{'
           f'border-radius: {newRadius}px;'
           '}'
        )

        self.setStyleSheet(self.__backgroundSetting + self.__fontSetting + self.__borderSetting)

    def setFontSettings(self, newFontSize: int = 14, newFontColor: str = 'black', newFontName: str = 'Consolas',
                        newFontWeight: int = 400, textAlign: str = 'center') -> None:

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
