from dialog_system.dialog_system import DialogSystem
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
        print("Здравствуйте, я – мини-ИИ для помощи в выборе " \
              "физической компьютерной памяти.\nДля начала работы " \
              "просто введите один из типовых запросов, например,\n" \
              "«Мне нужна оперативная память» или «Мне нужна память " \
              "с объемом носителя не менее 10 Тб».\nЧтобы узнать " \
              "подробнее, напишите «Помощь», или «Нужна помощь».")
