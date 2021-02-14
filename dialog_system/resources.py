from typing import List, Dict

from dialog_system.action_type import ActionType
from dialog_system.param_type import ParamType
from tree.memory_type import MemoryType

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
    "уходить": ActionType.Exit
}

param_synonyms: Dict[str, ParamType] = {
    "объём": ParamType.Capacity,
    "ёмкость": ParamType.Capacity,
    "размер": ParamType.Capacity,
    "вместительность": ParamType.Capacity,

    "скорость": ParamType.Speed,

    "год": ParamType.Year,
    "дата": ParamType.Year,

    "стоимость": ParamType.Cost,
    "цена": ParamType.Cost,

    "назначение": ParamType.Purpose,

    "тип": ParamType.Types,
    "вид": ParamType.Types,
    "для": ParamType.Types
}

purpose_synonyms: Dict[str, bool] = {
    "общий": True,
    "вторичный": True,

    "первичный": False,
    "специальный": False,
    "специализированный": False,
}

type_synonyms: Dict[str, MemoryType] = {
    "оперативный": MemoryType.RAM,
    "оз": MemoryType.RAM,

    "графический": MemoryType.GRAPHIC_MEMORY,
    "видео": MemoryType.GRAPHIC_MEMORY,
    "видеопамять": MemoryType.GRAPHIC_MEMORY,
    "видео-память": MemoryType.GRAPHIC_MEMORY,

    "микроконтроллер": MemoryType.MICRO_RAM,

    "кэш": MemoryType.CACHE_MEMORY,
    "кэш-память": MemoryType.CACHE_MEMORY,

    "хранение": MemoryType.SECONDARY_MEMORY,
    "жесткий": MemoryType.SECONDARY_MEMORY,
    "твердотельный": MemoryType.SECONDARY_MEMORY,
}

found_messages: List[str] = [
    "Вот, что я смог найти:\n",
    "Смотрите, что я нашел:\n",
    "Здесь все, что удалось найти по вашему запросу:\n",
    "На основании вашего запроса я нашел вот это:\n",
    "Это все, что мне удалось найти:\n"
]

not_found_messages: List[str] = [
    "Простите, ничего не смог найти по вашему запросу\n",
    "Извините, по запросу ничего не найдено\n",
    "Не нашел ничего из того, что вы искали\n",
    "Не смог найти ничего подходящего\n",
    "Ничего не найдено по вашему запросу\n",
]

exit_messages: List[str] = [
    "Завершение работы...",
    "Выключаюсь...",
    "До свиданья!",
    "Ухожу...",
    "Пока!",
    "Сворачиваемся..."
]

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
