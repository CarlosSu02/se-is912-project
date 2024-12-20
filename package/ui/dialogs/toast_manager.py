from pyqttoast import Toast, ToastPreset


class ToastManager(Toast):
    def __init__(self):
        super().__init__()
        self.setDuration(5000)

    def error(self, content):
        self.setTitle("Error")
        self.setText(str(content))
        self.applyPreset(ToastPreset.ERROR)
        self.show()

    def info(self, content="info!"):
        self.setTitle("Info")
        self.setText(str(content))
        self.applyPreset(ToastPreset.INFORMATION)
        self.show()

    def success(self, content):
        self.setTitle("Confirmación")
        self.setText(str(content))
        self.applyPreset(ToastPreset.SUCCESS)
        # self.setFixedHeight(100)
        self.show()


# FIX: handle errors.
def toasts():
    return ToastManager()
