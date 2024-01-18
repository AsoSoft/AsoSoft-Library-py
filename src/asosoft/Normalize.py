# Automated Kurdish Text Normalization  خاوێن کردنی ئۆتۆماتیکی دەقی کوردی
# Copyright (C) 2019 Aso Mahmudi, Hadi Veisi, Mohammad MohammadAmini, Hawre Hosseini
# Developer and Maintainer: Aso Mahmudi (aso.mehmudi@gmail.com)
#
# Source Code: https:#github.com/AsoSoft/AsoSoft-Library
# Paper: https:#www.researchgate.net/publication/333729065
# Cite:
#  @inproceedings{mahmudi2019automated,
#    title={Automated Kurdish Text Normalization},
#    author={Mahmudi, Aso and Veisi, Hadi and MohammadAmini, Mohammad and Hosseini, Hawre},
#    booktitle={The Second International Conference on Kurdish and Persian Languages and Literature},
#    year={2019}
#  }

import regex as re
import html

def replace_by_list(text, replace_list):
    for pattern, replacement in replace_list:
        text = re.sub(pattern, replacement, text)
    return text

KU = "ئابپتجچحخدرڕزژسشعغفڤقکگلڵمنوۆەهھیێأإآثذصضطظكيىةڎۊؤ" + "\u064B-\u065F"
JOINERS = "ئبپتثجچحخسشصضطظعغفڤقکكگلڵمنیيهھێ"

