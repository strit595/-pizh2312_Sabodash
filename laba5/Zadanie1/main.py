from vector_collection_module import VectorCollection, ExtendedVectorCollection, Заказ

def main():
    print("Тестирование класса VectorCollection\n")

    # Создание объектов Заказ
    заказ1 = Заказ([("Пицца", 500), ("Кола", 100)])
    заказ2 = Заказ([("Бургер", 300)])

    # Создание коллекции
    collection = VectorCollection([заказ1, заказ2])
    print(f"Созданная коллекция:\n{collection}")

    # Индексация и срез
    print(f"Первый заказ: {collection[0]}")
    print(f"Срез (0:1):\n{collection[0:1]}")

    # Добавление и удаление
    print(collection.add(Заказ([("Чай", 50]))))
    print(f"После добавления:\n{collection}")
    print(collection.remove(1))
    print(f"После удаления:\n{collection}")

    # Сохранение и загрузка
    collection.save("collection.json")
    new_collection = VectorCollection()
    new_collection.load("collection.json")
    print(f"Загруженная коллекция:\n{new_collection}")

    # Вызываемый метод
    total_cost = collection()
    print(f"Общая стоимость всех заказов: {total_cost} руб.")

    # Наследование
    ext_collection = ExtendedVectorCollection([заказ1], max_size=2)
    print(f"Расширенная коллекция:\n{ext_collection}")
    print(ext_collection.add(заказ2))
    try:
        ext_collection.add(Заказ([("Вода", 30])))  # Превышение max_size
    except ValueError as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()