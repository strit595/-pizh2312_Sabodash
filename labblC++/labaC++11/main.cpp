#include <iostream>
#include <string>
#include <vector>
#include <list>
#include <algorithm>
#include <clocale>

class Контакт {
protected:
    std::string имя;
    std::string телефон;
    std::string адрес;

public:
    Контакт() : имя("Неизвестно"), телефон("Неизвестно"), адрес("Неизвестно") {}

    Контакт(const std::string& имя, const std::string& телефон, const std::string& адрес)
        : имя(имя), телефон(телефон), адрес(адрес) {
    }

    virtual ~Контакт() = default;

    std::string getИмя() const { return имя; }
    std::string getТелефон() const { return телефон; }
    std::string getАдрес() const { return адрес; }

    virtual void показать() const {
        std::cout << "Имя: " << имя << ", Телефон: " << телефон << ", Адрес: " << адрес;
    }

    virtual bool operator<(const Контакт& другой) const {
        return имя < другой.имя;
    }

    virtual bool operator>(const Контакт& другой) const {
        return имя > другой.имя;
    }
};

class РабочийКонтакт : public Контакт {
private:
    std::string должность;
    std::string компания;

public:
    РабочийКонтакт() : Контакт(), должность("Неизвестно"), компания("Неизвестно") {}

    РабочийКонтакт(const std::string& имя, const std::string& телефон, const std::string& адрес,
        const std::string& должность, const std::string& компания)
        : Контакт(имя, телефон, адрес), должность(должность), компания(компания) {
    }

    void показать() const override {
        Контакт::показать();
        std::cout << ", Должность: " << должность << ", Компания: " << компания;
    }

    bool operator<(const Контакт& другой) const override {
        const РабочийКонтакт* rc = dynamic_cast<const РабочийКонтакт*>(&другой);
        if (rc) {
            if (компания != rc->компания)
                return компания < rc->компания;
            return должность < rc->должность;
        }
        return Контакт::operator<(другой);
    }

    bool operator>(const Контакт& другой) const override {
        const РабочийКонтакт* rc = dynamic_cast<const РабочийКонтакт*>(&другой);
        if (rc) {
            if (компания != rc->компания)
                return компания > rc->компания;
            return должность > rc->должность;
        }
        return Контакт::operator>(другой);
    }
};

class ЛичныйКонтакт : public Контакт {
private:
    std::string датаРождения;
    std::string email;

public:
    ЛичныйКонтакт() : Контакт(), датаРождения("Неизвестно"), email("Неизвестно") {}

    ЛичныйКонтакт(const std::string& имя, const std::string& телефон, const std::string& адрес,
        const std::string& датаРождения, const std::string& email)
        : Контакт(имя, телефон, адрес), датаРождения(датаРождения), email(email) {
    }

    void показать() const override {
        Контакт::показать();
        std::cout << ", Дата рождения: " << датаРождения << ", Email: " << email;
    }

    bool operator<(const Контакт& другой) const override {
        const ЛичныйКонтакт* lc = dynamic_cast<const ЛичныйКонтакт*>(&другой);
        if (lc) {
            return датаРождения < lc->датаРождения;
        }
        return Контакт::operator<(другой);
    }

    bool operator>(const Контакт& другой) const override {
        const ЛичныйКонтакт* lc = dynamic_cast<const ЛичныйКонтакт*>(&другой);
        if (lc) {
            return датаРождения > lc->датаРождения;
        }
        return Контакт::operator>(другой);
    }
};

std::ostream& operator<<(std::ostream& os, const Контакт& контакт) {
    контакт.показать();
    return os;
}

int main() {
    setlocale(LC_ALL, "Russian");

    // 2. Создание контейнера vector с объектами пользовательского типа
    std::vector<Контакт*> контакты = {
        new ЛичныйКонтакт("Иван", "111", "ул. Ленина 1", "1990-01-01", "ivan@mail.ru"),
        new РабочийКонтакт("Петр", "222", "ул. Мира 5", "Директор", "ООО Ромашка"),
        new ЛичныйКонтакт("Анна", "333", "пр. Победы 10", "1985-05-15", "anna@gmail.com"),
        new РабочийКонтакт("Ольга", "444", "ул. Центральная 3", "Менеджер", "ООО Код"),
        new ЛичныйКонтакт("Сергей", "555", "ул. Лесная 7", "2000-11-20", "sergey@yandex.ru")
    };

    // 3. Сортировка по убыванию
    std::sort(контакты.begin(), контакты.end(),
        [](const Контакт* a, const Контакт* b) { return *a > *b; });

    // 4. Просмотр отсортированного контейнера
    std::cout << "=== Контакты после сортировки по убыванию ===\n";
    for (const auto& к : контакты) {
        std::cout << *к << std::endl;
    }

    // 5. Поиск элементов по условию (email содержит "mail")
    auto условие = [](const Контакт* к) {
        const ЛичныйКонтакт* lc = dynamic_cast<const ЛичныйКонтакт*>(к);
        return lc && lc->getИмя().find("н") != std::string::npos;
        };

    // 6. Создание второго контейнера (list) и перемещение элементов
    std::list<Контакт*> выбранные;
    auto it = std::partition(контакты.begin(), контакты.end(),
        [&условие](const Контакт* к) { return !условие(к); });

    выбранные.assign(it, контакты.end());
    контакты.erase(it, контакты.end());

    // 7. Просмотр второго контейнера
    std::cout << "\n=== Выбранные контакты ===\n";
    for (const auto& к : выбранные) {
        std::cout << *к << std::endl;
    }

    // 8. Сортировка обоих контейнеров по возрастанию
    std::sort(контакты.begin(), контакты.end(),
        [](const Контакт* a, const Контакт* b) { return *a < *b; });

    выбранные.sort([](const Контакт* a, const Контакт* b) { return *a < *b; });

    // 9. Просмотр отсортированных контейнеров
    std::cout << "\n=== Основные контакты (по возрастанию) ===\n";
    for (const auto& к : контакты) {
        std::cout << *к << std::endl;
    }

    std::cout << "\n=== Выбранные контакты (по возрастанию) ===\n";
    for (const auto& к : выбранные) {
        std::cout << *к << std::endl;
    }

    // Очистка памяти
    for (auto& к : контакты) delete к;
    for (auto& к : выбранные) delete к;

    // 10. Выводы
    std::cout << "\n=== Выводы ===\n";
    std::cout << "1. Использованы контейнеры vector (основной) и list (для выбранных элементов)\n";
    std::cout << "2. Реализована сортировка по убыванию и возрастанию с использованием операторов сравнения\n";
    std::cout << "3. Для поиска и перемещения элементов использованы алгоритмы partition и assign\n";
    std::cout << "4. Полиморфизм позволяет работать с разными типами контактов через базовый класс\n";

    return 0;
}