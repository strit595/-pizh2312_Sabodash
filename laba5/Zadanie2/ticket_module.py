from abc import ABC, abstractmethod
import json
import os
from datetime import datetime, timedelta

# Класс для композиции: Действие (логирование списания)
class Действие:
    def __init__(self, описание, время):
        self.__описание = описание
        self.__время = время

    @property
    def описание(self):
        return self.__описание

    @property
    def время(self):
        return self.__время

    def __str__(self):
        return f"[{self.__время}] {self.__описание}"

    def to_dict(self):
        return {"описание": self.__описание, "время": self.__время.isoformat()}

    @classmethod
    def from_dict(cls, data):
        return cls(data["описание"], datetime.fromisoformat(data["время"]))

# Абстрактный базовый класс
class Билет(ABC):
    def __init__(self, номер):
        self.__номер = номер
        self.__дата_активации = datetime.now()
        self.__история = []
        self._баланс = 0

    @property
    def номер(self):
        return self.__номер

    @property
    def дата_активации(self):
        return self.__дата_активации

    @property
    def история(self):
        return self.__история

    @abstractmethod
    def списать_поездку(self):
        pass

    def __str__(self):
        return f"Билет №{self.__номер}, активирован: {self.__дата_активации.strftime('%Y-%m-%d %H:%M')}"

    def to_dict(self):
        return {
            "тип": self.__class__.__name__,
            "номер": self.__номер,
            "дата_активации": self.__дата_активации.isoformat(),
            "история": [d.to_dict() for d in self.__история],
            "баланс": self._баланс
        }

# Наследуемый класс: ПроезднойБилет
class ПроезднойБилет(Билет):
    def __init__(self, номер):
        super().__init__(номер)
        self.__активен = True

    def списать_поездку(self):
        if self.__активен:
            self.__история.append(Действие("Поездка списана (неограниченный проезд)", datetime.now()))
            print(f"Билет №{self.номер}: Поездка списана. Проезд неограничен.")
            return True
        print(f"Билет №{self.номер}: Проездной неактивен.")
        return False

    def деактивировать(self):
        self.__активен = False
        self.__история.append(Действие("Проездной деактивирован", datetime.now()))
        print(f"Билет №{self.номер}: Деактивирован.")

    def __call__(self):
        return self.__активен

    def to_dict(self):
        data = super().to_dict()
        data["активен"] = self.__активен
        return data

    @classmethod
    def from_dict(cls, data):
        билет = cls(data["номер"])
        билет._Билет__дата_активации = datetime.fromisoformat(data["дата_активации"])
        билет._Билет__история = [Действие.from_dict(d) for d in data["история"]]
        билет._баланс = data["баланс"]
        билет.__активен = data["активен"]
        return билет

# Наследуемый класс: БилетОрганичением
class БилетОрганичением(Билет):
    def __init__(self, номер, срок_действия_дней):
        super().__init__(номер)
        # Используем свойство дата_активации вместо прямого доступа к __дата_активации
        self.__срок_действия = self.дата_активации + timedelta(days=срок_действия_дней)

    @property
    def срок_действия(self):
        return self.__срок_действия

    def списать_поездку(self):
        if datetime.now() <= self.__срок_действия:
            self.__история.append(Действие("Поездка списана (в пределах срока)", datetime.now()))
            print(f"Билет №{self.номер}: Поездка списана. Срок действия до {self.__срок_действия.strftime('%Y-%m-%d')}")
            return True
        print(f"Билет №{self.номер}: Срок действия истёк ({self.__срок_действия.strftime('%Y-%m-%d')})")
        return False

    def проверить_статус(self):
        status = "Активен" if datetime.now() <= self.__срок_действия else "Истёк"
        print(f"Билет №{self.номер}: Статус - {status}")
        return status

    def __call__(self):
        return datetime.now() <= self.__срок_действия

    def to_dict(self):
        data = super().to_dict()
        data["срок_действия"] = self.__срок_действия.isoformat()
        return data

    @classmethod
    def from_dict(cls, data):
        # Создаём объект с нулевым сроком, так как срок_действия будет установлен ниже
        билет = cls(data["номер"], 0)
        билет._Билет__дата_активации = datetime.fromisoformat(data["дата_активации"])
        билет._БилетОрганичением__срок_действия = datetime.fromisoformat(data["срок_действия"])
        билет._Билет__история = [Действие.from_dict(d) for d in data["история"]]
        билет._баланс = data["баланс"]
        return билет

