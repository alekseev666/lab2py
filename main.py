from model.house import House
from model.report import create_report_word, create_report_excel
from model.database import Database

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
        value = input(text).strip()
        if value.isdigit() and int(value) > 0:
            return int(value)
        print("Введите целое число больше нуля")

def input_house():
    while True:
        try:
            h = House(input("Адрес дома: "))
            break
        except ValueError as e:
            print(e)
    for i in range(input_count("Количество квартир: ")):
        while True:
            try:
                f = h.add_flat(input_count(f"Номер квартиры {i + 1}: "))
                break
            except ValueError as e:
                print(e)
        for j in range(input_count(f"Количество комнат в квартире #{f.number}: ")):
            name = input(f"  Название комнаты {j + 1}: ")
            while not name.strip():
                name = input("  Название не может быть пустым, введите ещё раз: ")
            a = input_number("  Длина, м: ")
            b = input_number("  Ширина, м: ")
            f.add_room(name, a, b)
    return h

def demo_house():
    h = House("ул. Ленина, 5")
    f = h.add_flat(101)
    f.add_room("спальня", 4, 5)
    f.add_room("кухня", 3, 3)
    f = h.add_flat(102)
    f.add_room("студия", 5, 6)
    f = h.add_flat(103)
    f.add_room("гостиная", 5, 4)
    f.add_room("спальня", 4, 3.5)
    f.add_room("кухня", 3, 2.5)
    return h

def print_house(h):
    print(f"\nДом: {h.address}, квартир: {len(h)}")
    for f in h.flats:
        print(f"  {f}")
        for r in f.rooms:
            print(f"    {r}: {r.a:g} x {r.b:g} x {r.c:g} м")

def calculate(h, db):
    T_in = input_number("Температура в здании, °C: ", positive=False)
    T_out = input_number("Температура на улице, °C: ", positive=False)
    while T_out >= T_in:
        print("Температура на улице должна быть ниже, чем в здании")
        T_out = input_number("Температура на улице, °C: ", positive=False)
    K = input_number("Коэффициент рассеивания (0.6 - 4): ")
    while not 0.6 <= K <= 4:
        print("Коэффициент должен быть от 0.6 до 4")
        K = input_number("Коэффициент рассеивания (0.6 - 4): ")

    #Формула Q = (V * (T_in-T_out) * K)/860
    Q = h.heat_power(T_in, T_out, K)
    print()
    for f in h.flats:
        print(f"{f}: площадь {f.area():.1f} м², объём {f.volume():.1f} м³")
    print(f"Общая площадь помещения {h.area():.1f} м²")
    print(f"Тепловая мощность для обогрева помещения "
          f"{Q:.1f} кВт")
    calc_id = db.save(h, T_in, T_out, K)
    print(f"Расчёт сохранён в базу данных (№{calc_id})")

    print("\nСохранить отчёт: 1 - Word, 2 - Excel, 3 - оба, 0 - не сохранять")
    choice = input("Ваш выбор: ").strip()
    while choice not in ("0", "1", "2", "3"):
        choice = input("Введите 0, 1, 2 или 3: ").strip()
    if choice in ("1", "3"):
        print(f"Сохранён {create_report_word(h.area(), Q)}")
    if choice in ("2", "3"):
        print(f"Сохранён {create_report_excel(h, T_in, T_out, K)}")

def open_history(db):
    rows = db.history()
    if not rows:
        print("История пуста")
        return None
    print(f"\n{'№':>4}  {'Дата':<16}  {'Адрес':<25} {'Площадь':>10} {'Мощность':>10}")
    for calc_id, date, address, area, q in rows:
        print(f"{calc_id:>4}  {date:<16}  {address:<25} {area:>7.1f} м² {q:>6.1f} кВт")
    while True:
        value = input("\nНомер расчёта, чтобы открыть дом (0 - назад): ").strip()
        if value == "0":
            return None
        if value.isdigit():
            h = db.load_house(int(value))
            if h is not None:
                return h
        print("Нет такого расчёта")

def main():
    print("Расчёт площади и тепловой мощности помещений")
    with Database() as db:
        while True:
            print("\n1 - создать дом")
            print("2 - демонстрационный дом")
            print("3 - история расчётов")
            print("0 - выход")
            choice = input("Ваш выбор: ").strip()
            if choice == "1":
                h = input_house()
            elif choice == "2":
                h = demo_house()
            elif choice == "3":
                h = open_history(db)
                if h is None:
                    continue
            elif choice == "0":
                break
            else:
                print("Нет такого пункта")
                continue
            print_house(h)
            calculate(h, db)

if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход")
