import unittest
from src.asosoft import *

class TestModule(unittest.TestCase):
    def test_KurdishG2P(self):
        self.assertEqual(KurdishG2P("شەو و ڕۆژ بووین بە گرفت. درێژیی دیوارەکەی گرتن"),
                         f"ˈşeˈwû ˈřoj ˈbûyn ˈbe ˈgiˈrift. ˈdiˈrêˈjîy ˈdîˈwaˈreˈkey ˈgirˈtin")
    def test_Ar2La(self):
        self.assertEqual(Ar2La("گیرۆدەی خاڵی ڕەشتە؛ گوێت لە نەغمەی تویوورە؟"),
                         f"gîrodey xałî řeşte; gwêt le neẍmey tuyûre?")
    def test_Ar2LaFeryad(self):
        self.assertEqual(Ar2LaFeryad("گیرۆدەی خاڵی ڕەشتە؛ گوێت لە نەغمەی تویوورە؟"),
                         f"gîrodey xaḻî ṟeşte; gwêt le nex̱mey tuyûre?")
    def test_Ar2LaSimple(self):
        self.assertEqual(Ar2LaSimple("گیرۆدەی خاڵی ڕەشتە؛ گوێت لە نەغمەی تویوورە؟"),
                         "gîrodey xalî reşte; gwêt le nexmey tuyûre?")
    def test_La2Ar(self):
        self.assertEqual(La2Ar("Gelî keç û xortên kurdan, hûn hemû bi xêr biçin"),
                         "گەلی کەچ و خۆرتێن کوردان، هوون هەموو ب خێر بچن")
    def test_Phonemes2IPA(self):
        self.assertEqual(Phonemes2IPA(KurdishG2P("شەو و ڕۆژ بووین بە گرفت. درێژیی دیوارەکە گرتن")),
                         f"ʃa·wu ro̞ʒ bujn ba gɪ·ɾɪft. dɪ·ɾɛ·ʒij di·wä·ɾa·ka gɪɾ·tɪn")

    def test_Normalize(self):
        self.assertEqual(Normalize("دەقے شیَعري خـــۆش. ره‌نگه‌كاني خاك"),
                         "دەقی شێعری خۆش. ڕەنگەکانی خاک")
    def test_AliK2Unicode(self):
        self.assertEqual(AliK2Unicode("ئاشناكردنى خويَندكار بة طوَرِانكاريية كوَمةلاَيةتييةكان"),
                         "ئاشناکردنی خوێندکار بە گۆڕانکارییە کۆمەڵایەتییەکان")
    def test_AliWeb2Unicode(self):
        self.assertEqual(AliWeb2Unicode("هةر جةرةيانصکي مصذووُيي کة أوو دةدا"),
                         "ھەر جەرەیانێکی مێژوویی کە ڕوو دەدا")
    def test_Dylan2Unicode(self):
        self.assertEqual(Dylan2Unicode("لثكؤلثنةران بؤيان دةركةوتووة كة دةتوانث بؤ لةش بةكةصك بث"),
                         "لێکۆلێنەران بۆیان دەرکەوتووە کە دەتوانێ بۆ لەش بەکەڵک بێ")
    def test_Zarnegar2Unicode(self):
        self.assertEqual(Zarnegar2Unicode("بلٌيٌين و بگه‌رٍيٌين بوٌ هه‌لاٌلٌه‌ى سىٌيه‌مى فه‌لسه‌فه"),
                         "بڵێین و بگەڕێین بۆ هەڵاڵەی سێیەمی فەلسەفە")
    def test_NormalizePunctuations(self):
        self.assertEqual(NormalizePunctuations("دەقی«کوردی » و ڕێنووس ،((خاڵبەندی )) چۆنە ؟", False),
                         "دەقی «کوردی» و ڕێنووس، «خاڵبەندی» چۆنە؟")
    def test_TrimLine(self):
        self.assertEqual(TrimLine("   دەق\u200c  "), "دەق")
    def test_ReplaceHtmlEntity(self):
        self.assertEqual(ReplaceHtmlEntity("ئێوە &quot;دەق&quot; بە زمانی &lt;کوردی&gt; دەنووسن"),
                         'ئێوە "دەق" بە زمانی <کوردی> دەنووسن')
    def test_UnifyNumerals(self):
        self.assertEqual(UnifyNumerals("ژمارەکانی ٤٥٦ و ۴۵۶ و 456", "en"),
                         "ژمارەکانی 456 و 456 و 456")
    def test_SeperateDigits(self):
        self.assertEqual(SeperateDigits("لە ساڵی1950دا1000دۆلاریان بە 5کەس دا"),
                         "لە ساڵی 1950 دا 1000 دۆلاریان بە 5 کەس دا")
    def test_Word2WordReplacement(self):
        self.assertEqual(Word2WordReplacement("مال، نووری مالیکی", {"مال": "ماڵ", "سلاو": "سڵاو"}),
                         "ماڵ، نووری مالیکی")

    def test_Numeral_converter(self):
        self.assertEqual(Number2Word("لە ساڵی 1999دا بڕی 40% لە پارەکەیان واتە $102.1یان وەرگرت"),
                         "لە ساڵی هەزار و نۆسەد و نەوەد و نۆدا بڕی چل لە سەد لە پارەکەیان واتە سەد و دوو پۆینت یەک دۆلاریان وەرگرت")
    
    def test_KurdishSort(self):
        self.assertEqual(KurdishSort(["یەک", "ڕەنگ", "ئەو", "ئاو", "ڤەژین", "فڵان"]),
                        ["ئاو", "ئەو", "ڕەنگ", "فڵان", "ڤەژین", "یەک"])
    def test_CustomSort(self):
        self.assertEqual(CustomSort(["یەک", "ڕەنگ", "ئەو", "ئاو", "ڤەژین", "فڵان"], list("ئءاآأإبپتثجچحخدڎڊذرڕزژسشصضطظعغفڤقكکگڴلڵمنوۆۊۉۋهھەیێ")),
                        ["ئاو", "ئەو", "ڕەنگ", "فڵان", "ڤەژین", "یەک"])
    
    def test_Poem_Meter_Classifier(self):
        poem = f"گەرچی تووشی ڕەنجەڕۆیی و حەسرەت و دەردم ئەمن\nقەت لەدەس ئەم چەرخە سپڵە نابەزم مەردم ئەمن\nمن لە زنجیر و تەناف و دار و بەند باکم نییە\nلەت لەتم کەن، بمکوژن، هێشتا دەڵێم کوردم ئەمن"
        classified = ClassifyKurdishPoem(poem)
        self.assertEqual(classified.overalMeterType, "Quantitative/عەرووزی")
        self.assertEqual(classified.overalPattern, "فاعلاتن فاعلاتن فاعلاتن فاعلن")

if __name__ == '__main__':
    unittest.main()