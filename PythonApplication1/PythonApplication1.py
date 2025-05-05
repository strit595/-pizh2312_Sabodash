# -*- coding: utf-8 -*-
import sys
import io
from abc import ABC, abstractmethod
from typing import List, Literal, Tuple

# Настройка консоли для вывода русских символов (особенно для Windows)
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Абстрактный базовый класс для частей животного
class AnimalPart(ABC):
    """Абстрактный базовый класс для частей животного с общим поведением."""
    
    @abstractmethod
    def update_value(self, value: int) -> None:
        """Обновляет значение части животного в пределах допустимых границ."""
        pass

    @abstractmethod
    def get_value(self) -> int:
        """Возвращает текущее значение части животного."""
        pass

# Конкретная реализация для части пчелы
class Bee(AnimalPart):
    """Класс, представляющий компонент пчелы."""
    
    def __init__(self, value: int):
        self._value: int = max(0, min(value, 100))  # Инкапсуляция: приватный атрибут

    def update_value(self, value: int) -> None:
        """Обновляет значение пчелы, обеспечивая диапазон от 0 до 100."""
        self._value = max(0, min(self._value + value, 100))

    def get_value(self) -> int:
        """Возвращает текущее значение пчелы."""
        return self._value

# Конкретная реализация для части слона
class Elephant(AnimalPart):
    """Класс, представляющий компонент слона."""
    
    def __init__(self, value: int):
        self._value: int = max(0, min(value, 100))  # Инкапсуляция: приватный атрибут

    def update_value(self, value: int) -> None:
        """Обновляет значение слона, обеспечивая диапазон от 0 до 100."""
        self._value = max(0, min(self._value + value, 100))

    def get_value(self) -> int:
        """Возвращает текущее значение слона."""
        return self._value

# Основной класс с использованием композиции
class BeeElephant:
    """Класс, представляющий гибрид частей пчелы и слона."""
    
    def __init__(self, bee_part: int, elephant_part: int):
        """Инициализирует BeeElephant с частями пчелы и слона.
        
        Args:
            bee_part (int): Начальное значение для компонента пчелы.
            elephant_part (int): Начальное значение для компонента слона.
        """
        self._bee: AnimalPart = Bee(bee_part)  # Композиция: часть пчелы
        self._elephant: AnimalPart = Elephant(elephant_part)  # Композиция: часть слона

    def fly(self) -> bool:
        """Проверяет, может ли существо летать на основе значений пчелы и слона.
        
        Returns:
            bool: True, если значение пчелы не меньше значения слона, иначе False.
        """
        return self._bee.get_value() >= self._elephant.get_value()

    def trumpet(self) -> str:
        """Издает звук на основе значений слона и пчелы.
        
        Returns:
            str: 'tu-tu-doo-doo!', если значение слона не меньше значения пчелы,
                 'wzzzzz' в противном случае.
        """
        return "tu-tu-doo-doo!" if self._elephant.get_value() >= self._bee.get_value() else "wzzzzz"

    def eat(self, meal: Literal['nectar', 'grass'], value: int) -> None:
        """Кормит существо, корректируя значения пчелы и слона в зависимости от типа еды.
        
        Args:
            meal (Literal['nectar', 'grass']): Тип еды (нектар или трава).
            value (int): Количество потребляемой еды.
        """
        if meal == 'nectar':
            self._elephant.update_value(-value)
            self._bee.update_value(value)
        elif meal == 'grass':
            self._bee.update_value(-value)
            self._elephant.update_value(value)

    def get_parts(self) -> Tuple[int, int]:
        """Возвращает текущие значения частей пчелы и слона.
        
        Returns:
            Tuple[int, int]: Кортеж, содержащий (значение пчелы, значение слона).
        """
        return (self._bee.get_value(), self._elephant.get_value())

# Тестовая функция для проверки функциональности и вывода русских слов
def test_russian_output():
    """Тестирует функциональность класса BeeElephant и вывод русских слов."""
    print("Тест 1: Пчела и Слон")
    be = BeeElephant(3, 2)
    print(f"Может летать: {be.fly()}")
    print(f"Звук: {be.trumpet()}")
    be.eat('grass', 4)
    print(f"Части [пчела, слон]: {be.get_parts()}")

    print("\nТест 2: Гибрид с большим слоном")
    be2 = BeeElephant(13, 87)
    print(f"Может летать: {be2.fly()}")
    print(f"Звук: {be2.trumpet()}")
    be2.eat('nectar', 90)
    print(f"Звук после еды: {be2.trumpet()}")
    print(f"Части [пчела, слон]: {be2.get_parts()}")

if __name__ == "__main__":
    test_russian_output()