normalization_replaces = {
    "NormalizeKurdish1": [
        #========= Tatweels (U+0640)
        "\u0640{2,}", "\u0640", # merge
        rf"(?<=[{JOINERS}])\u0640(?=[{KU}])", "", # delete unnecessary tatweel e.g. هـا to ها
        # replace tatweel nonadjacent to Kurdish letters with dash
        rf"(?<=[{JOINERS}])\u0640", "\uF640", # temporal preserve
        rf"\u0640(?=[{KU}])", "\uF640", # temporal preserve
        "\u0640", "-",
        "\uF640", "\u0640",

        #========= Zero-Width Non-Joiner
        "[\uFEFF\u200C]+", "\u200C", #Standardize and remove dublicated ZWNJ
        # remove unnecessary ZWNJ
        r"‌(?=(\s|\p{P}|$))", "",    # ZWNJ + white spaces
        rf"(?<![{JOINERS}])\u200C", "", # rmove after non-joiner letter: سەرzwnjزل

        #========= Zero-Width Joiner (U+200D)
        "\u200D{2,}", "\u200D", # merge
        "ه" + "\u200D", "هـ",   # final Heh, e.g. ماه‍  => ماهـ
        f"(?<![{JOINERS}])\u200D(?![{JOINERS}])", "", #remove unnecessary ZW-J
    ],
    "NormalizeKurdish2": [
        #========= standard H, E, Y, K
        "ه" + "\u200C", "ە",    # Heh+ZWNJ =>  kurdish AE
        "ه" + f"(?=([^{KU}ـ]|$))", "ە",   #final Heh looks like Ae
        "ھ" + f"(?=([^{KU}]|$))", "هـ",   # final Heh Doachashmee
        "ھ" , "ه",  # non-final Heh Doachashmee
        "ى|ي", "ی",  # Alef maksura | Arabic Ye => Farsi ye
        "ك", "ک",  # Arabic Kaf => Farsi Ke
        "\u200C" + "و ", " و ", # شوێن‌و جێ => شوێن و جێ

        #========= errors from font conversion
        "لاَ|لاً|لأ", "ڵا",
        "(ی|ێ)" + "[\u064E\u064B]+", "ێ",  #FATHA & FATHATAN
        "(و|ۆ)" + "[\u064E\u064B]+", "ۆ",
        "(ل|ڵ)" + "[\u064E\u064B]+", "ڵ",
        "(ر|ڕ)" + "\u0650+", "ڕ", #KASRA
    ],
    "NormalizeKurdish3": [
            f"(?<![{KU}])" + "ر" + f"(?=[{KU}])", "ڕ", # initial R
            f"(?<![{KU}])" + "وو" + "(?=[ئبپتجچحخدرڕزژسشعغفڤقکگلڵمنهھی])", "و", # inintial WU
    ],
    "AliK2Unicode": [
            "لاَ|لآ|لاً", "ڵا",
            "لً|لَ|لأ", "ڵ",
            "ة", "ە",
            "ه" + "(?!([ئابپتجچحخدرڕزژسشعغفڤقکگلڵمنوۆەهھیێأإآثذصضطظكيىةڎۊؤ]|$))", "هـ",
            "ض", "چ",
            "ث", "پ",
            "ظ", "ڤ",
            "ط", "گ",
            "ك", "ک",
            "ىَ|يَ|یَ|آ", "ێ",
            "رِ", "ڕ",
            "ؤ|وَ", "ۆ",
            "ي|ى", "ی",
            "ء", "\u200Cو",
            "ِ", "",
            "ذ", "ژ"
    ],
    "AliWeb2Unicode": [
            "لاَ|لآ|لاً", "ڵا",
            "لَ|پ", "ڵ",
            "ة", "ە",
            "ه", "ھ",
            "ه", "ھ",
            "رِ|أ", "ڕ",
            "ؤ|وَ", "ۆ",
            "يَ|یَ", "ێ",
            "ص", "ێ",
            "ي", "ی",
            "ط", "ڭ", #swap ط and گ
            "گ", "ط", #
            "ڭ", "گ", #
            "ض", "چ",
            "ث", "پ",
            "ظ", "ڤ",
            "ْ|ُ", "",
            "ى", "*",
            "ك", "ک",
            "ذ", "ژ"
    ],
    "Dylan2Unicode": [
            "لإ|لأ|لآ", "ڵا",
            "ؤ|وَ", "ۆ",
            "ة", "ە",
            "ض", "ڤ",
            "ص", "ڵ",
            "ث", "ێ",
            "ؤ", "ۆ",
            "ه", "ھ",
            "ك", "ک",
            "ي|ى", "ی",
            "ذ", "ڕ"
    ],
    "Zarnegar2Unicode": [
            "لاٌ", "ڵا",
            "ى|ي", "ی",
            "یٌ", "ێ",
            "ه\u200C", "ە",
            "لٌ", "ڵ",
            "رٍ", "ڕ",
            "وٌ", "ۆ"
    ],
    "SeperateDigits": [
            r"(?<![ \t\d\-+.])(\d)", r" \1",
            r"(\d)(?![ \t\d\-+.])", r"\1 ",
            r"(\d) (ی|یەم|) ", r"\1\2 " # Izafe (12y mang)
    ],
    "NormalizePunctuations1": [
            r"\(\(", "«",
            r"\)\)", "»",
            "»", "\uF8FA", # temp replacement «x»eke
            r"\)", "\uF8FB", #temp replacement
            "([!.:;?،؛؟]+)(\p{Pi})", r"\1 \2",
            r"(\p{P}+)(?![\s\p{P}])", r"\1 ",   # Seprate all punctuations
            r"\uF8FA", "»", # undo temp replacement
            r"\uF8FB", ")", # undo temp replacement
            r"(?<![ \t\p{P}])(\p{P}+)", r" \1",   # Seprate all punctuations
            r"(\d) ([.|\u066B]) (?=\d)", r"\1\2",    #DECIMAL SEPARATOR
            r"(\d) ([,\u066C]) (?=\d\d\d)", r"\1\2", #THOUSANDS SEPARATOR
            r"(\d) ([/\u060D]) (?=\d)", r"\1\2" #DATE SEPARATOR
    ],
    "NormalizePunctuations2": [
            " ((\p{Pe}|\p{Pf})+)", r"\1",   # A ) B  => A) B
            "((\p{Ps}|\p{Pi})+) ", r"\1",   # A ( B  => A (B
            " ([!.:;?،؛؟]+)", r"\1",    # A !  => A!
    ],
    "NormalizePunctuations3": [
            r"(?<![ \t\p{P}])(\uF8FD)", r" \1",   # A" B  => A " B
            r"(\uF8FD)(?![ \t\p{P}])", r"\1 ",   # A "B  => A " B
    ]
}


# ================= Normalization =================
def load_normalizer_replaces(file):
    output = {}

    items = file.strip().split('\n')
    for i in range(1, len(items)):
        item = items[i].split(',')
        ch_old = chr(int(item[0], 16))
        ch_new = ''.join(chr(int(ch, 16)) for ch in item[1].split() if ch != "")
        if ch_old not in output:
            output[ch_old] = ch_new

    return output

deep_replacements = load_normalizer_replaces("resources/NormalizeUnicodeDeep.csv")
additional_replacements = load_normalizer_replaces("resources/NormalizeUnicodeAdditional.csv")

