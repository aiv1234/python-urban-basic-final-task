import csv
from sys import stdout

TYPE_ERR = "Число этажей должно быть целым числом."
VALUE_ERR = "Число этажей должно быть положительным."
SMALL_HOUSE_MAX = 5
MEDIUM_HOUSE_MAX = 16


def read_file(filename: str) -> list[dict]:
    """Читает данные из CSV файла и преобразует их в список словарей.

    :param filename: Название файла, содержащего данные.
    :return: Список словарей с данными о домах.
    """
    houses = []
    with open(filename, encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            house = {}
            for key, value in row.items():
                if key in ("floor_count", "population"):
                    house[key] = int(value)
                elif key in ("heating_value", "area_residential"):
                    house[key] = float(value)
                else:
                    house[key] = value
            houses.append(house)
    return houses


def classify_house(floor_count: int) -> str:
    """Классифицирует дом на основе количества этажей.

    Проверяет, является ли количество этажей целым числом и положительным значением.
    Возвращает категорию дома в зависимости от количества этажей.

    :param floor_count: Количество этажей в доме.
    :return: Категория дома: "Малоэтажный", "Среднеэтажный" или "Многоэтажный".
    """
    if not isinstance(floor_count, int):
        raise TypeError(TYPE_ERR)
    if floor_count <= 0:
        raise ValueError(VALUE_ERR)

    if floor_count <= SMALL_HOUSE_MAX:
        result = "Малоэтажный"
    elif SMALL_HOUSE_MAX < floor_count <= MEDIUM_HOUSE_MAX:
        result = "Среднеэтажный"
    else:
        result = "Многоэтажный"

    return result


def get_classify_houses(houses: list[dict]) -> list[str]:
    """Классифицирует дома на основе количества этажей.

    :param houses: Список словарей с данными о домах.
    :return: Список категорий домов.
    """
    return [classify_house(int(row["floor_count"])) for row in houses]


def get_count_house_categories(categories: list[str]) -> dict[str, int]:
    """Подсчитывает количество домов в каждой категории.

    :param categories: Список категорий домов.
    :return: Словарь с количеством домов в каждой категории.
    """
    category_counts = {}
    for category in categories:
        if category in category_counts:
            category_counts[category] += 1
        else:
            category_counts[category] = 1
    return category_counts


def min_area_residential(houses: list[dict]) -> str:
    """Находит адрес с наименьшим средним количеством жилплощади на жильца.

    :param houses: Список словарей с данными о домах.
    :return: Адрес с наименьшим средним количеством жилплощади на жильца.
    """
    min_avg_area_per_person = float("inf")
    min_area_house = ""
    for house in houses:
        avg_area_per_person = house["area_residential"] / house["population"]
        if avg_area_per_person < min_avg_area_per_person:
            min_avg_area_per_person = avg_area_per_person
            min_area_house = house["house_address"]
    return min_area_house


if __name__ == "__main__":
    houses = read_file("housing_data.csv")
    classified_houses = get_classify_houses(houses)
    categories = set(classified_houses)
    category_counts = get_count_house_categories(list(categories))
    min_area_house = min_area_residential(houses)

    stdout.write("Категории домов и их количество в каждой:\n ")
    stdout.write(
        "; ".join([f"{row}: {category_counts[row]}" for row in category_counts]),
    )
    stdout.write(
        ".\nДом с наименьшим средним количеством жилплощадим на жильца: ",
    )
    stdout.write(f"{min_area_house}.")
