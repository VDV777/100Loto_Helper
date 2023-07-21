from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QGridLayout, QGroupBox, QSizePolicy, QPushButton

from CustomWidgets.Label.Label_1 import Label_1
from Main.MenuElements.Widget_Ticket import Widget_Ticket


class Widget_TicketInfo(QGroupBox):

    def __init__(self, parent: QWidget = None):
        super(Widget_TicketInfo, self).__init__(parent)

        self.__lay_main = QGridLayout()
        self.setLayout(self.__lay_main)

        self.__backgroundSetting = ''
        self.__fontSetting = ''
        self.__borderSetting = ''

        self.ticketPreview: Widget_Ticket = None

        self.__lbl_list_InfoText: list[Label_1] = []

        self.pb_addVariant = QPushButton('Добавить вариант')

        self.__setWidgetSettings()

    def __setWidgetSettings(self):

        self.setTitle('Информация о билете')
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFontSettings(newFontSize=12, newFontColor='white', newFontWeight=800, newFontName='Consolas')
        self.setBorderSettings(newColor_default='white', borderSize_default=1)

        self.show()

    def createWidget(self, sidesCount: int, valuesCountToGuess: list[int], maxValueOfDigits: list[int]):

        self.ticketPreview = Widget_Ticket(sidesCount, valuesCountToGuess, maxValueOfDigits)
        self.__lay_main.addWidget(self.ticketPreview, 0, 0, self.ticketPreview.sidesCount + 1, 1, Qt.AlignmentFlag.AlignCenter)
        self.__lay_main.addWidget(self.pb_addVariant, 3, self.ticketPreview.sidesCount + 1, 1, 1, Qt.AlignmentFlag.AlignCenter)

        self.__createTicketInfoText()

    def __createTicketInfoText(self):

        if self.ticketPreview is not None:

            for index, side in enumerate(self.ticketPreview.getSides()):

                lbl = Label_1()
                lbl.setFontSettings(12, 'white', 'Consolas', 800)
                lbl.setText('Количество комбинаций для стороны ' + index.__str__() + ': ' + side.combinationsCount().__str__())
                self.__lay_main.addWidget(lbl, index, self.ticketPreview.sidesCount + 1, 1, 1, Qt.AlignmentFlag.AlignCenter)
                self.__lbl_list_InfoText.append(lbl)

    def clearWidget(self):

        if self.ticketPreview is not None:
            self.__lay_main.removeWidget(self.ticketPreview)
            self.ticketPreview = None

        for lbl in self.__lbl_list_InfoText:
            self.__lay_main.removeWidget(lbl)
        self.__lbl_list_InfoText.clear()

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
