import re
from datetime import datetime

class DataClass:
    def __init__(self, temperature, location, date):
        self.__temperature = temperature
        self.__location = location
        self.__date = date

    def get_temperature(self):
        return self.__temperature

    def get_location(self):
        return self.__location

    def get_date(self):
        return self.__date

    def __str__(self):
        if self.__temperature > 0:
            temperature_str = f"{self.__temperature:+g}"
        else:
            temperature_str = f"{self.__temperature:g}"
        return f"{temperature_str} °C; {self.__location}; {self.__date}"

    def __repr__ (self):
        return f"DataClass(temperature={self.__temperature}, location='{self.__location}', date='{self.__date}')"

def analyzefile(filename):
    items: list[DataClass] = []

    with open(filename, encoding="utf-8") as file:
        for line in file:
            temperature_match = re.search(r'(-?\+?\d+\.\d+)', line)
            location_match = re.search(r'"([^"]+)"', line)
            date_match = re.search(r'(\d{4}[-./]\d{2}[-./]\d{2}|\d{2}[-./]\d{2}[-./]\d{4})', line)

            if temperature_match and location_match and date_match:
                temperature_float = float(temperature_match.group(1))
                location = location_match.group(1)
                date_str = date_match.group(1)

                normalized_date = re.sub(r'[-./]', '.', date_str)

                try:
                    date_obj = datetime.strptime(normalized_date, '%Y.%m.%d').date()
                    weather_obj = DataClass(temperature_float, location, date_obj)
                    items.append(weather_obj)

                except ValueError:
                    print(f'Невалидная дата в строке: {line}')
            else:
                print(f'Не удалось распарсить строку: {line}')

    return items

if __name__ == '__main__':

    weather = analyzefile("temperatures.txt")

print('\n--- Фильтрация ---')
      user_date_str = input(
          'Введите дату для поиска в формате ДД.ММ.ГГГГ (например,'
          ' 25.10.2023): '
      ).strip()

      try:
        search_date = datetime.strptime(user_date_str, '%d.%m.%Y').date()

        filtered_items = [
            item for item in weather if item.get_date() == search_date
        ]

        if filtered_items:
          print(
              f'\nНайдено записей за {user_date_str}: {len(filtered_items)}'
          )
          for item in filtered_items:
            print(item)
        else:
          print(f'\nЗапрашиваемая дата ({user_date_str}) не найдена в данных.')

      except ValueError:
        print(
            'Ошибка: Неверный формат даты! Пожалуйста, используйте формат'
            ' ДД.ММ.ГГГГ.'
        )
