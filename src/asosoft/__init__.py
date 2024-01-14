__version__ = "0.1.0"

from .Sort import (
    kurdish_sort,
    CustomSort
)

from .Number2Word import Number2Word

from .Transliteration import (
    Ar2La,
    Ar2LaF,
    Ar2LaSimple,
    La2Ar,
    LaDigraph2Ar,
    Phonemes2ASCII,
    Phonemes2Hawar,
    Phonemes2IPA    
)

from .Normalize import (
    Normalize,
    SeperateDigits,
    NormalizePunctuations,
    TrimLine,
    ReplaceHtmlEntity,
    ReplaceUrlEmail,
    Char2CharReplacment,
    Word2WordReplacement,
    UnifyNumerals,    
    AliK2Unicode,
    AliWeb2Unicode,
    Dylan2Unicode,
    Zarnegar2Unicode
)

from .G2P import KurdishG2P

from .PoemClassifier import ClassifyKurdishPoem