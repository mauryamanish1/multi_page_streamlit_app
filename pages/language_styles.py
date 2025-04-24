import re

LANGUAGE_STYLES = {
    'en': [  # English
        re.compile(r"\b(the|a|an)\b", re.IGNORECASE),  # Common articles
        re.compile(r"ing\b"),  # Common suffix
        re.compile(r"'s\b"),  # Possessive apostrophe
    ],
    'bg': [  # Bulgarian (Cyrillic script)
        re.compile(r"[Ѐ-ЯЁІЇЙ]").search,  # Contains Cyrillic letters
        re.compile(r"на\b"),  # Common preposition
        re.compile(r"те\b"),  # Common pronoun ending
    ],
    'zh': [  # Chinese (Han script)
        re.compile(r"[\u4e00-\u9fff]").search,  # Contains Han characters
        re.compile(r"[，。？！]").search,  # Common Chinese punctuation
        lambda text: len(re.findall(r"\b\w+\b", text)) < len(text) / 3, # Lower ratio of space-separated words
    ],
    'cs': [  # Czech (Latin script with diacritics)
        re.compile(r"[áčďéěíňóřšťůúýžÁČĎÉĚÍŇÓŘŠŤŮÚÝŽ]").search,  # Contains Czech diacritics
        re.compile(r"\b(a|i|o|s|z)\b"),  # Common short words
        re.compile(r"ovi\b"), # Common masculine possessive ending
    ],
    'da': [  # Danish (Latin script with specific vowels)
        re.compile(r"[æøåÆØÅ]").search,  # Contains Danish specific vowels
        re.compile(r"\b(og|i|en|et)\b"),  # Common conjunctions/articles
        re.compile(r"erne\b"), # Common plural definite suffix
    ],
    'nl': [  # Dutch (Latin script, digraphs)
        re.compile(r"\bij\b"),  # Common digraph
        re.compile(r"\b(de|het|een)\b", re.IGNORECASE),  # Common articles
        re.compile(r"lijk\b"), # Common suffix
    ],
    'et': [  # Estonian (Latin script with specific vowels)
        re.compile(r"[õäöüÕÄÖÜ]").search,  # Contains Estonian specific vowels
        re.compile(r"\bon\b"),  # Common pronoun
        re.compile(r"line\b"), # Common suffix
    ],
    'fi': [  # Finnish (Latin script with specific vowels, agglutinative)
        re.compile(r"[äöÄÖ]").search,  # Contains Finnish specific vowels
        re.compile(r"\b(ja|on|ei)\b"),  # Common conjunction/verb
        re.compile(r"nen\b"), # Common suffix
    ],
    'fr': [  # French (Latin script with accents, common articles)
        re.compile(r"[àâçéèêëîïôûüÿÀÂÇÉÈÊËÎÏÔÛÜŸ]").search,  # Contains French accents/cedilla
        re.compile(r"\b(le|la|les|un|une|des)\b", re.IGNORECASE),  # Common articles
        re.compile(r"ment\b"), # Common suffix
    ],
    'de': [  # German (Latin script with umlauts, Esszett)
        re.compile(r"[äöüßÄÖÜẞ]").search,  # Contains German umlauts/eszett
        re.compile(r"\b(der|die|das|ein|eine)\b", re.IGNORECASE),  # Common articles
        re.compile(r"keit\b"), # Common suffix
    ],
    'el': [  # Greek (Greek script)
        re.compile(r"[Α-Ωα-ω]").search,  # Contains Greek letters
        re.compile(r"[.,·;]").search, # Common Greek punctuation
        lambda text: len(re.findall(r"\b\w+\b", text)) < len(text) / 3, # Lower ratio of space-separated words
    ],
    'hr': [  # Croatian (Latin script with specific diacritics)
        re.compile(r"[čćđšžČĆĐŠŽ]").search,  # Contains Croatian diacritics
        re.compile(r"\b(i|a|je|ne)\b"),  # Common conjunctions/short words
        re.compile(r"ski\b"), # Common suffix
    ],
    'hu': [  # Hungarian (Latin script with double acute, umlauts)
        re.compile(r"[űőŰŐ]").search,  # Contains Hungarian double acute
        re.compile(r"[öüÖÜ]").search,  # Contains Hungarian umlauts
        re.compile(r"\b(a|az|és|nem)\b"),  # Common articles/conjunction/negation
        re.compile(r"nak\b"), # Common suffix
    ],
    'it': [  # Italian (Latin script with accents, common articles)
        re.compile(r"[àèéìòùÀÈÉÌÒÙ]").search,  # Contains Italian accents
        re.compile(r"\b(il|lo|la|i|gli|le|un|una|uno)\b", re.IGNORECASE),  # Common articles
        re.compile(r"mente\b"), # Common suffix
    ],
    'lv': [  # Latvian (Latin script with specific diacritics)
        re.compile(r"[āēīūļņŗšžĀĒĪŪĻŅŖŠŽ]").search,  # Contains Latvian diacritics
        re.compile(r"\b(un|ir|nav)\b"),  # Common conjunction/verbs
        re.compile(r"ums\b"), # Common suffix
    ],
    'lt': [  # Lithuanian (Latin script with specific diacritics)
        re.compile(r"[ąčęėįšųūžĄČĘĖĮŠŲŪŽ]").search,  # Contains Lithuanian diacritics
        re.compile(r"\b(ir|o|kad)\b"),  # Common conjunctions
        re.compile(r"as\b"), # Common suffix
    ],
    'mt': [  # Maltese (Latin script with specific diacritics, Arabic influence)
        re.compile(r"[ċġħż]").search,  # Contains Maltese specific diacritics
        re.compile(r"\b(il-|l-|u-|id-|is-)\b", re.IGNORECASE), # Common definite articles (prefix)
        re.compile(r"ijiet\b"), # Common plural suffix
    ],
    'no': [  # Norwegian (Latin script with specific vowels)
        re.compile(r"[æøåÆØÅ]").search,  # Contains Norwegian specific vowels
        re.compile(r"\b(og|i|en|et)\b"),  # Common conjunctions/articles (similar to Danish)
        re.compile(r"ene\b"), # Common plural definite suffix
    ],
    'pl': [  # Polish (Latin script with specific diacritics)
        re.compile(r"[ąćęłńóśźżĄĆĘŁŃÓŚŹŻ]").search,  # Contains Polish diacritics
        re.compile(r"\b(i|a|że|nie)\b"),  # Common conjunctions/short words/negation
        re.compile(r"ski\b"), # Common suffix (similar to Croatian)
    ],
    'pt': [  # Portuguese (Latin script with accents, common articles)
        re.compile(r"[áàâãéêíóôõúçÁÀÂÃÉÊÍÓÔÕÚÇ]").search,  # Contains Portuguese accents/cedilla
        re.compile(r"\b(o|a|os|as|um|uma|uns|umas|de|do|da)\b", re.IGNORECASE),  # Common articles/prepositions
        re.compile(r"mente\b"), # Common suffix (similar to Italian)
    ],
    'ro': [  # Romanian (Latin script with specific diacritics)
        re.compile(r"[ăâîșțĂÂÎȘȚ]").search,  # Contains Romanian specific diacritics
        re.compile(r"\b(și|un|o|pe)\b"),  # Common conjunction/articles/preposition
        re.compile(r"esc\b"), # Common verb ending
    ],
    'ru': [  # Russian (Cyrillic script)
        re.compile(r"[А-ЯЁЪЫЬЭЮЯа-яёъыьэюя]").search,  # Contains Russian Cyrillic letters
        re.compile(r"и\b"),  # Common conjunction
        re.compile(r"ый\b"),  # Common adjective ending
    ],
    'sk': [  # Slovak (Latin script with specific diacritics)
        re.compile(r"[áčďéíľňóŕšťúýžÁČĎÉÍĽŇÓŔŠŤÚÝŽ]").search,  # Contains Slovak diacritics
        re.compile(r"\b(a|aj|že|nie)\b"),  # Common conjunctions/short words/negation
        re.compile(r"ský\b"), # Common adjective ending
    ],
    'sl': [  # Slovenian (Latin script with specific diacritics)
        re.compile(r"[čšžČŠŽ]").search,  # Contains Slovenian diacritics
        re.compile(r"\b(in|je|da|ne)\b"),  # Common conjunctions/short words/negation
        re.compile(r"ski\b"), # Common adjective ending (similar to Croatian/Polish)
    ],
    'es': [  # Spanish (Latin script with accents, common articles)
        re.compile(r"[áéíñóúüÁÉÍÑÓÚÜ]").search,  # Contains Spanish accents/ñ/ü
        re.compile(r"\b(el|la|los|las|un|una|unos|unas|de|del|a|al)\b", re.IGNORECASE),  # Common articles/prepositions
        re.compile(r"mente\b"), # Common suffix (similar to Italian/Portuguese)
    ],
    'sv': [  # Swedish (Latin script with specific vowels)
        re.compile(r"[åäöÅÄÖ]").search,  # Contains Swedish specific vowels
        re.compile(r"\b(och|i|en|ett)\b"),  # Common conjunctions/articles (similar to Danish/Norwegian)
        re.compile(r"het\b"), # Common suffix
    ],
    'tr': [  # Turkish (Latin script with specific letters)
        re.compile(r"[çğıöşüÇĞIİÖŞÜ]").search,  # Contains Turkish specific letters
        re.compile(r"\b(ve|bir|bu|o)\b"),  # Common conjunction/articles/pronouns
        re.compile(r"ler\b"), # Common plural suffix
    ],
    'us': [  # US English (same as 'en' for these purposes)
        re.compile(r"\b(the|a|an)\b", re.IGNORECASE),
        re.compile(r"ing\b"),
        re.compile(r"'s\b"),
    ],
    'ar': [  # Arabic (Arabic script, right-to-left)
        re.compile(r"[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]").search,  # Contains Arabic script
        re.compile(r"ال\b|\bفي\b|\bو\b"), # Common article/preposition/conjunction
        lambda text: len(re.findall(r"\b\w+\b", text)) < len(text) / 3 if text else False, # Lower ratio of space-separated words
    ],
}