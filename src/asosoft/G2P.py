# Automated Grapheme-to-Phoneme Conversion for Central Kurdish based on Optimality Theory
# Copyright (C) 2019 Aso Mahmudi, Hadi Veisi
# Maintainer: Aso Mahmudi (aso.mehmudi@gmail.com)
# Demo: https://asosoft.github.io/g2p/
# Source Code: https://github.com/AsoSoft/AsoSoft-Library
# Test-set: https://github.com/AsoSoft/Kurdish-G2P-dataset
# Paper: https://www.sciencedirect.com/science/article/abs/pii/S0885230821000292
# Cite:
#   @article{mahmudi2021automated,
#     title={Automated grapheme-to-phoneme conversion for Central Kurdish based on optimality theory},
#     author={Mahmudi, Aso and Veisi, Hadi},
#     journal={Computer Speech \& Language},
#     volume={70},
#     pages={101222},
#     year={2021},
#     publisher={Elsevier}
#   }

import re
import os
import csv
from .Normalize import UnifyNumerals
from .Number2Word import Number2Word
from collections import OrderedDict

# Normalizion
def G2P_normalize(text):
    s = [
        "  +", " " ,
        "دٚ", "ڎ",
        "گٚ", "ڴ",
        r"(^|\s)چ بکە", r"\1چبکە",
        "َ", "ە",  # فتحه 
        "ِ", "ی",  # کسره 
        "ُ", "و",  # ضمه 
        "ء", "ئ",  # Hamza   
        "أ", "ئە",
        "إ", "ئی",
        "آ", "ئا",
        "ظ|ذ|ض", "ز",
        "ص|ث", "س",
        "ط", "ت",
        "ك", "ک",
        "ي|ى", "ی",
        "ه‌", "ە",
        "ھ", "ه",
        "ـ", "",  # tatweel
        "؟", "?",
        "،", ",",
        "؛", ";",
        r"\r", "",
    ]
    for i in range(0, len(s), 2):
        text = re.sub(s[i], s[i + 1], text)
    return text

history = {}
path = os.path.dirname(__file__)
G2P_exceptions = {}
G2P_certain = {}
def load_replaces():
    with open(os.path.join(path, "resources/G2PExceptions.csv"), 'r', encoding="utf-8", newline='\n') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the first row
        for row in reader:
            G2P_exceptions[row[0]] = row[1]
            
    with open(os.path.join(path, "resources/G2PCertain.csv"), 'r', encoding="utf-8", newline='\n') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the first row
        for row in reader:
            G2P_certain[row[0]] = row[1]


# GEN: generates all possible candidates:
# e.g.  بوون => bûn, buwn, bwun

def Generator(gr):
    if len(G2P_exceptions) == 0:
        load_replaces()

    # Converting exceptional words
    for key, value in G2P_exceptions.items():
        gr = re.sub(key, value, gr)

    # Converting certain characters
    for key, value in G2P_certain.items():
        gr = re.sub(key, value, gr)

    # Uncertainty in "و" and "ی"
    CandList1 = [""]
    while len(gr) > 0:
        temp = []
        if re.match("^ووووو", gr):
            temp.extend(["uwuwu", "uwuww", "uwwuw", "uwûw", "wuwwu", "wuwuw", "wuwû", "wûww", "wwuwu", "wwuww", "wwûw", "wûwu", "ûwwu", "ûwuw", "ûwû"])
            gr = gr[5:]
        elif re.match("^وووو", gr):
            temp.extend(["uwwu", "uwuw", "uwû", "wwuw", "wwû", "wuww", "wuwu", "wûw", "ûwu", "ûww"])
            gr = gr[4:]
        elif re.match("^ووو", gr):
            temp.extend(["wuw", "wwu", "wû", "uww", "uwu", "ûw"])
            gr = gr[3:]
        elif re.match("^وو", gr):
            temp.extend(["wu", "uw", "ww", "û"])
            gr = gr[2:]
        elif re.match("^و", gr):
            temp.extend(["u", "w"])
            gr = gr[1:]
        elif re.match("^یی", gr):
            temp.extend(["îy", "yî"])
            gr = gr[2:]
        elif re.match("^ی", gr):
            temp.extend(["y", "î"])
            gr = gr[1:]
        else:
            temp.append(gr[0])
            gr = gr[1:]

        Count = len(CandList1)
        TempList = list(CandList1)
        CandList1.clear()

        for i in range(Count):
            for j in range(len(temp)):
                WW = bool(re.match("^ww", temp[j]))
                IsPreviousVowel = bool(re.search("[aeêouûiîüȯė]$", TempList[i]))
                IsNowVowel = bool(re.match("^[aeêouûiîüȯė]", temp[j]))
                ConsonantBeforeWW = not IsPreviousVowel and WW
                hiatus = IsPreviousVowel and IsNowVowel

                if not hiatus and not ConsonantBeforeWW:
                    CandList1.append(TempList[i] + temp[j])

    # Adding "i" between Consonant Clusters
    Candidates = i_insertion(CandList1)

    # ======= Syllabification for each candidate
    OutputCandidates = syllabification(Candidates)

    # for speed up: remove candidates that has 1) syllable without vowel or 2) more than 3 consonants in coda
    cCount = len(OutputCandidates)
    if cCount > 1:
        i = cCount - 1
        while i > -1:
            if re.search("ˈ[^aeêouûiîüȯė]+(ˈ|$)", OutputCandidates[i]) or re.search("[aeêouûiîüȯė][^aeêouûiîüȯėˈ]{4,}", OutputCandidates[i]):
                del OutputCandidates[i]
            i -= 1

    return OutputCandidates

