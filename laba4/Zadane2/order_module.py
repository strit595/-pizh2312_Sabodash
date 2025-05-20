from abc import ABC, abstractmethod
import json
from datetime import datetime

# Класс для композиции: Товар
class Товар:
    def __init__(self, наименование, цена):
        self.__наименование = наименование
        self.__цена = float(цена)

    @property
    def наименование(self):
        return self.__наименование

    @property
    def цена(self):
        return self.__цена

    def __str__(self):
        return f"{self.__наименование} ({self.__цена} руб.)"

# Абстрактный базовый класс
class OrderEntity(ABC):
    @abstractmethod
    def рассчитать_стоимость(self):
        pass

# Основной класс Заказ
class Заказ(OrderEntity):
    def __init__(self, товары=None, статус="в обработке"):
        self.__товары = [] if товары is None else [Товар(t[0], t[1]) for t in товары]
        self.__статус = статус
        self.__общая_стоимость = self.__обновить_стоимость()
        self.__дата_создания = datetime.now()

    # Инкапсуляция: геттеры и сеттеры
    @property
    def товары(self):
        return self.__товары

    @property
    def общая_стоимость(self):
        return self.__общая_стоимость

    @property
    def статус(self):
        return self.__статус

    @статус.setter
    def статус(self, value):
        if value not in ["в обработке", "оплачен", "доставлен"]:
            raise ValueError("Недопустимый статус")
        self.__статус = value

    @property
    def дата_создания(self):
        return self.__дата_создания

    # Специальные методы
    def __str__(self):
        товары_список = "\n".join(f"- {т}" for т in self.__товары)
        return f"Заказ от {self.__дата_создания.strftime('%Y-%m-%d %H:%M')}\nСтатус: {self.__статус}\nТовары:\n{товары_список}\nОбщая стоимость: {self.__общая_стоимость} руб."

    def __eq__(self, other):
        if isinstance(other, Заказ):
            return self.__товары == other.товары and self.__статус == other.статус
        return False

    def __add__(self, other):
        if not isinstance(other, Заказ):
            raise ValueError("Can only add another Order")
        new_товары = self.__товары + other.товары
        return Заказ([(т.наименование, т.цена) for т in new_товары], self.__статус)

    def __sub__(self, other):
        if not isinstance(other, Заказ):
            raise ValueError("Can only subtract another Order")
        new_товары = [т for т in self.__товары if т not in other.товары]
        return Заказ([(т.наименование, т.цена) for т in new_товары], self.__статус)

    # Метод класса
    @classmethod
    def from_string(cls, str_value):
        lines = str_value.strip().split("\n")
        товары = []
        for line in lines[2:-1]:  # Пропускаем заголовок и стоимость
            name, price = line.split(" (")[0][2:], float(line.split("(")[1].split(" руб.)")[0])
            товары.append((name, price))
        return cls(товары, lines[1].split(": ")[1])

    # Вспомогательные методы
    def рассчитать_стоимость(self):
        return self.__обновить_стоимость()

    def __обновить_стоимость(self):
        self.__общая_стоимость = sum(т.цена for т in self.__товары)
        return self.__общая_стоимость

    def добавить_товар(self, наименование, цена):
        self.__товары.append(Товар(наименование, цена))
        self.__общая_стоимость = self.__обновить_стоимость()

    def удалить_товар(self, индекс):
        if 0 <= индекс < len(self.__товары):
            self.__товары.pop(индекс)
            self.__общая_стоимость = self.__обновить_стоимость()
        else:
            raise IndexError("Неверный индекс товара")

    # Сохранение и загрузка
    def save(self, filename):
        data = {
            "товары": [{"наименование": т.наименование, "цена": т.цена} for т in self.__товары],
            "статус": self.__статус,
            "дата_создания": self.__дата_создания.isoformat(),
            "общая_стоимость": self.__общая_стоимость
        }
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def load(self, filename):
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.__товары = [Товар(t["наименование"], t["цена"]) for t in data["товары"]]
        self.__статус = data["статус"]
        self.__дата_создания = datetime.fromisoformat(data["дата_создания"])
        self.__общая_стоимость = float(data["общая_стоимость"])

    # Вызываемый метод
    def __call__(self, наименование, цена):
        self.добавить_товар(наименование, цена)
        return f"Добавлен товар: {наименование} ({цена} руб.)"

# Наследование: расширенный класс
class ExtendedOrder(Заказ):
    def __init__(self, товары=None, статус="в обработке", скидка=0):
        super().__init__(товары, статус)
        self.__скидка = float(скидка)

    @property
    def скидка(self):
        return self.__скидка

    def рассчитать_стоимость(self):
        base_cost = super().рассчитать_стоимость()
        return base_cost * (1 - self.__скидка / 100)

    def __str__(self):
        return f"{super().__str__()}\nСкидка: {self.__скидка}%"