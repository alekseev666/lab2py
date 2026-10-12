from model.house import House
from model.report import create_report_word, create_report_excel

def input_number(text, positive=True):
    while True:
        try:
            value = float(input(text).replace(",", "."))
        except ValueError:
            print("Введите число")
            continue
        if positive and value <= 0:
            print("Число должно быть больше нуля")
            continue
        return value

def input_count(text):
    while True:
        value = input(text)
        if value.isdigit() and int(value) > 0:
            return int(value)
        print("Введите целое число больше нуля")

def input_house():
    h = House(input("Адрес дома: "))
    for i in range(input_count("Количество квартир: ")):
        f = h.add_flat(input_count(f"Номер квартиры {i + 1}: "))
        for j in range(input_count(f"Количество комнат в квартире #{f.number}: ")):
            name = input(f"  Название комнаты {j + 1}: ")
            a = input_number("  Длина, м: ")
            b = input_number("  Ширина, м: ")
            c = input_number("  Высота, м: ")
            f.add_room(name, a, b, c)
    return h

def main():
    h = input_house()

    T_in = input_number("Температура в здании, °C: ", positive=False)
    T_out = input_number("Температура на улице, °C: ", positive=False)
    K = input_number("Коэффициент рассеивания (0.6 - 4): ")

    #Формула Q = (V * (T_in-T_out) * K)/860
    Q = h.heat_power(T_in, T_out, K)
    print()
    for f in h.flats:
        print(f"{f}: площадь {f.total_area():.1f} м², объём {f.total_volume():.1f} м³")
    print(f"Общая площадь помещения {h.total_area():.1f} м²")
    print(f"Тепловая мощность для обогрева помещения "
          f"{Q:.1f} кВт")

    print("\nСохранить отчёт: 1 - Word, 2 - Excel, 3 - оба, 0 - не сохранять")
    choice = input("Ваш выбор: ")
    if choice in ("1", "3"):
        create_report_word(h.total_area(), Q)
        print("Сохранён Отчёт.docx")
    if choice in ("2", "3"):
        create_report_excel(h, T_in, T_out, K)
        print("Сохранён Отчёт.xlsx")

if __name__ == "__main__":
    main()
