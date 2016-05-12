import os, sys, re
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from battery.ui.battery_ui import Ui_Dialog


class Main(QDialog, Ui_Dialog):

    def __init__(self):
        QDialog.__init__(self)
        self.setupUi(self)

        self.systray_icon = QIcon('icons/battery.png')
        self.systray = QSystemTrayIcon(self.systray_icon, self)
        menu = QMenu()
        hide = QAction('Hide', self)
        show = QAction('Show', self)
        close = QAction('Close', self)
        menu.addActions([hide, show, close])
        self.systray.setContextMenu(menu)
        self.systray.show()

        hide.triggered.connect(self.hide)
        show.triggered.connect(self.show)
        close.triggered.connect(self.close)

        timer = QTimer(self)
        self.connect(timer, SIGNAL("timeout()"), self, SLOT("update()"))
        self.connect(timer, SIGNAL("timeout()"), self.__battery_percentage)
        timer.start(1000)

    def __battery_percentage(self):
        command = os.popen('acpi').read()
        percentage = re.sub('%', '', re.search("\d+%", command).group())
        self.progressBar.setValue(int(percentage))

        if percentage < '20':
            self.alert_notification(percentage)
        elif percentage < '10':
            self.warning_notification(percentage)

    def alert_notification(self, percentage):
        pass

    def warning_notification(self, percentage):
        pass


def main():
    app = QApplication(sys.argv)
    dialog = Main()
    dialog.show()
    app.exec_()


if __name__ == '__main__':
    main()
