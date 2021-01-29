from dialog_system import DialogSystem


class UserInterface:
    dialog_system: DialogSystem

    def __init__(self, dialog_system: DialogSystem = None):
        if dialog_system is not None:
            self.dialog_system = dialog_system
        else:
            self.dialog_system = DialogSystem()

    def loop(self):
        pass