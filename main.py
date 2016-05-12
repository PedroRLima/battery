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
        self.connect(timer, SIGNAL("timeout()"), self.battery_percentage)
        timer.start(1000)

    def battery_percentage(self):
        command = os.popen('acpi').read()
        percentage = re.sub('%', '', re.search("\d+%", command).group())
        self.progressBar.setValue(percentage)


def main():
    app = QApplication(sys.argv)
    dialog = Main()
    dialog.show()
    app.exec_()


if __name__ == '__main__':
    main()
