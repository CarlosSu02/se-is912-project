import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtWidgets import QApplication, QMenu, QWidget, QSystemTrayIcon


class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        QSystemTrayIcon.__init__(self, icon, parent)
        menu = QMenu(parent)
        exitAction = QAction(parent=menu, text="Exit")
        exitAction.triggered.connect(self.exit)

        menu.addAction(exitAction)
        self.setContextMenu(menu)

        self.activated.connect(
            lambda reason: print(reason == QSystemTrayIcon.ActivationReason.Trigger)
        )

    def exit(self):
        print("exit!")
        # self.exit()
        QApplication.quit()


def main():
    app = QApplication(sys.argv)

    w = QWidget()
    # trayIcon = QSystemTrayIcon(QIcon("Bomb.xpm"), w)
    trayIcon = SystemTrayIcon(QIcon("./icons/ds.ico"), w)
    # trayIcon.setIcon(QIcon("./icons/ds.ico"))

    trayIcon.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
