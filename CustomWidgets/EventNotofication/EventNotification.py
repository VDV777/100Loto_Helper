import threading

from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtCore import QSequentialAnimationGroup, QPropertyAnimation, QEasingCurve, Qt, QObject, QRect
from PyQt6.QtWidgets import QApplication


class Singleton(type(QObject), type):

    def __init__(cls, name, bases, dict):
        super().__init__(name, bases, dict)
        cls._instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class EventNotification(QWidget, metaclass=Singleton):

    def __init__(self):
        super().__init__()

        # get desktop size
        self.__desktopSizeWidth = QApplication.primaryScreen().size().width()
        self.__desktopSizeHeight = QApplication.primaryScreen().size().height()
        # set size params and type window
        self.setFixedSize(int(self.__desktopSizeWidth / 5), int(self.__desktopSizeHeight / 20))
        self.move(QApplication.primaryScreen().geometry().center().x() - self.geometry().center().x(), -self.geometry().height())
        self.setWindowFlags(Qt.WindowType.ToolTip | Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        # init label
        self.__eventInfo = "Hello World!!!"
        self.__lbl_info = QLabel(self)
        self.__lbl_info.setGeometry(0, 0, self.width(), self.height())
        self.__lbl_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.__lbl_info.setText(self.__eventInfo)
        self.__lbl_info.setStyleSheet('''
        QLabel
        {
        font: 24px Tahoma;
        border-style: solid;
        border-width: 1px;
        border-color: black;
        background-color: #20ff0000;
        }
        ''')
        # animations
        # анимация вниз
        self.__animation_lbl_info_down = QPropertyAnimation(self, b'geometry')
        self.__animation_lbl_info_down.setDuration(100)
        self.__animation_lbl_info_down.setStartValue(self.geometry())
        self.__animation_lbl_info_down.setEndValue(QRect(self.geometry().x(), self.geometry().y() + self.geometry().height(), self.geometry().width(), self.geometry().height()))
        self.__animation_curve_lbl_Info = QEasingCurve(QEasingCurve.Type.InCurve)
        self.__animation_lbl_info_down.setEasingCurve(self.__animation_curve_lbl_Info)
        # анимация вверх
        self.__animation_lbl_Info_up = QPropertyAnimation(self, b'geometry')
        self.__animation_lbl_Info_up.setDuration(3000)
        self.__animation_lbl_Info_up.setStartValue(QRect(self.geometry().x(), self.geometry().y() + self.geometry().height(), self.geometry().width(),self.geometry().height()))
        self.__animation_lbl_Info_up.setEndValue(self.geometry())
        # групповая анимация
        self.animation_group = QSequentialAnimationGroup()
        self.animation_group.addAnimation(self.__animation_lbl_info_down)
        self.animation_group.addAnimation(self.__animation_lbl_Info_up)
        #
        self.show()

    # @property.getter
    # def eventInfo(self) -> str:
    #     return self.__eventInfo
    #
    # @eventInfo.setter
    # def eventInfo(self, newValue: str) -> None:
    #     self.__eventInfo = newValue

    def animation_start(self, massage: str = 'Test', backgroundColor: str = '#5000ff00') -> None:

        self.__lbl_info.setText(massage)

        self.__lbl_info.setStyleSheet(
            'QLabel'
            '{'
            'font: 24px Tahoma;'
            'border-style: solid;'
            'border-width: 1px;'
            'border-color: black;'
            f'background-color: {backgroundColor};'
            '}'
        )

        self.animation_group.stop()
        self.animation_group.start()
