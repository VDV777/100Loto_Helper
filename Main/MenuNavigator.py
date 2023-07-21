

class MenuNavigator:

    START = 0
    ANALYTIC = 1

    def __init__(self):
        self.menu = self.START

    def nextMenu(self):

        if self.menu == self.ANALYTIC:
            self.menu = self.ANALYTIC
        else:
            self.menu += 1

    def previousMenu(self):
        if self.menu == self.START:
            self.menu = self.START
        else:
            self.menu -= 1

