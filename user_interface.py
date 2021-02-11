from dialog_system.dialog_system import DialogSystem
import dialog_system.resources as resources

from accessify import private


class UserInterface:
    dialog_system: DialogSystem

    def __init__(self, dialog_system: DialogSystem = None):
        if dialog_system is not None:
            self.dialog_system = dialog_system
        else:
            self.dialog_system = DialogSystem()

    def loop(self) -> any:
        UserInterface.show_intro()

        while True:
            message = input("\nВведите сообщение: ")
            answer = self.dialog_system.answer(message)
            print(answer)

            if answer == "Завершение работы...":
                break

    @staticmethod
    def show_intro() -> str:
        print(resources.intro)
