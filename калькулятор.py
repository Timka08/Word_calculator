operations_list = ["умножить", "плюс", "минус", "делить"]

numbers_dict = {
    "ноль": 0, "один": 1, "одна": 1, "два": 2, 'две': 2, "три": 3, "четыре": 4, "пять": 5, "шесть": 6,
    "семь": 7, "восемь": 8, "девять": 9, "десять": 10, "одиннадцать": 11,
    "двенадцать": 12, "тринадцать": 13, "четырнадцать": 14, "пятнадцать": 15,
    "шестнадцать": 16, "семнадцать": 17, "восемнадцать": 18, "девятнадцать": 19,
    "двадцать": 20, "тридцать": 30, "сорок": 40, "пятьдесят": 50, "шестьдесят": 60,
    "семьдесят": 70, "восемьдесят": 80, "девяносто": 90, "сто": 100,
    "двести": 200, "триста": 300, "четыреста": 400, "пятьсот": 500,
    "шестьсот": 600, "семьсот": 700, "восемьсот": 800, "девятьсот": 900,
    "тысяча": 1000, "тысячи": 1000, "тысяч": 1000
}
def number_to_word(n):
    if n < 0:
        return "минус " + number_to_word(-n)
    if n == 0:
        return "ноль"
    if n in numbers_dict.values():
        for k, v in numbers_dict.items():
            if v == n:
                return k
    word = ""
    if n >= 1000:
        thousands, n = divmod(n, 1000)
        # правильные формы для "тысяча"
        if thousands == 1:
            word += "тысяча"
        elif thousands in [2]:
            word += "две тысячи"
        elif 3 <= thousands <= 4:
            word += number_to_word(thousands) + " тысячи"
        else:
            word += number_to_word(thousands) + " тысяч"
        if n > 0:
            word += " " + number_to_word(n)
        return word
    if n >= 100:
        hundreds, n = divmod(n, 100)
        word += number_to_word(hundreds*100)
        if n > 0:
            word += " " + number_to_word(n)
        return word
    if n >= 20:
        tens, ones = divmod(n, 10)
        word += number_to_word(tens*10)
        if ones > 0:
            word += " " + number_to_word(ones)
        return word
    return [k for k, v in numbers_dict.items() if v == n][0]


def words_to_number(words_list):
    if words_list is None:
        return 0
    total = 0
    current = 0
    negative = False
    i = 0
    while i < len(words_list):
        w = words_list[i]
        if isinstance(w, int):
            current += w
        elif w == "-":
            negative = True
        elif w in numbers_dict:
            # просто прибавляем, кроме "тысяча"
            if w == "тысяча" or w == "тысячи" or w == "тысяч":
                if current == 0:  # например, "тысяча" без множителя
                    current = 1
                total += current * 1000
                current = 0
            else:
                current += numbers_dict[w]
        else:
            print(f"Некорректное число: {w}")
            return None
        i += 1

    total += current
    return -total if negative else total


def clean_input(string_list):
    return [w for w in string_list if w != "на"]

def calc_expression(string_list):
    string_list = clean_input(string_list)
    string_list[0:1] = ["-" if w=="минус" else w for w in string_list[0:1]]
    string_list = [w for w in string_list]
    if not any(op in string_list for op in operations_list):
        return words_to_number(string_list) 
    while any(op in string_list for op in operations_list):
        index = -1
        op = ""
        for i, word in enumerate(string_list):
            if word in ["умножить", "делить"]:
                index = i
                op = word
                break
        if index == -1:
            for i, word in enumerate(string_list):
                if word in ["плюс", "минус"]:
                    index = i
                    op = word
                    break
        if index == -1:
            break

        left = words_to_number(string_list[:index])
        right = words_to_number(string_list[index+1:])
        if left is None or right is None:
            return None

        if op == "плюс":
            res = left + right
        elif op == "минус":
            res = left - right
        elif op == "умножить":
            res = left * right
        elif op == "делить":
            if right == 0:
                print("Ошибка: деление на ноль")
                return None
            q = left // right
            r = left % right
            if r != 0:
                print(f"Деление: {number_to_word(left)} / {number_to_word(right)} = {number_to_word(q)} (остаток {number_to_word(r)})")
            res = q

        string_list = [res]

    return string_list[0]  # возвращаем число

def process_brackets(string_list):
    string_list = clean_input(string_list)
    stack = []
    i = 0
    while i < len(string_list):
        if string_list[i] == "скобка" and i+1 < len(string_list) and string_list[i+1] == "открывается":
            stack.append(i)
            i += 2
        elif string_list[i] == "скобка" and i+1 < len(string_list) and string_list[i+1] == "закрывается":
            if not stack:
                print("Ошибка: нет открывающей скобки")
                return None
            start = stack.pop()
            end = i+1
            inner_list = string_list[start+2:end-1]
            inner_result = calc_expression(inner_list)
            if inner_result is None:
                return None
            del string_list[start:end+1]
            string_list.insert(start, inner_result)
            i = start
        else:
            i += 1

    final_result = calc_expression(string_list)
    if final_result is None:
        print("Ошибка в вычислениях")
        return None
    return number_to_word(final_result)

def run_calc():
    user_input = input("Введите выражение: ").split()
    result = process_brackets(user_input)
    if result is not None:
        print("Итог:", result)

run_calc()
