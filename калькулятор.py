from fractions import Fraction

# --- Словари чисел и операций ---
numbers_dict = {
    "ноль": 0, "один": 1, "одна": 1, "два": 2, "две": 2, "три": 3, "четыре": 4,
    "пять": 5, "шесть": 6, "семь": 7, "восемь": 8, "девять": 9, "десять": 10,
    "одиннадцать": 11, "двенадцать": 12, "тринадцать": 13, "четырнадцать": 14,
    "пятнадцать": 15, "шестнадцать": 16, "семнадцать": 17, "восемнадцать": 18,
    "девятнадцать": 19, "двадцать": 20, "тридцать": 30, "сорок": 40,
    "пятьдесят": 50, "шестьдесят": 60, "семьдесят": 70, "восемьдесят": 80,
    "девяносто": 90, "сто": 100, 
}

# Словарь для порядковых числительных (для дробей)
fraction_words = {
    "перв": 1, "втор":2, "треть":3, "четвёрт":4, "пят":5, "шест":6, "седьм":7,
    "восьм":8, "девят":9, "десят":10, "одиннадцат":11, "двенадцат":12,
    "тринадцат":13, "четырнадцат":14, "пятнадцат":15, "шестнадцат":16,
    "семнадцат":17, "восемнадцат":18, "девятнадцат":19, "двадцат":20
}

# Список операций
operations_list = ["плюс", "минус", "умножить"]
numbers_dict_rev = {v: k for k, v in numbers_dict.items()}

# --- Парсинг числа ---
def words_to_number(words_list):
    total = 0
    for w in words_list:
        if w in numbers_dict:
            total += numbers_dict[w]
        else:
            raise ValueError(f"Неизвестное число: {w}")
    return total

# --- Очистка суффиксов у дробных слов ---
def clean_fraction_word(word):
    for suf in ["ая", "ых", "их", "ого", "ая", "ое"]:
        if word.endswith(suf):
            return word[:-len(suf)]
    return word

# --- Парсинг дроби ---
def parse_fraction(words):
    numerator = words_to_number([words[0]])
    denom_word = clean_fraction_word(words[1])
    
    if denom_word in fraction_words:
        denominator = fraction_words[denom_word]
    else:
        raise ValueError(f"Неизвестное дробное слово: {words[1]}")
    return numerator, denominator

# --- Парсинг числа или дроби ---
def parse_number(words):
    # Обрабатываем отрицательные числа
    while len(words) >= 2 and words[0] == "минус" and words[1] == "минус":
        words = words[2:]

    negative = False
    if words and words[0] == "минус":
        negative = True
        words = words[1:]

    if "и" in words:  # смешанная дробь
        i = words.index("и")
        whole = words_to_number(words[:i])
        numerator, denominator = parse_fraction(words[i+1:])
        frac = Fraction(whole,1) + Fraction(numerator, denominator)
    elif len(words) >= 2:
        # проверяем, что второе слово реально дробное
        denom_word = clean_fraction_word(words[1])
        if denom_word in fraction_words:
            numerator, denominator = parse_fraction(words)
            frac = Fraction(numerator, denominator)
        else:
            frac = Fraction(words_to_number(words), 1)
    else:
        frac = Fraction(words_to_number(words),1)
    
    return -frac if negative else frac


# --- Имя дроби с правильным окончанием ---
def fraction_name(denom, remainder=False):
    """
    Возвращает словесное имя знаменателя.
    remainder=False -> форма для полной дроби (напр. 'пятая')
    remainder=True  -> форма для остатка (напр. 'пятых')
    """
    # Малые номинатив/род (1..10 и 10)
    names = {
        1: ("первая","первых"),
        2: ("вторая","вторых"),
        3: ("третья","третьих"),
        4: ("четвёртая","четвёртых"),
        5: ("пятая","пятых"),
        6: ("шестая","шестых"),
        7: ("седьмая","седьмых"),
        8: ("восьмая","восьмых"),
        9: ("девятая","девятых"),
        10:("десятая","десятых"),
    }

    # если простой случай (до 10) — вернём готовую форму
    if denom in names:
        return names[denom][1] if remainder else names[denom][0]

    # разбиваем на десятки и единицы
    tens = (denom // 10) * 10
    ones = denom % 10

    # соберём части
    parts = []
    if tens > 0:
        # десятки: берём слово из numbers_dict_rev, иначе fallback на number_to_word
        tens_word = numbers_dict_rev.get(tens, number_to_word(tens))
        parts.append(tens_word)

    if ones > 0:
        # если единица маленькая — используем её порядковую форму
        if ones in names:
            ones_form = names[ones][1] if remainder else names[ones][0]
            parts.append(ones_form)
        else:
            # fallback: "три-ых"/"три-ая" — редко понадобится
            parts.append(number_to_word(ones) + ("-ых" if remainder else "-ая"))
        return " ".join(parts)

    # если единиц нет, например 20,30 — крепим окончание к десятку (приближённо)
    tens_word = parts[0] if parts else number_to_word(denom)
    return tens_word + ("ых" if remainder else "ая")




# --- Перевод дроби в слова ---
def fraction_to_words(frac: Fraction):
    frac = frac.limit_denominator()
    whole = frac.numerator // frac.denominator
    remainder = frac.numerator % frac.denominator

    words = []
    if whole != 0:
        words.append(number_to_word(whole))
    
    if remainder != 0:
        remainder_word = number_to_word(remainder)
        denom_word = fraction_name(frac.denominator, remainder=True)
        if whole != 0:
            words.append("и")
        words.append(f"{remainder_word} {denom_word}")
    
    if not words:  # если ни целого, ни остатка
        words.append("ноль")
    
    return " ".join(words)



# --- Перевод числа в слова ---
def number_to_word(n):
    if n < 0:
        return "минус " + number_to_word(-n)
    if n == 0:
        return "ноль"

    parts = []

    if n >= 100:
        hundreds = (n // 100) * 100
        if hundreds in numbers_dict_rev:
            parts.append(numbers_dict_rev[hundreds])
        n %= 100

    if n >= 20:
        tens = (n // 10) * 10
        if tens in numbers_dict_rev:
            parts.append(numbers_dict_rev[tens])
        n %= 10

    if 0 < n < 20:
        parts.append(numbers_dict_rev[n])

    return " ".join(parts)


# --- Вычисление выражения ---
def calc_expression(words):
    # Удаление "на"
    words = [w for w in words if w != "на"]

    # Обрабатываем ведущие минусы для первого числа
    first_num_sign = 1
    while words and words[0] == "минус":
        first_num_sign *= -1
        words = words[1:]

    # Находим первую операцию (которая не относится к ведущему минусу)
    op_index = None
    op = None
    for idx, w in enumerate(words):
        if w in operations_list:
            op_index = idx
            op = w
            break

    if op_index is None:  # Только число
        return parse_number(words) * first_num_sign

    # Левая часть — учитываем знак
    left = parse_number(words[:op_index]) * first_num_sign
    right = parse_number(words[op_index+1:])

    if op == "плюс":
        return left + right
    elif op == "минус":
        return left - right
    elif op == "умножить":
        return left * right



# --- Основной цикл ---
def run_calc():
    while True:
        user_input = input("Введите выражение: ").split()
        try:
            result = calc_expression(user_input)
            print("Итог:", fraction_to_words(result))
        except Exception as e:
            print("Ошибка:", e)
        cont = input("Еще раз? (да/нет): ").strip().lower()
        if cont in ["нет","н","не"]:
            print("Пока!")
            break

run_calc()