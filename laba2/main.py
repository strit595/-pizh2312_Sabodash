from abc import ABC, abstractmethod
from datetime import datetime

# Класс для композиции
class Comment:
    def __init__(self, author, text):
        self.__author = author
        self.__text = text
        self.__timestamp = datetime.now()
    
    @property
    def author(self):
        return self.__author
    
    @property
    def text(self):
        return self.__text
    
    @property
    def timestamp(self):
        return self.__timestamp
    
    def __str__(self):
        return f"{self.__author} ({self.__timestamp:%Y-%m-%d %H:%M}): {self.__text}"

# Абстрактный базовый класс (абстракция)
class AbstractPost(ABC):
    @abstractmethod
    def add_like(self):
        pass
    
    @abstractmethod
    def add_comment(self, author, text):
        pass
    
    @abstractmethod
    def get_info(self):
        pass

# Основной класс Post (наследование, инкапсуляция, полиморфизм)
class Post(AbstractPost):
    def __init__(self, author, message):
        self.__author = author  # Приватный атрибут
        self._timestamp = datetime.now()  # Защищённый атрибут
        self.__likes = 0
        self.__message = message
        self.__comments = []  # Композиция: список объектов Comment
    
    # Геттеры и сеттеры для инкапсуляции
    @property
    def author(self):
        return self.__author
    
    @property
    def message(self):
        return self.__message
    
    @message.setter
    def message(self, new_message):
        if isinstance(new_message, str) and new_message.strip():
            self.__message = new_message
        else:
            raise ValueError("Message must be a non-empty string")
    
    @property
    def likes(self):
        return self.__likes
    
    @property
    def comments(self):
        return self.__comments
    
    # Реализация абстрактных методов
    def add_like(self):
        self.__likes += 1
    
    def add_comment(self, author, text):
        comment = Comment(author, text)  # Композиция
        self.__comments.append(comment)
    
    def get_info(self):
        return f"Post by {self.__author}: {self.__message} ({self.__likes} likes, {len(self.__comments)} comments)"
    
    # Полиморфизм: перегрузка стандартных методов
    def __str__(self):
        return f"[Post] {self.__author}: {self.__message} (Likes: {self.__likes})"
    
    def __eq__(self, other):
        if isinstance(other, Post):
            return self.__author == other.author and self.__message == other.message
        return False
    
    # Вызываемый метод
    def __call__(self, author, comment_text):
        self.add_comment(author, comment_text)
        return f"Comment added by {author}"

# Производный класс для спонсированных постов (наследование, полиморфизм)
class SponsoredPost(Post):
    def __init__(self, author, message, sponsor):
        super().__init__(author, message)
        self.__sponsor = sponsor
    
    @property
    def sponsor(self):
        return self.__sponsor
    
    # Полиморфизм: переопределение метода
    def get_info(self):
        return f"Sponsored Post by {self.author}: {self.message} (Sponsored by {self.__sponsor}, {self.likes} likes, {len(self.comments)} comments)"
    
    def __str__(self):
        return f"[SponsoredPost] {self.author}: {self.message} (Sponsor: {self.__sponsor}, Likes: {self.likes})"

# Пример использования
if __name__ == "__main__":
    # Создание постов
    post1 = Post("Alex", "Hello, world!")
    post2 = SponsoredPost("Maria", "Check out our product!", "CoolBrand")
    
    # Добавление лайков и комментариев
    post1.add_like()
    post1("Sasha", "Great post!")  # Использование __call__
    post2.add_like()
    post2.add_comment("Anna", "Nice ad!")
    
    # Вывод информации
    print(post1)  # [Post] Alex: Hello, world! (Likes: 1)
    print(post2)  # [SponsoredPost] Maria: Check out our product! (Sponsor: CoolBrand, Likes: 1)
    print(post1.get_info())  # Post by Alex: Hello, world! (1 likes, 1 comments)
    print(post2.get_info())  # Sponsored Post by Maria: Check out our product! (Sponsored by CoolBrand, 1 likes, 1 comments)
    
    # Проверка комментариев
    for comment in post1.comments:
        print(comment)  # Sasha (2025-05-18 14:20): Great post!
    
    # Проверка равенства (полиморфизм)
    post3 = Post("Alex", "Hello, world!")
    print(post1 == post3)  # True