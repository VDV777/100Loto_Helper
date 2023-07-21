from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QIcon, QPixmap, QTransform
from PyQt6.QtWidgets import QPushButton, QWidget, QGridLayout


class PushButton_Circle_1(QPushButton):

    def __init__(self, text: str = '', parent: QWidget = None, size: int = 50, iconMarginIndent: int = 10, iconPath: str = '', isMirroredIcon: bool = False):
        super(PushButton_Circle_1, self).__init__(text, parent)

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.iconMarginIndent = iconMarginIndent

        self.setFixedWidth(size)
        self.setFixedHeight(size)

        self.setStyleSheet('PushButton_Circle_1'
                           '{'
                           "background-color: #00ffffff;"
                           "border-color: white;"
                           "border-width: 0px;"
                           "border-style: outset;"
                           f"border-radius: {self.width() / 2 - 1}px;"
                           '}'
                           'PushButton_Circle_1:hover'
                           '{'
                           "border-width: 2px;"
                           "border-color: yellow;"
                           "background-color: #00ffffff;"
                           '}'
                           'PushButton_Circle_1:pressed'
                           '{'
                           "border-width: 4px;"
                           "border-color: green;"
                           "background-color: #00ffffff;"
                           '}'
                           )

        if iconPath != '':
            pixmap = QPixmap(iconPath)
            if isMirroredIcon:
                pixmap = pixmap.transformed((QTransform().scale(-1, 1)))
            self.setIcon(QIcon(pixmap))
            self.setIconSize(QSize(self.width() - iconMarginIndent, self.width() - iconMarginIndent))

        self.show()

    def setBorderSettings(self, newColor_default: str = 'white', newColor_hover: str = 'yellow', newColor_pressed: str = 'green', borderSize_default: float = 1.0, borderSize_hover: float = 2.0, borderSize_pressed: float = 4.0) -> None:

        self.setStyleSheet(
           'PushButton_Circle_1'
           '{'
           f'border-color: {newColor_default};'
           "border-style: outset;"
           f"border-radius: {self.width() / 2 - 1}px;"
           '}'
           'PushButton_Circle_1:hover'
           '{'
           f'border-color: {newColor_hover};'
           f'border-width: {borderSize_hover}px;'
           '}'
           'PushButton_Circle_1:pressed'
           '{'
           f'border-color: {newColor_pressed};'
           f'border-width: {borderSize_pressed}px;'
           '}'
        )
