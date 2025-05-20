from abc import ABC, abstractmethod

# Класс для композиции: преобразование римских чисел
class RomanConverter:
    _roman_values = [
        ('M', 1000), ('CM', 900), ('D', 500), ('CD', 400),
        ('C', 100), ('XC', 90), ('L', 50), ('XL', 40),
        ('X', 10), ('IX', 9), ('V', 5), ('IV', 4), ('I', 1)
    ]

    @staticmethod
    def to_decimal(roman):
        if not roman or not isinstance(roman, str):
            raise ValueError("Invalid Roman numeral")
        result = 0
        i = 0
        for symbol, value in RomanConverter._roman_values:
            while i < len(roman) and roman.startswith(symbol, i):
                result += value
                i += len(symbol)
        if i != len(roman):
            raise ValueError("Invalid Roman numeral")
        return result

    @staticmethod
    def to_roman(decimal):
        if not isinstance(decimal, int) or decimal <= 0 or decimal >= 4000:
            raise ValueError("Decimal must be an integer between 1 and 3999")
        result = ""
        for symbol, value in RomanConverter._roman_values:
            while decimal >= value:
                result += symbol
                decimal -= value
        return result

# Абстрактный базовый класс
class AbstractNumber(ABC):
    @abstractmethod
    def __add__(self, other):
        pass

    @abstractmethod
    def __sub__(self, other):
        pass

    @abstractmethod
    def __mul__(self, other):
        pass

    @abstractmethod
    def __truediv__(self, other):
        pass

    @abstractmethod
    def get_value(self):
        pass

# Основной класс Roman
class Roman(AbstractNumber):
    def __init__(self, value):
        self.__converter = RomanConverter()  # Композиция
        self.__roman = self.__validate(value)
        self.__decimal = self.__converter.to_decimal(self.__roman)

    def __validate(self, value):
        if isinstance(value, str):
            # Проверяем, что строка — валидное римское число
            try:
                self.__converter.to_decimal(value)
                return value
            except ValueError:
                raise ValueError("Invalid Roman numeral")
        elif isinstance(value, int):
            if value <= 0 or value >= 4000:
                raise ValueError("Value must be between 1 and 3999")
            return self.__converter.to_roman(value)
        else:
            raise ValueError("Value must be a string or integer")

    # Инкапсуляция: геттеры
    @property
    def roman(self):
        return self.__roman

    @property
    def decimal(self):
        return self.__decimal

    def get_value(self):
        return self.__roman

    # Арифметические операции
    def __add__(self, other):
        if not isinstance(other, Roman):
            raise ValueError("Operand must be a Roman number")
        result = self.__decimal + other.decimal
        return Roman(result)

    def __sub__(self, other):
        if not isinstance(other, Roman):
            raise ValueError("Operand must be a Roman number")
        result = self.__decimal - other.decimal
        if result <= 0:
            raise ValueError("Roman numerals cannot be negative or zero")
        return Roman(result)

    def __mul__(self, other):
        if not isinstance(other, Roman):
            raise ValueError("Operand must be a Roman number")
        result = self.__decimal * other.decimal
        return Roman(result)

    def __truediv__(self, other):
        if not isinstance(other, Roman):
            raise ValueError("Operand must be a Roman number")
        if other.decimal == 0:
            raise ValueError("Division by zero")
        result = self.__decimal // other.decimal
        if result <= 0:
            raise ValueError("Roman numerals cannot be negative or zero")
        return Roman(result)

    # Полиморфизм: стандартные методы
    def __str__(self):
        return f"Roman({self.__roman})"

    def __eq__(self, other):
        if isinstance(other, Roman):
            return self.__decimal == other.decimal
        return False

    # Вызываемый метод
    def __call__(self, as_decimal=False):
        return self.__decimal if as_decimal else self.__roman

    # Статические методы для преобразований
    @staticmethod
    def to_decimal(roman):
        return RomanConverter.to_decimal(roman)

    @staticmethod
    def to_roman(decimal):
        return RomanConverter.to_roman(decimal)

# Производный класс для демонстрации наследования
class ExtendedRoman(Roman):
    def __init__(self, value, description=""):
        super().__init__(value)
        self.__description = description

    @property
    def description(self):
        return self.__description

    # Полиморфизм: переопределение
    def __str__(self):
        return f"ExtendedRoman({self.roman}, {self.__description})"

    def get_value(self):
        return f"{self.roman} ({self.__description})"

# Пример использования
if __name__ == "__main__":
    # Создание римских чисел
    num1 = Roman("X")  # 10
    num2 = Roman(5)    # V

    # Арифметические операции
    print(num1 + num2)  # Roman(XV)
    print(num1 - num2)  # Roman(V)
    print(num1 * num2)  # Roman(L)
    print(num1 / num2)  # Roman(II)

    # Вызов __call__
    print(num1())           # X
    print(num1(as_decimal=True))  # 10

    # Статические методы
    print(Roman.to_decimal("XII"))  # 12
    print(Roman.to_roman(17))       # XVII

    # Наследование и полиморфизм
    ext_num = ExtendedRoman("XX", "Twenty")
    print(ext_num)  # ExtendedRoman(XX, Twenty)
    print(ext_num.get_value())  # XX (Twenty)

    # Проверка равенства
    num3 = Roman("X")
    print(num1 == num3)  # True