# Unicode Normalization for Central Kurdish
def Normalize(text, isOnlyKurdish=True, changeInitialR=True, deepUnicodeCorrectios=True, additionalUnicodeCorrections=True, usersReplaceList=None):
    if usersReplaceList is None:
        usersReplaceList = {}

    replaces = {}

    # Character-based replacement (ReplaceList and Private Use Area)
    char_list = list(set(text))

    if deepUnicodeCorrectios:
        for item in deep_replacements:
            if item[0] in char_list:
                replaces[item[0]] = item[1]

    if additionalUnicodeCorrections:
        for item in additional_replacements:
            if item[0] in char_list and item[0] not in replaces:
                replaces[item[0]] = item[1]

    for item in usersReplaceList.items():
        if item[0] in char_list and item[0] not in replaces:
            replaces[item[0]] = item[1]

    for ch in char_list:
        if ch in replaces:  # ReplaceList
            text = text.replace(ch, replaces[ch])
        elif 57343 < ord(ch) < 63744:  # Private Use Area
            text = text.replace(ch, '□')  # u25A1 White Square

    text = _replaceByList(text, normalization_replaces["NormalizeKurdish1"])

    # if the text is Monolingual (only Central Kurdish)
    if isOnlyKurdish:
        text = _replaceByList(text, normalization_replaces["NormalizeKurdish2"])

        # Initial r
        if changeInitialR:
            text = _replaceByList(text, normalization_replaces["NormalizeKurdish3"])

    return text


# Seperate digits from words (e.g. replacing "12a" with "12 a")
def SeperateDigits(text):
    return _replaceByList(text, normalization_replaces["SeperateDigits"])

# Normalize Punctuations
def NormalizePunctuations(text, seprateAllPunctuations):
    text = text.replace('"', "\uF8FD")  # temp replacement
    text = _replaceByList(text, normalization_replaces["NormalizePunctuations1"])
    if not seprateAllPunctuations:
        text = _replaceByList(text, normalization_replaces["NormalizePunctuations2"])
    else:
        text = _replaceByList(text, normalization_replaces["NormalizePunctuations3"])
    text = text.replace("\uF8FD", '"')  # undo temp replacement
    return text

# Trim white spaces of a line
def TrimLine(line):
    line = re.sub("[\u200B\u200C\uFEFF]+$", "", line.strip())
    line = re.sub("^[\u200B\u200C\uFEFF]+", "", line.strip())
    return line.strip()

# HTML Entity replacement for web crawled texts (e.g. "&amp;eacute;" with "é")
def ReplaceHtmlEntity(text):
    return re.sub("&[a-zA-Z]+;", lambda m: html.unescape(m.group(0)), text)

# Replace URLs and Emails with a certain word (improves language models)
def ReplaceUrlEmail(text):
    text = re.sub(r"([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+\.[a-zA-Z]{2,5})", "EmailAddress", text)
    text = re.sub(r"((http[s]?|ftp)?://([\w-]+\.)+[\w-]+(/[\w-~./?%+&=]*)?)", "URL", text)
    return text

# Character replacement for ANSI CodePage
def Char2CharReplacment(text, codepage):
    for key, value in codepage.items():
        text = text.replace(key, value)
    return text

# Word to Word Replacement
def Word2WordReplacement(line, wordReplacements):
    return re.sub(r"(?<![\w\u200C])[\w\u200C]+", lambda m: wordReplacements.get(m.group(0), m.group(0)), line)

#  ===== Unifying Numerals =====
_digits = [
    "۰", "٠", "0",
    "۱", "١", "1",
    "۲", "٢", "2",
    "۳", "٣", "3",
    "۴", "٤", "4",
    "۵", "٥", "5",
    "۶", "٦", "6",
    "۷", "٧", "7",
    "۸", "٨", "8",
    "۹", "٩", "9"
]

# unifies numeral characters into desired numeral type from en (0123456789) or ar (٠١٢٣٤٥٦٧٨٩).
def UnifyNumerals(text, NumeralType):
    for i in range(0, len(_digits), 3):
        if NumeralType == "en":
            text = re.sub(_digits[i] + "|" + _digits[i + 1], _digits[i + 2], text)
        elif NumeralType == "ar":
            text = re.sub(_digits[i] + "|" + _digits[i + 2], _digits[i + 1], text)
    return text

# ================= Converting Non-Standard Fonts  =================
# Converts Kurdish text written in AliK fonts into Unicode standard
def AliK2Unicode(text):
    return _replaceByList(text, normalization_replaces["AliK2Unicode"])

# Converts Kurdish text written in AliWeb fonts into Unicode standard
def AliWeb2Unicode(text):
    return _replaceByList(text, normalization_replaces["AliWeb2Unicode"])

# Converts Kurdish text written in KDylan fonts into Unicode standard
def Dylan2Unicode(text):
    return _replaceByList(text, normalization_replaces["Dylan2Unicode"])

# Converts Kurdish text written in Zarnegar fonts into Unicode standard
def Zarnegar2Unicode(text):
    return _replaceByList(text, normalization_replaces["Zarnegar2Unicode"])
