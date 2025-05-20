from abc import ABC, abstractmethod
import json
from datetime import datetime

# Класс Товар
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

    def to_dict(self):
        return {"наименование": self.__наименование, "цена": self.__цена}

    @classmethod
    def from_dict(cls, data):
        return cls(data["наименование"], data["цена"])

# Класс Заказ
class Заказ:
    def __init__(self, товары=None, статус="в обработке"):
        self.__товары = [] if товары is None else [Товар(t[0], t[1]) for t in товары]
        self.__статус = статус
        self.__общая_стоимость = self.__обновить_стоимость()
        self.__дата_создания = datetime.now()

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
        valid_statuses = ["в обработке", "оплачен", "доставлен"]
        if value not in valid_statuses:
            raise ValueError(f"Статус должен быть одним из {valid_statuses}")
        self.__статус = value

    @property
    def дата_создания(self):
        return self.__дата_создания

    def __обновить_стоимость(self):
        self.__общая_стоимость = sum(т.цена for т in self.__товары)
        return self.__общая_стоимость

    def __str__(self):
        товары_список = "\n".join(f"- {т}" for т in self.__товары)
        return (f"Заказ от {self.__дата_создания.strftime('%Y-%m-%d %H:%M')}\n"
                f"Статус: {self.__статус}\nТовары:\n{товары_список}\n"
                f"Общая стоимость: {self.__общая_стоимость} руб.")

    def to_dict(self):
        return {
            "товары": [т.to_dict() for т in self.__товары],
            "статус": self.__статус,
            "дата_создания": self.__дата_создания.isoformat(),
            "общая_стоимость": self.__общая_стоимость
        }

    @classmethod
    def from_dict(cls, data):
        z = cls()
        z.__товары = [Товар.from_dict(t) for t in data["товары"]]
        z.__статус = data["статус"]
        z.__дата_создания = datetime.fromisoformat(data["дата_создания"])
        z.__общая_стоимость = data["общая_стоимость"]
        return z

# Абстрактный базовый класс
class CollectionEntity(ABC):
    @abstractmethod
    def add(self, value):
        pass

    @abstractmethod
    def remove(self, index):
        pass

# Основной класс VectorCollection
class VectorCollection(CollectionEntity):
    def __init__(self, data=None):
        self.__data = [] if data is None else [self._validate_item(item) for item in data]
        print(f"Инициализация VectorCollection в {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    @property
    def data(self):
        return self.__data

    def _validate_item(self, item):
        if not isinstance(item, Заказ):
            raise ValueError("Элемент должен быть экземпляром класса Заказ")
        return item

    def __str__(self):
        return f"VectorCollection с {len(self.__data)} заказами:\n" + "\n".join(str(item) for item in self.__data)

    def __getitem__(self, key):
        if isinstance(key, slice):
            return VectorCollection(self.__data[key])
        if not (0 <= key < len(self.__data)):
            raise IndexError("Индекс вне диапазона")
        return self.__data[key]

    def add(self, value):
        self.__data.append(self._validate_item(value))
        print(f"Добавлен заказ в {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        return f"Добавлен заказ: {value}"

    def remove(self, index):
        if not (0 <= index < len(self.__data)):
            raise IndexError("Индекс вне диапазона")
        removed = self.__data.pop(index)
        print(f"Удалён заказ в {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        return f"Удалён заказ: {removed}"

    def save(self, filename):
        data = [item.to_dict() for item in self.__data]
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"Сохранено в {filename} в {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    def load(self, filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.__data = [Заказ.from_dict(item) for item in data]
            print(f"Загружено из {filename} в {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        except FileNotFoundError:
            print(f"Файл {filename} не найден в {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            self.__data = []

    def __call__(self):
        total = sum(item.общая_стоимость for item in self.__data)
        print(f"Общая стоимость рассчитана в {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        return total

# Наследование: расширенный класс
class ExtendedVectorCollection(VectorCollection):
    def __init__(self, data=None, max_size=10):
        super().__init__(data)
        self.__max_size = max_size
        print(f"Инициализация ExtendedVectorCollection с max_size={max_size} в {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    @property
    def max_size(self):
        return self.__max_size

    def add(self, value):
        if len(self.data) >= self.__max_size:
            raise ValueError(f"Превышен максимальный размер {self.__max_size}")
        return super().add(value)

    def __str__(self):
        return f"ExtendedVectorCollection (макс. {self.__max_size} заказов):\n" + super().__str__()