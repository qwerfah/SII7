from user_interface import UserInterface
import pymorphy2

if __name__ == "__main__":
    analyzer = pymorphy2.MorphAnalyzer()

    print(analyzer.parse("")[0].normal_form)

    interface: UserInterface = UserInterface()
    interface.loop()
