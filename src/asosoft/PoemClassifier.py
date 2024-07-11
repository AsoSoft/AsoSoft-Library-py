# Automatic Meter Classification of Kurdish Poems
# Copyright (C) 2019 Aso Mahmudi, Hadi Veisi
# Maintainer: Aso Mahmudi (aso.mehmudi@gmail.com)
# Demo: https://asosoft.github.io/poem/
# Source Code: https://github.com/AsoSoft/AsoSoft-Library
# Test-set: https://github.com/AsoSoft/Vejinbooks-Poem-Dataset
# Paper: https://arxiv.org/abs/2102.12109
# Cite:
#@article{mahmudi2021automatic,
#    title={Automatic Meter Classification of Kurdish Poems},
#    author={Mahmudi, Aso and Veisi, Hadi},
#    journal={arXiv preprint arXiv: 2102.12109},
#    year={2021}
#}

import os
import re
from .G2P import KurdishG2P

def ClassifyKurdishPoem(poem):
    normalized = poem_normalization(poem)
    syllabified = KurdishG2P(normalized, convertNumbersToWord=True, backMergeConjunction=True, singleOutputPerWord=True).split('\n')
    classified = poem_classification(syllabified)
    return classified

class Pattern:
    def __init__(self):
        self.freq = 0
        self.weights = ""
        self.title = ""

class ScannedHemistich:
    def __init__(self):
        self.lineNo = 0
        self.scanned = ""
        self.meterID = 0
        self.dist = 0

class ResultSet:
    def __init__(self):
        self.syllabic = 0
        self.syllabicConfidence = 0.0
        self.quantitative = ""
        self.quantitativeConfidence = 0.0
        self.overalPattern = ""
        self.overalMeterType = ""
        self.details = []
class Pattern:
    def __init__(self):
        self.freq = 0
        self.weights = ""
        self.title = ""

class ResultSet:
    def __init__(self):
        self.syllabic = 0
        self.syllabicConfidence = 0.0
        self.quantitative = ""
        self.quantitativeConfidence = 0.0
        self.overalPattern = ""
        self.overalMeterType = ""
        self.details = []

CommonPatterns = []

path = os.path.dirname(__file__)

def load_poem_patterns():
    with open(os.path.join(path, "resources/PoemPatterns.csv"), 'r', encoding="utf-8") as file:
        PoemPatterns = file.readlines()
    for i in range(1, len(PoemPatterns)):
        item = PoemPatterns[i].strip().split(',')
        CommonPatterns.append(Pattern())
        CommonPatterns[-1].freq = int(item[0])
        CommonPatterns[-1].weights = item[1]
        CommonPatterns[-1].title = item[2]

max_dist = 4
patternScores = [0] * 27

# Classifies the input Kurdish poem
def poem_classification(sHemistiches):
    if len(CommonPatterns) == 0:
        load_poem_patterns()
    patternScores.clear()
    patternScores.extend([0] * 27)
    output = ResultSet()
    #===== syallabic analysis
    syllableCounts = []
    for i in range(len(sHemistiches)):
        sCount = len(sHemistiches[i].split('ˈ')) - 1
        if sCount > 0:
            syllableCounts.append(sCount)
    HemistichesCount = len(syllableCounts)
    mode = max(set(syllableCounts), key = syllableCounts.count)
    output.syllabic = mode
    output.syllabicConfidence = (syllableCounts.count(mode) / HemistichesCount) * 100

    #===== quantitative analysis
    AcceptableCandidates = []
    for i in range(len(sHemistiches)):
        AcceptableCandidates.extend(pattern_match(convert_to_CV(sHemistiches[i]), i))

    highScore = patternScores.index(max(patternScores))
    output.quantitative = CommonPatterns[highScore].title
    output.quantitativeConfidence = ((patternScores[highScore] / max_dist) / HemistichesCount) * 100

    #===== final output for each hemistich
    final = []
    for i in range(len(sHemistiches)):
        highScoreMatches = [x for x in AcceptableCandidates if x.lineNo == i and x.meterID == highScore]
        if len(highScoreMatches) > 0:
            final.append(highScoreMatches[0])
        else:
            final.append(ScannedHemistich())
    output.details = final

    # ===== overal poem classification
    stdDev = calculate_standard_deviation(syllableCounts)
    metricalMargin = 40 if output.syllabic > 10 else 50
    stdDevMargin = output.syllabic / 10
    if stdDev > stdDevMargin:
        output.overalMeterType = "Free Verse/شیعری نوێ"
    elif output.quantitativeConfidence >= metricalMargin:
        output.overalMeterType = "Quantitative/عەرووزی"
        output.overalPattern = output.quantitative
    elif output.syllabicConfidence >= 40 and stdDev < 1:
        output.overalMeterType = "Syllabic/بڕگەیی"
        output.overalPattern = str(output.syllabic) + "Syllabic"
    
    return output

