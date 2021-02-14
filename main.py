import pymorphy2

from user_interface import UserInterface

if __name__ == "__main__":
    analyzer = pymorphy2.MorphAnalyzer()

    print(analyzer.parse("")[0].normal_form)

    interface: UserInterface = UserInterface()
    interface.loop()