# insertion of hidden /i/ vowel
# e.g. brd => bird, brid, birid
def i_insertion(Cands):
    Candidates = []
    for i in range(len(Cands)):
        ThisCand = []
        if Cands[i]:
            ThisCand.append(Cands[i][0])
            for j in range(1, len(Cands[i])):
                Count = len(ThisCand)
                TempList = ThisCand.copy()
                ThisCand.clear()
                for k in range(Count):
                    ThisCand.append(TempList[k] + Cands[i][j])
                    if re.search(r'[^aeêouûiîüȯė][^aeêouûiîüȯė]', Cands[i][j - 1:j + 1]):
                        ThisCand.append(TempList[k] + "i" + Cands[i][j])
        else:
            ThisCand.append(Cands[i])
        Candidates.extend(ThisCand)
    return Candidates

# Syllabification of candidates
# e.g. dexom => ˈdeˈxom
def syllabification(Candidates):
    cCount = len(Candidates)
    for i in range(cCount):
        # Onset C(C)V
        Candidates[i] = re.sub(r"([^aeêouûiîȯėwy][wy]|[^aeêouûiîȯė])([aeêouûiîȯė])", r"ˈ\1\2", Candidates[i])
        # if no ˈ at beginig  (grˈtin => ˈgrˈtin)
        Candidates[i] = re.sub(r"^([^ˈ])", r"ˈ\1", Candidates[i])
        # add candidate ( 'be'sye => + 'bes'ye)
        if re.search(r"[aeêouûiîȯė][^aeêouûiîȯė]?ˈ[^aeêouûiîȯėwy][wy]", Candidates[i]):
            Candidates.append(re.sub(r"([aeêouûiîȯė][^aeêouûiîȯė]?)ˈ([^aeêouûiîȯėwy])([wy])", r"\1\2ˈ\3", Candidates[i]))
    return Candidates

# Sonority Sequencing Principle in EVAL needs phoneme ranking 
def sonority_index(ch):
    c = str(ch)
    if re.search(r"[wy]", c):  # Approximant
        return 6
    if re.search(r"[lłrř]", c):  # Lateral
        return 5
    if re.search(r"[mn]", c):  # Nasal
        return 4
    if re.search(r"[fvszşjxẍƹḧh]", c):  # Fricative
        return 3
    if re.search(r"[cç]", c):  # Affricate
        return 2
    else:  # Stop
        return 1

     
