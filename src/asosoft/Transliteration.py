import re
import os
from .G2P import KurdishG2P
_latinLetters = "a-zêîûçşéúıŕřĺɫƚḧẍḍṿʔ"

_TransliterationReplaces = {
    "LaDi2Ar": [
        "gh", "ẍ",
        "hh", "ḧ",
        "ll", "ɫ",
        "rr", "ř"
    ],
    "La2Ar": [
        "\u201C", "«",
        "\u201D", "»",
        rf"([0-9])([\'’-])([aeiouêîûéú])", r"\1\3",     # (e.g. 1990'an 5'ê)
        "ʔ", "",    # glottal stop
        rf"(^|[^{_latinLetters}0-9\"’])([aeiouêîûéú])", r"\1ئ\2", #insert initial hamza
        rf"([aeouêîûéú])([aeiouêîûéú])", r"\1ئ\2",     #insert hamza between adjacent vowels
        rf"(ئ)([uû])([^{_latinLetters}0-9])", r"و\3",     #omit the inserted hamza for "û" (=and)
        "a", "ا",
        "b", "ب",
        "ç", "چ",
        "c", "ج",
        "d", "د",
        "ḍ", "ڎ", # a Horami consonant
        "ê|é", "ێ",
        "e", "ە",
        "f", "ف",
        "g", "گ",
        "h", "ه",
        "ḧ", "ح",
        "i|ı", "",
        "î|y|í", "ی",
        "j", "ژ",
        "k", "ک",
        "l", "ل",
        "ɫ|ł|ƚ|Ɨ|ĺ", "ڵ",
        "m", "م",
        "n", "ن",
        "ŋ", "نگ",
        "o", "ۆ",
        "ö", "وێ",
        "p", "پ",
        "q", "ق",
        "r", "ر",
        "ř|ŕ", "ڕ",
        "s", "س",
        "ş|š|ș|s̩", "ش",
        "ṣ", "ص",
        "t", "ت",
        "ṭ", "ط",
        "û|ú", "وو",
        "u|w", "و",
        "ü", "ۊ",
        "v", "ڤ",
        "x", "خ",
        "ẍ", "غ",
        "z", "ز",
        rf"ه($|[^ابپتجچحخدرڕزژسشصعغفڤقکگلڵمنوۆهەیێ])", r"هـ\1",  # word-final h
        "\"|’", "ئ", # need checking, not sure "ع" or "ئ"
        "\\u003F", "؟", #question mark
        ",", "،",  #comma
        ";", "؛",  #semicolon
    ]
}

def _replaceByList(text, replaceList):
    for i in range(0, len(replaceList), 2):
        text = re.sub(replaceList[i], replaceList[i + 1], text)
    return text

# Transliterating the Latin script into Arabic script of Kurdish (e.g. çak→چاک)
def La2Ar(text):
    text = _replaceByList(text.lower(), _TransliterationReplaces["La2Ar"])
    return text

def LaDigraph2Ar(text):
    text = text.lower()
    text = _replaceByList(text, _TransliterationReplaces["LaDi2Ar"])
    text = _replaceByList(text, _TransliterationReplaces["La2Ar"])
    return text

#Transliterating the Arabic script into Latin script of Kurdish (e.g. چاک→çak)
def Ar2La(text):
    return Phonemes2Hawar(KurdishG2P(text, backMergeConjunction=False))

# Transliterating the Arabic script into Latin script of Kurdish (e.g. چاک→çak)
def Ar2LaSimple(text):
    text = Phonemes2Hawar(KurdishG2P(text, backMergeConjunction=False))
    text = text.replace("ḧ", "h")
    text = text.replace("ř", "r")
    text = text.replace("ł", "l")
    text = text.replace("ẍ", "x")
    return text

# Transliterating the Arabic script into Latin script of Kurdish (e.g. چاک→çak)
def Ar2LaF(text):
    text = Phonemes2Hawar(KurdishG2P(text, backMergeConjunction=False))
    text = text.replace("ˈ", "")
    text = text.replace("ř", "ṟ")
    text = text.replace("ł", "ḻ")
    text = text.replace("ħ", "ẖ")
    text = text.replace("ẍ", "x̱")
    text = text.replace("ƹ", "‛")
    text = text.replace("ʔ", "")
    return text

_path = os.path.dirname(__file__) 
# Converts the output of the G2P into IPA (e.g. ˈdeˈçê→da.t͡ʃɛ)
def Phonemes2IPA(text):
    text = re.sub(r'(?<=(^|\W))ˈ', '', text)
    text = re.sub(r'ˈ', '·', text) #middle dot
    
    with open(os.path.join(_path, "resources/Phoneme2IPA.csv"), 'r') as file:
        Phoneme2IPA = file.readlines()

    for i in range(1, len(Phoneme2IPA)):
        item = Phoneme2IPA[i].split(',')
        text = re.sub(item[0], item[1], text)
    return text

# Converts the output of the G2P into Hawar (e.g. ˈʔeˈłêm→ełêm)
def Phonemes2Hawar(text):
    text = text.replace("ˈ", "")
    text = re.sub(r'(^ʔ|(?<=\W)ʔ)', '', text)
    text = re.sub(r'[ʔƹ]', '’', text)
    return text

# Converts the output of the G2P into Jira's ASCII format (e.g. ˈdeˈçim→D▪A▪CH▪M)
def Phonemes2ASCII(text):
    text = re.sub(r'[iˈ]', '', text)
    
    with open(os.path.join(_path, "resources/Phoneme2Ascii.csv"), 'r') as file:
        Phoneme2Ascii = file.readlines()

    for i in range(1, len(Phoneme2Ascii)):
        item = Phoneme2Ascii[i].split(',')
        text = re.sub(item[0], item[1] + '▪', text)
    return text
