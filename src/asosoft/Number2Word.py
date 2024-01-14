import re
# converts numerals into Central Kurdish words. It is useful in text-to-speech tools.

def Number2Word(text):
    # convert numbers to latin
    text = _latinize_numbers(text)
    # normalization steps
    text = re.sub("([0-9]{1,3})[,،](?=[0-9]{3})", r"\1", text)  # remove thousand separator 12,345,678 => 12345678
    text = re.sub("(?<![0-9])-([0-9]+)", r"ناقس \1", text)  # negative
    text = re.sub("(?<![0-9])% ?([0-9]+)", r"لە سەددا \1", text)  # percent sign before
    text = re.sub("([0-9]+) ?%", r"\1 لە سەد", text)  # percent sign after
    text = re.sub(r"\$ ?([0-9]+(\.[0-9]+)?)", r"\1 دۆلار", text)  # $ currency
    text = re.sub(r"£ ?([0-9]+(\.[0-9]+)?)", r"\1 پاوەن", text)  # £ currency
    text = re.sub(r"€ ?([0-9]+(\.[0-9]+)?)", r"\1 یۆرۆ", text)  # € currency

    # convert float numbers
    text = re.sub(r"([0-9]+)\.([0-9]+)", lambda m: _floatName(m.group(1), m.group(2)), text)

    # convert remaining integer numbers
    text = re.sub("([0-9]+)", lambda m: _integerName(m.group(1)), text)

    return text

_unifyNumbers = [
    r"٠|۰", "0",
    r"١|۱", "1",
    r"٢|۲", "2",
    r"٣|۳", "3",
    r"٤|۴", "4",
    r"٥|۵", "5",
    r"٦|۶", "6",
    r"٧|۷", "7",
    r"٨|۸", "8",
    r"٩|۹", "9"
]

def _latinize_numbers(text):
    for i in range(0, len(_unifyNumbers), 2):
        text = re.sub(_unifyNumbers[i], _unifyNumbers[i + 1], str(text))
    return text

def _floatName(integerPart, decimalPart):
    point = " پۆینت " + re.sub("((?<=0)0|^0)", " سفر ", decimalPart)
    point = re.sub("[0-9]", "", point)
    return _integerName(integerPart) + point + _integerName(decimalPart)

def _integerName(inputInteger):
    output = ""
    if inputInteger != "0":
        ones = ["", "یەک", "دوو", "سێ", "چوار", "پێنج", "شەش", "حەوت", "هەشت", "نۆ"]
        teens = ["دە", "یازدە", "دوازدە", "سێزدە", "چواردە", "پازدە", "شازدە", "حەڤدە", "هەژدە", "نۆزدە"]
        tens = ["", "", "بیست", "سی", "چل", "پەنجا", "شەست", "هەفتا", "هەشتا", "نەوەد"]
        hundreds = ["", "سەد", "دووسەد", "سێسەد", "چوارسەد", "پێنسەد", "شەشسەد", "حەوتسەد", "هەشتسەد", "نۆسەد"]
        thousands = ["", " هەزار", " ملیۆن", " ملیار", " تریلیۆن", " کوادرلیۆن", " کوینتیلیۆن"]
        temp = inputInteger
        for i in range(0, len(inputInteger), 3):
            currentThree = re.search("([0-9]{1,3})$", temp).group(1)
            temp = temp[:-len(currentThree)]
            currentThree = currentThree.zfill(3)
            C = int(currentThree[0])
            X = int(currentThree[1])
            I = int(currentThree[2])
            conjunction1 = " و " if (C != 0) and (X != 0 or I != 0) else ""
            conjunction2 = " و " if X != 0 and I != 0 else ""
            if X == 1:
                currentThree = hundreds[C] + conjunction1 + teens[I]
            else:
                currentThree = hundreds[C] + conjunction1 + tens[X] + conjunction2 + ones[I]
            M = thousands[int(i / 3)]
            currentThree += M if currentThree != "" else ""
            conjunction3 = "" if output == "" else " و "
            output = currentThree + conjunction3 + output if currentThree != "" else output
        output = output.replace("یەک هەزار", "هەزار")
    else:  # if input number = 0
        output = "سفر"
    return output