# EVAL: specifies a penalty number for each syllabified candidate
def EVAL(Candidates):
    output = {}
    if len(Candidates) > 0:
        Penalty = {}
        for candidate in Candidates:
            P = 0
            # ================= types of penalties ============
            # Complex Onset
            P += len(re.findall(r"ˈ([^aeêouûiîȯėˈ]{2,}[wy]|[^aeêouûiîȯėˈ]+[^wy])[aeêouûiîȯė]", candidate)) * 20

            # Complex Coda
            if candidate != "ˈpoynt":
                P += len(re.findall(r"[aeêouûiîȯė][^aeêouûiîȯėˈ]{3}", candidate)) * 10

            P += len(re.findall(r"[^aeêouûiîȯėˈ][wy][aeêouûiîȯė][wy][^aeêouûiîȯėˈ]", candidate)) * 20

            # SSP: ascending Sonority in coda
            codas = re.findall(r"(?<=[aeêouûiîȯė])[^aeêouûiîȯėˈ]{2,}", candidate)
            for coda in codas:
                chars = coda
                for j in range(len(chars) - 1):
                    if sonority_index(chars[j]) <= sonority_index(chars[j + 1]):
                        P += 10
            # DEP: i insertion
            P += candidate.count("i") * 2
            #===========================

            P += candidate.count("kˈr") * 3

            #  ('kurd'si'tan => 'kur'dis'tan) 
            P += len(re.findall(r"[^aeêouûiîȯėˈ]ˈsiˈtaˈ?n", candidate)) * 3

            #"(kewt|newt|ḧewt|rext|sext|dest|pest|řast|mest|pişt|wîst|hest|bîst|heşt|şest)"                    
            # suffix /it/ and /im/ ('sert => 'se'rit) ('xewt !! 'xe'wit / 'xewt)
            if not re.search(r"(rift|neft|kurt|girt|xirt|germ|term|port)", candidate):
                P += len(re.findall(r"[aeêouûiîȯė]([^aeêouûiîyȯėˈ]m|[^aeêouûiîysşxwˈ]t)$", candidate)) * 3

            # (ˈdyu/ => ˈdîw) and (ˈkwiř => ˈkuř)
            P += candidate.count("yu") * 5
            P += candidate.count("uy") * 5
            P += candidate.count("yi") * 5
            P += candidate.count("iˈ?y") * 5  # bes'ti'yan
            P += candidate.count("wu") * 5
            P += candidate.count("uˈ?w") * 2  # 'bi'bu'wî
            P += candidate.count("wi") * 2
            P += candidate.count("iw") * 2
            P += candidate.count("wû") * 5
            P += candidate.count("uˈwî") * 1

            # ˈdiˈrêˈjayˈyî => ˈdiˈrêˈjaˈyîy  (not heyyî and teyyî)
            # ˈdiˈrêjˈyî => ˈdiˈrêˈjîy
            # (NOT ˈḧeyˈyî  teyˈyî")
            P += len(re.findall(r"[^aeêouûiîȯė]ˈyî", candidate)) * 3

            # [CV]'CyV => [CV]C'yV (ˈdiˈrêˈjyî => ˈdiˈrêˈjîy) ('bes'tye'tî => 'best'ye'tî)
            P += len(re.findall(r"(?<!^)ˈ[^aeêouûiî][wy]", candidate)) * 3

            # C'CyV => CC'yV  (bir'dyan => bird'yan) ˈswênˈdyan
            P += len(re.findall(r"[^aeêouûiî]ˈ[^aeêouûiî][y][aeêouûî]", candidate)) * 2

            # twîˈwur => tu'yûr
            P += len(re.findall(r"[^aeêouûiî]wîˈw", candidate)) * 3
            #===========================
            # Cix (řê'kix'raw => řêk'xi'raw
            P += len(re.findall(r"[^aeêouûiî]ixˈ", candidate)) * 2

            # ^'hełC' => ^'heł'C
            P += len(re.findall(r"^ˈhe(ł[^aeêouûiîˈ]ˈ|ˈłi)", candidate)) * 3

            # (he'jarn => 'he'ja'rin)
            P += candidate.count(r"rn") * 5

            # ('xawn => 'xa'win) ('pyawn => pya'win)
            P += len(re.findall(r"[aêoûî][w][^aeêouûiîˈ]", candidate)) * 5

            # 
            P += len(re.findall(r"uw(ˈ|$)", candidate)) * 5
            #===========================

            # ('lab'ri'di'nî => 'la'bir'di'nî)
            P += len(re.findall(r"[aeêouûiî][^aeêouûiîˈ]ˈriˈ", candidate)) * 5
            
            # 'ser'nic, 'dek'rid, gir'fit => 'se'rinc, 'de'kird, 'gi'rift  (NOT gir'tin)
            pat = re.search(r"([^aeêouûiîˈ])ˈ([^aeêouûiîˈ])i([^aeêouûiîˈ])", candidate)
            if pat:
                C = re.sub("[iˈ]", "", pat.group())
                if sonority_index(C[1]) > sonority_index(C[2]):
                    P += 3
            # ('sern'cê => 'se'rin'cê) 
            pat = re.search(r"([^aeêouûiîˈ])([^aeêouûiîˈ])ˈ([^aeêouûiîˈ])", candidate)
            if pat:
                C = re.sub("[iˈ]", "", pat.group())
                if sonority_index(C[0]) > sonority_index(C[1]):
                    P += 3
            # ('ser'ni'cê => 'se'rin'cê) 
            pat = re.search(r"([^aeêouûiîˈ])ˈ([^aeêouûiîˈ])iˈ([^aeêouûiîˈ])", candidate)
            if pat:
                C = re.sub("[iˈ]", "", pat.group())
                if sonority_index(C[0]) > sonority_index(C[1]) and sonority_index(C[1]) > sonority_index(C[2]):
                    P += 3
            # ('gi'rit'nê => 'gir'ti'nê)  ('ku'şit'ne => 'kuş'ti'ne)
            pat = re.search(r"[aeêouûiî]ˈ([^aeêouûiîˈ])i([^aeêouûiîˈ])ˈ([^aeêouûiîˈ])", candidate)
            if pat:
                C = re.sub("[aeêouûiîˈ]", "", pat.group())
                if sonority_index(C[2]) >= sonority_index(C[1]):
                    P += 3
            Penalty[candidate] = P

        output = OrderedDict(sorted(Penalty.items(), key=lambda x: x[1]))
    return output

