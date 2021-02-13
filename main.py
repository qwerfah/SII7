from user_interface import UserInterface
import pymorphy2
from typing import Dict, List, Tuple
from functools import reduce

if __name__ == "__main__":
    analyzer = pymorphy2.MorphAnalyzer()

    print(analyzer.parse("нужна")[0].normal_form)

    interface: UserInterface = UserInterface()
    interface.loop()