# input: "ˈgerˈçî ˈtûˈşî ˈřenˈceˈřoˈyîw ˈḧesˈreˈtû ˈderˈdim ˈʔeˈmin "
# output: List<"∪––––∪–––∪–––∪–", "∪––––∪–––∪––∪∪–">
def convert_to_CV(syllabified):
    if len(syllabified) > 100: # abort if line is too long
        syllabified = " "
    CV = syllabified
    CV = re.sub(r"[\[\]«»]", "", CV) # remove "] [" 
    CV = re.sub(r"[\n\r\?,;! ]+", "¤", CV + "\n")  # open junctures (punctuation and end of line) => ¤
    CV = re.sub(" ˈ¤", "¤", CV)
    CV = re.sub(r"îˈye", "iˈye", CV) # (ˈnîˈye => ˈniˈye)
    CV = re.sub(r"([^ieuaêoîûˈ])([yw])", r"\1ɰ", CV)  # gyan-gîyan, xiwa-xuwa  => – or ∪–
    CV = re.sub(r"[bcçdfghḧjklłmnpqrřsşṣtvwxẍyzʔƹ]", "C", CV)
    syllables = CV.split('ˈ')[1:]
    output = [""]
    for i in range(len(syllables)):
        count = len(output)
        if re.search("ɰ", syllables[i]): # CVcC(C) syllable (e.g. گیان خوا)
            for j in range(count):
                output.append(output[j] + "–")
                output[j] += "∪–"
        elif re.search("([ieuaêoîû]C+|[aêoû]$|[aêo]¤$)", syllables[i]): # heavy syllable
            if i < 2: # at first position may be light
                for j in range(count):
                    output.append(output[j] + "∪")
                    output[j] += "–"
            else:
                for j in range(count):
                    output[j] += "–"
        elif re.search("([ieu]$|i¤$)", syllables[i]): # light syllable
            for j in range(count):
                output[j] += "∪"
    return output

# input: List of "∪–"s
# output: List of nearests of 27 common meter patterns
def pattern_match(cands, lineNumber):
    if len(CommonPatterns) == 0:
        load_poem_patterns()
    output = []
    if cands[0].strip() != "":
        for i in range(len(CommonPatterns)): # for 27 common meter patterns
            distances = {}
            for j in range(len(cands)): # for each candidate
                distances[j] = dist_levenshtein(cands[j], CommonPatterns[i].weights)
            lowestDist = min(distances.values())
            if lowestDist <= max_dist:
                patternScores[i] += max_dist - lowestDist
                for item in [x for x in distances.items() if x[1] == lowestDist]:
                    output.append(ScannedHemistich())
                    output[-1].lineNo = lineNumber
                    output[-1].scanned = cands[item[0]]
                    output[-1].meterID = i
                    output[-1].dist = item[1]
    return output

# ==================================================
# Normalizes the input text for classification steps.
def poem_normalization(text: str) -> str:
    text = re.sub("ط", "ت", text)
    text = re.sub("[صث]", "س", text)
    text = re.sub("[ضذظ]", "ز", text)
    text = re.sub("( و)([.،؟!])", r"\1", text)
    return text

def calculate_standard_deviation(values) -> float:
    standard_deviation = 0
    if len(values) > 0:
        avg = sum(values) / len(values)
        squared_diff  = sum((d - avg) ** 2 for d in values)
        standard_deviation = (squared_diff / len(values) ) ** 0.5
    return standard_deviation

def dist_levenshtein(s1, s2):
    if not s1:
        if s2:
            return len(s2)
        return 0
    if not s2:
        if s1:
            return len(s1)
        return 0
    m = len(s1) + 1
    n = len(s2) + 1
    d = [[0] * n for _ in range(m)]

    for i in range(m):
        d[i][0] = i
    for i in range(n):
        d[0][i] = i

    for i in range(1, m):
        for j in range(1, n):
            cost = 0 if s1[i - 1] == s2[j - 1] else 2 # or 2
            min1 = d[i - 1][j] + 1
            min2 = d[i][j - 1] + 1
            min3 = d[i - 1][j - 1] + cost
            d[i][j] = min(min1, min2, min3)
    return d[m - 1][n - 1]