# chooses the best candidates for the word
def evaluator(gr, Candidates):
    Output = []
    evaluatedCandidates = EVAL(Candidates) 
    if len(evaluatedCandidates) > 0:
        LowestPenalt = list(evaluatedCandidates.values())[0]
        for key, value in evaluatedCandidates.items():
            if value < LowestPenalt + 5:
                Output.append(key)
    return gr if len(Output) == 0 else '¶'.join(Output)
   
def word_G2P(gr, SingleOutputPerWord):
    # Check history for speed up
    if gr not in history:
        history[gr] = evaluator(gr, Generator(gr))
    return history[gr].split('¶')[0] if SingleOutputPerWord else history[gr]

# Converts Central Kurdish text in standard Arabic script into syllabified phonemic Latin script (i.e. graphemes to phonems)
def KurdishG2P(text, convertNumbersToWord=False, backMergeConjunction=True, singleOutputPerWord=True):
    sb = []
    text = UnifyNumerals(text, "en")
    if convertNumbersToWord:
        text = Number2Word(text)

    text = G2P_normalize(text.strip())

    ku = "ئابپتجچحخدرڕزژسشعغفڤقکگلڵمنوۆەهیێ" + "ۋۉۊڎڴݵݸ"
    wordss = re.findall(f"([{ku}]+|[^{ku}]+)", text)
    for word in wordss:
        if re.search(f"[{ku}]", word) and word != "و":
            sb.append(word_G2P(re.sub(f"[^{ku}]+", "", word), singleOutputPerWord))
        else:
            sb.append(word)
    output = ''.join(sb)
    # conjunction و
    output = re.sub("(^|[?!.] ?)" + "و", r"\1ˈwe", output)
    if not backMergeConjunction:
        output = re.sub("و", "û", output)
    else:
        # if there are candidates preceeding conjunction (e.g ˈbîst¶ˈbîˈsit و)
        output = re.sub(r"(\w+)¶(\w+)¶(\w+) و", r"\1 و¶\2 و¶\3 و", output)
        output = re.sub(r"(\w+)¶(\w+) و", r"\1 و¶\2 و", output)
        # ('bi'ra + w => bi'raw)
        output = re.sub(r"([aeêouûiî]) و", r"\1w", output)
        # ('be'fir + û => 'bef'rû)
        output = re.sub(r"(?<=\w)ˈ([^aeêouûiî])i([^aeêouûiî]) و", r"\1ˈ\2û", output)
        # ('ser + û => 'se'rû)
        # ('sard + û => 'sar'dû)
        # ('min + û => 'mi'nû)
        # ('bi'gir + û => 'bi'gi'rû) 
        # ('gir'tin + û => 'gir'ti'nû)
        output = re.sub(r"([^aeêouûiî]) و", r"ˈ\1û", output)
        # if conjunction makes candidates the same  (e.g ˈbîsˈtû¶ˈbîsˈtû)
        output = re.sub(r"(\w+)¶\1(\s|$)", r"\1", output)

    return output.rstrip()