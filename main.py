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
        bar = os.popen('acpi').read()
        print(bar)
        percentage = re.search('\d+%', bar)
        num = int(percentage.group(1))
        self.progressBar.setValue(num)

        if num == 20:
            self.systray.showMessage('Alert', 'Battery is {0}\n'
                                              'Please connect the charger'.format(num),
                                     QSystemTrayIcon.Warning)
        if num == 10:
            self.systray.showMessage('Alert', 'Battery is {0}\n'
                                              'Computer is going to turn off'.format(num),
                                     QSystemTrayIcon.Critical)







def main():
    app = QApplication(sys.argv)
    dialog = Main()
    dialog.show()
    app.exec_()

if __name__ == '__main__':
    main()