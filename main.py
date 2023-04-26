import sys

from PyQt6.QtWidgets import QApplication
from _100_LOTO import _100_LOTO

if __name__ == '__main__':

    qApp = QApplication(sys.argv)

    _100_loto = _100_LOTO()

    sys.exit(qApp.exec())
