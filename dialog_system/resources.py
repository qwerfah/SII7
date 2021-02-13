from typing import List, Dict

from dialog_system.action_type import ActionType
from dialog_system.param_type import ParamType

action_synonyms: Dict[str, ParamType] = {
    "помощь": ActionType.Help,
    "помочь": ActionType.Help,
    "уметь": ActionType.Help,
    "мочь": ActionType.Help,
    "подсказать": ActionType.Help,
    "нужныйпомощь": ActionType.Help,
    "нужныйпомочь": ActionType.Help,

    "найти": ActionType.Search,
    "отыскать": ActionType.Search,
    "искать": ActionType.Search,
    "поиск": ActionType.Search,
    "нужныйнайти": ActionType.Search,
    "нужныйпамять": ActionType.Search,
    "необходимыйнайти": ActionType.Search,
    "необходимыйпамять": ActionType.Search,
    "требоватьсянайти": ActionType.Search,
    "требоватьсяпамять": ActionType.Search,
    "показать": ActionType.Search,
    "отобразить": ActionType.Search,
    "помочьнайти": ActionType.Search,
    "помочьотыскать": ActionType.Search,
    "помочьподобрать": ActionType.Search,

    "выйти": ActionType.Exit,
    "конец": ActionType.Exit,
    "завершение": ActionType.Exit,
    "завершить": ActionType.Exit,
    "выход": ActionType.Exit,
    "стоп": ActionType.Exit,
}

param_synonyms: Dict[str, ParamType] = {
    "объём": ParamType.Capacity,
    "ёмкость": ParamType.Capacity,
    "размер": ParamType.Capacity,
    "вместительность": ParamType.Capacity,

    "скорость": ParamType.Speed,

    "год": ParamType.Year,
    "годвыпуск": ParamType.Year,
    "годрелиз": ParamType.Year,

    "стоимость": ParamType.Cost,
    "цена": ParamType.Cost,

    "назначение": ParamType.Purpose,

    "тип": ParamType.Types,
}

unknown_messages: List[str] = [
    "Извините, не понял вас. Попробуйте задать другой вопрос.",
    "Простите, я вас не понимаю. Попытайтесь сформулировать запрос иначе.",
    "Прошу прощения, я вас не понимаю, повторите запрос.",
    "Ничего не понял, попробуйте спросить что-то другое.",
    "Не смог найти ответ на ваш вопрос, может что-то еще?",
    "Не нашел ни одного подходящего варианта ответа, спросите еще раз.",
    "Простите, я не настолько умный, не знаю что вам ответить.",
    "В if-else нет варианта, подходящего под ваш запрос (искусственный интеллект слишком искусственный)."
]

intro: str = "Здравствуйте, я – мини-ИИ для помощи в выборе " \
             "физической компьютерной памяти.\nДля начала работы " \
             "просто введите один из типовых запросов, например,\n" \
             "«Мне нужна оперативная память» или «Мне нужна память " \
             "с объемом носителя не менее 10 Тб».\nЧтобы узнать " \
             "подробнее, напишите «Помощь», или «Нужна помощь»."
