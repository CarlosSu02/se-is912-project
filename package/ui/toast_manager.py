from PyQt6.QtWidgets import QApplication
from pyqttoast import Toast, ToastPreset


# class Toasts(Toast):
#     # error = QSystemTrayIcon.MessageIcon.Critical
#
#     def __init__(self, content=None):
#         if content is None:
#             return
#         # super().__init__(icon=QIcon("./icons/ds.ico"))
#         super().__init__()
#         self.content = content
#         self.setDuration(5000)
#
#     # def tray_error(self, str):
#     # print("here!")
#     # self.showMessage("Error", str, self.error)
#
#     def error(self):
#         self.setTitle("Error")
#         self.setText(self.content)
#         self.applyPreset(ToastPreset.ERROR)
#         self.show()

# toast = Toast()
#
# toast.setDuration(5000)


# def toast_error(content):
#     toast = Toast()
#     toast.setDuration(5000)
#
#     toast.setTitle("Error")
#     toast.setText(str(content))
#     toast.applyPreset(ToastPreset.ERROR)
#     toast.show()


class ToastManager(Toast):
    def __init__(self):
        # if content is None:
        #     return
        # super().__init__(icon=QIcon("./icons/ds.ico"))
        super().__init__()
        # self.content = content
        self.setDuration(5000)

    # def tray_error(self, str):
    # print("here!")
    # self.showMessage("Error", str, self.error)

    def error(self, content):
        self.setTitle("Error")
        self.setText(str(content))
        self.applyPreset(ToastPreset.ERROR)
        self.show()


# toasts = ToastManager()
# toasts = None


def toasts():
    return ToastManager()
