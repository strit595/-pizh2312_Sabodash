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

    std::string getДолжность() const { return должность; }
    std::string getКомпания() const { return компания; }
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

    std::string getДатаРождения() const { return датаРождения; }
    std::string getEmail() const { return email; }
};

int main() {
    setlocale(LC_ALL, "Russian");

    // 1. Создание и заполнение контейнера
    std::vector<Контакт*> контакты = {
        new ЛичныйКонтакт("Иван", "111", "ул. Ленина 1", "1990-01-01", "ivan@mail.ru"),
        new РабочийКонтакт("Петр", "222", "ул. Мира 5", "Директор", "ООО Ромашка"),
        new ЛичныйКонтакт("Анна", "333", "пр. Победы 10", "1985-05-15", "anna@gmail.com"),
        new РабочийКонтакт("Ольга", "444", "ул. Центральная 3", "Менеджер", "ООО Код"),
        new ЛичныйКонтакт("Сергей", "555", "ул. Лесная 7", "2000-11-20", "sergey@yandex.ru")
    };

    // 2. Сортировка по убыванию с использованием лямбда-функции
    std::sort(контакты.begin(), контакты.end(), [](const Контакт* a, const Контакт* b) {
        // Сначала сортируем по типу контакта
        bool aIsPersonal = dynamic_cast<const ЛичныйКонтакт*>(a) != nullptr;
        bool bIsPersonal = dynamic_cast<const ЛичныйКонтакт*>(b) != nullptr;

        if (aIsPersonal != bIsPersonal)
            return aIsPersonal > bIsPersonal; // Личные контакты сначала

        // Для личных контактов сортируем по дате рождения
        if (aIsPersonal) {
            auto lc1 = dynamic_cast<const ЛичныйКонтакт*>(a);
            auto lc2 = dynamic_cast<const ЛичныйКонтакт*>(b);
            return lc1->getДатаРождения() > lc2->getДатаРождения();
        }
        // Для рабочих контактов сортируем по компании, затем по должности
        else {
            auto rc1 = dynamic_cast<const РабочийКонтакт*>(a);
            auto rc2 = dynamic_cast<const РабочийКонтакт*>(b);
            if (rc1->getКомпания() != rc2->getКомпания())
                return rc1->getКомпания() > rc2->getКомпания();
            return rc1->getДолжность() > rc2->getДолжность();
        }
        });

    // 3. Просмотр отсортированного контейнера
    std::cout << "=== Контакты после сортировки по убыванию ===\n";
    std::for_each(контакты.begin(), контакты.end(), [](const Контакт* к) {
        к->показать();
        std::cout << std::endl;
        });

    // 4. Поиск элементов с использованием лямбда-функции
    auto условиеВыбора = [](const Контакт* к) {
        auto lc = dynamic_cast<const ЛичныйКонтакт*>(к);
        if (lc) {
            return lc->getEmail().find("mail") != std::string::npos;
        }
        return false;
        };

    // 5. Создание второго контейнера (list) и перемещение элементов
    std::list<Контакт*> выбранныеКонтакты;
    std::copy_if(контакты.begin(), контакты.end(), std::back_inserter(выбранныеКонтакты), условиеВыбора);

    // Удаление выбранных элементов из исходного контейнера
    контакты.erase(std::remove_if(контакты.begin(), контакты.end(), условиеВыбора), контакты.end());

    // 6. Просмотр второго контейнера
    std::cout << "\n=== Выбранные контакты (с email содержащим 'mail') ===\n";
    std::for_each(выбранныеКонтакты.begin(), выбранныеКонтакты.end(), [](const Контакт* к) {
        к->показать();
        std::cout << std::endl;
        });

    // 7. Сортировка обоих контейнеров по возрастанию с использованием лямбда-функций
    auto сортировкаПоВозрастанию = [](const Контакт* a, const Контакт* b) {
        return a->getИмя() < b->getИмя();
        };

    std::sort(контакты.begin(), контакты.end(), сортировкаПоВозрастанию);
    выбранныеКонтакты.sort(сортировкаПоВозрастанию);

    // 8. Просмотр отсортированных контейнеров
    std::cout << "\n=== Основные контакты (по возрастанию имен) ===\n";
    std::for_each(контакты.begin(), контакты.end(), [](const Контакт* к) {
        к->показать();
        std::cout << std::endl;
        });

    std::cout << "\n=== Выбранные контакты (по возрастанию имен) ===\n";
    std::for_each(выбранныеКонтакты.begin(), выбранныеКонтакты.end(), [](const Контакт* к) {
        к->показать();
        std::cout << std::endl;
        });

    // Очистка памяти
    std::for_each(контакты.begin(), контакты.end(), [](Контакт* к) { delete к; });
    std::for_each(выбранныеКонтакты.begin(), выбранныеКонтакты.end(), [](Контакт* к) { delete к; });

    // 9. Выводы
    std::cout << "\n=== Выводы ===\n";
    std::cout << "1. Все алгоритмы (сортировка, поиск, копирование) используют лямбда-функции\n";
    std::cout << "2. Лямбда-функции обеспечивают более гибкую и локальную логику сравнения и фильтрации\n";
    std::cout << "3. Использование лямбда-функций делает код более компактным и читаемым\n";
    std::cout << "4. Лямбда-функции позволяют легко адаптировать критерии сортировки и поиска\n";
    std::cout << "5. Сохранена полиморфная обработка разных типов контактов через dynamic_cast\n";

    return 0;
}