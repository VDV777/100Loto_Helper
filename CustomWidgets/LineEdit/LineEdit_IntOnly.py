from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtGui import QDoubleValidator, QFocusEvent, QFontMetrics, QTextOption
from PyQt6.QtWidgets import QLineEdit, QWidget


class LineEdit_IntOnly(QLineEdit):

    def __init__(self, parent: QWidget = None):
        super(LineEdit_IntOnly, self).__init__(parent)

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setFocusPolicy(Qt.FocusPolicy.ClickFocus)  # Чтобы отображался placeholder text
        self.setStyleSheet(
            f'{self.__class__.__name__}'
            "{"
            "border: 1px solid #f2f2f2;"
            "border-radius: 10px;"
            "padding: 0 8px;"
            "background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #10ffffff, stop: 1 #10ffffff);"
            "font: 14px Tahoma;"
            "color: #f2f2f2;"
            "selection-background-color: 0x10ffffff;"
            "}"
            f'{self.__class__.__name__}:hover'
            "{"
            "background-color: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #1000FF00, stop: 1 #100000FF);"
            "}"
        )

        validator = QDoubleValidator()
        validator.setNotation(QDoubleValidator.Notation.StandardNotation)
        self.setValidator(validator)

        self.textChanged.connect(self.event_textChanged)

        self.setMaximumWidth(50)

    def leaveEvent(self, a0: QEvent) -> None:

        # self.clearFocus()

        return super(LineEdit_IntOnly, self).leaveEvent(a0)

    def event_textChanged(self, text: str) -> None:

        fm = QFontMetrics(self.font())
        tbr = fm.tightBoundingRect(text)
        self.setFixedWidth(tbr.width() + fm.__sizeof__())