# Наследуемый класс: БилетОрганичениемПоездок
class БилетОрганичениемПоездок(Билет):
    def __init__(self, номер, количество_поездок):
        super().__init__(номер)
        self.__количество_поездок = количество_поездок
        self._баланс = количество_поездок

    @property
    def количество_поездок(self):
        return self.__количество_поездок

    def списать_поездку(self):
        if self._баланс > 0:
            self._баланс -= 1
            self.__количество_поездок -= 1
            self.__история.append(Действие(f"Поездка списана, осталось {self._баланс}", datetime.now()))
            print(f"Билет №{self.номер}: Поездка списана. Осталось {self._баланс} поездок.")
            return True
        print(f"Билет №{self.номер}: Поездки закончились.")
        return False

    def обновить_баланс(self, value):
        if value >= 0:
            self._баланс = value
            self.__количество_поездок = value
            self.__история.append(Действие(f"Баланс обновлён до {value}", datetime.now()))
            print(f"Билет №{self.номер}: Баланс обновлён до {value} поездок.")
        else:
            raise ValueError("Баланс не может быть отрицательным")

    def __call__(self):
        return self._баланс > 0

    def __str__(self):
        return f"{super().__str__()}, Осталось поездок: {self._баланс}"

    def to_dict(self):
        data = super().to_dict()
        data["количество_поездок"] = self.__количество_поездок
        return data

    @classmethod
    def from_dict(cls, data):
        билет = cls(data["номер"], data["количество_поездок"])
        билет._Билет__дата_активации = datetime.fromisoformat(data["дата_активации"])
        билет._Билет__история = [Действие.from_dict(d) for d in data["история"]]
        билет._баланс = data["баланс"]
        билет.__количество_поездок = data["количество_поездок"]
        return билет

# Класс для управления базой данных билетов
class TicketDatabase:
    def __init__(self, filename="tickets_db.json"):
        self.__filename = filename
        self.__билеты = []
        self.__load()

    @property
    def билеты(self):
        return self.__билеты

    def __load(self):
        if os.path.exists(self.__filename):
            try:
                with open(self.__filename, "r", encoding="utf-8") as f:
                    data = json.load(f)
                for item in data:
                    if item["тип"] == "ПроезднойБилет":
                        билет = ПроезднойБилет.from_dict(item)
                    elif item["тип"] == "БилетОрганичением":
                        билет = БилетОрганичением.from_dict(item)
                    elif item["тип"] == "БилетОрганичениемПоездок":
                        билет = БилетОрганичениемПоездок.from_dict(item)
                    else:
                        continue
                    self.__билеты.append(билет)
                print(f"База данных загружена из {self.__filename}")
            except Exception as e:
                print(f"Ошибка загрузки базы данных: {e}")
                self.__билеты = []
        else:
            self.__save()
            print(f"Создана новая база данных: {self.__filename}")

    def __save(self):
        with open(self.__filename, "w", encoding="utf-8") as f:
            json.dump([билет.to_dict() for билет in self.__билеты], f, ensure_ascii=False, indent=4)
        print(f"База данных сохранена в {self.__filename}")

    def добавить_билет(self, билет):
        # Проверяем, есть ли билет с таким номером
        for b in self.__билеты:
            if b.номер == билет.номер:
                self.__билеты.remove(b)
                break
        self.__билеты.append(билет)
        self.__save()
        print(f"Билет №{билет.номер} добавлен в базу данных")

    def удалить_билет(self, номер):
        билет = self.найти_билет(номер)
        if билет:
            self.__билеты.remove(билет)
            self.__save()
            print(f"Билет №{номер} удалён из базы данных")
        else:
            print(f"Билет №{номер} не найден")

    def найти_билет(self, номер):
        for билет in self.__билеты:
            if билет.номер == номер:
                return билет
        return None

    def __str__(self):
        return f"База данных билетов ({len(self.__билеты)} билетов):\n" + "\n".join(str(б) for б in self.__билеты)