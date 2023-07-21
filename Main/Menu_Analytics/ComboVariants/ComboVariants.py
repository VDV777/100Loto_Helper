from PyQt6.QtWidgets import QWidget, QGridLayout


class ComboVariants(QWidget):

    def __init__(self, parent: QWidget = None):
        super(ComboVariants, self).__init__(parent)

        self.__lay_main = QGridLayout()
        self.setLayout(self.__lay_main)

        self.__backgroundSetting = ''
        self.__fontSetting = ''
        self.__borderSetting = ''

    def setWidgetSettings(self):
        self.setMinimumSize(500, 500)

    def setBackgroundColor(self, newColorDefault: str = 'white') -> None:

        self.__backgroundSetting = str(
            f'{self.__class__.__name__}'
            '{'
            f'background-color: {newColorDefault};'
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
            f'{self.__class__.__name__}:title'
            '{'
            'subcontrol-origin: margin;'
            'subcontrol-position: top center;'
            'padding-left: -5px;'
            # 'padding-right: 10px;'
            '}'
        )

        self.setStyleSheet(self.__backgroundSetting + self.__fontSetting + self.__borderSetting)

    def setBorderSettings(self, newColor_default: str = 'white', borderSize_default: int = 1) -> None:

        self.__borderSetting = str(
            f'{self.__class__.__name__}'
            '{'
            f'border: {borderSize_default}px solid {newColor_default};'
            '}'
        )

        self.setStyleSheet(self.__backgroundSetting + self.__fontSetting + self.__borderSetting)