import re

LANGUAGE_STYLES = {
    'en': [
        re.compile(r"\b(the)\b\s+\w+\s+\b(is|are)\b", re.IGNORECASE),
        re.compile(r"\b(can't|won't|shouldn't)\b", re.IGNORECASE), # More specific contractions
    ],
    'bg': [
        re.compile(r"[Ѐ-ЯЁІЇЙ]").search,
        re.compile(r"\b(съм|си|е|сме|сте|са)\b\s+\w+\s+\b(ли)\b"),
    ],
    'zh': [
        lambda text: len(re.findall(r"[\u4e00-\u9fff]", text)) > 50, # Require a significant number of Han characters
        re.compile(r"[，。？！]").search,
    ],
    'cs': [
        re.compile(r"[áčďéěíňóřšťůúýžÁČĎÉĚÍŇÓŘŠŤŮÚÝŽ]").search,
        re.compile(r"\b(jsem|jsi|je)\b\s+\w+\s+\b(že)\b"),
    ],
    'da': [
        re.compile(r"[æøåÆØÅ]").search,
        re.compile(r"\b(er)\b\s+\w+\s+\b(ikke)\b"),
    ],
    'nl': [
        re.compile(r"\bij\b"),
        re.compile(r"\b(ben|bent|is)\b\s+\w+\s+\b(niet)\b", re.IGNORECASE),
    ],
    'et': [
        re.compile(r"[õäöüÕÄÖÜ]").search,
        re.compile(r"\b(ei)\s+\b(ole)\b"),
    ],
    'fi': [
        re.compile(r"[äöÄÖ]").search,
        re.compile(r"\b(en)\s+\b(ole)\b"), # Changed from full conjugation
    ],
    'fr': [
        re.compile(r"[àâçéèêëîïôûüÿÀÂÇÉÈÊËÎÏÔÛÜŸ]").search,
        re.compile(r"\b(n'|ne)\s+\w+\s+\b(pas)\b", re.IGNORECASE),
    ],
    'de': [
        re.compile(r"[äöüßÄÖÜẞ]").search,
        re.compile(r"\b(bin|ist)\b\s+\w+\s+\b(nicht)\b", re.IGNORECASE),
    ],
    'el': [
        re.compile(r"[Α-Ωα-ω]").search,
        re.compile(r"\b(είμαι)\b\s+\w+\s+\b(δεν)\b"),
    ],
    'hr': [
        re.compile(r"[čćđšžČĆĐŠŽ]").search,
        re.compile(r"\b(sam|si|je)\b\s+\w+\s+\b(ne)\b"),
    ],
    'hu': [
        re.compile(r"[űőŰŐ]").search,
        re.compile(r"[öüÖÜ]").search,
        re.compile(r"\b(vagyok)\b\s+\w+\s+\b(nem)\b"),
    ],
    'it': [
        re.compile(r"[àèéìòùÀÈÉÌÒÙ]").search,
        re.compile(r"\b(sono|è)\b\s+\w+\s+\b(non)\b", re.IGNORECASE),
    ],
    'lv': [
        re.compile(r"[āēīūļņŗšžĀĒĪŪĻŅŖŠŽ]").search,
        re.compile(r"\b(esmu|esi|ir)\b\s+\w+\s+\b(ne)\b"),
    ],
    'lt': [
        re.compile(r"[ąčęėįšųūžĄČĘĖĮŠŲŪŽ]").search, # Typo fix
        re.compile(r"\b(esu|esi|yra)\b\s+\w+\s+\b(ne)\b"),
    ],
    'mt': [
        re.compile(r"[ċġħż]").search,
        re.compile(r"\b(jien|kont)\b\s+\w+\s+\b(mhux)\b", re.IGNORECASE),
    ],
    'no': [
        re.compile(r"[æøåÆØÅ]").search,
        re.compile(r"\b(er)\b\s+\w+\s+\b(ikke)\b"),
    ],
    'pl': [
        re.compile(r"[ąćęłńóśźżĄĆĘŁŃÓŚŹŻ]").search,
        re.compile(r"\b(jestem|jesteś|jest)\b\s+\w+\s+\b(nie)\b"),
    ],
    'pt': [
        re.compile(r"[áàâãéêíóôõúçÁÀÂÃÉÊÍÓÔÕÚÇ]").search,
        re.compile(r"\b(eu|sou|é)\b\s+\w+\s+\b(não)\b", re.IGNORECASE),
    ],
    'ro': [
        re.compile(r"[ăâîșțĂÂÎȘȚ]").search,
        re.compile(r"\b(eu|sunt|este)\b\s+\w+\s+\b(nu)\b"),
    ],
    'ru': [
        re.compile(r"[А-ЯЁЪЫЬЭЮЯа-яёъыьэюя]").search,
        re.compile(r"\b(я|ты|он|она|оно)\s+\b(не)\b"),
    ],
    'sk': [
        re.compile(r"[áčďéíľňóŕšťúýžÁČĎÉÍĽŇÓŔŠŤÚÝŽ]").search,
        re.compile(r"\b(som|si|je)\b\s+\w+\s+\b(nie)\b"), # Typo fix
    ],
    'sl': [
        re.compile(r"[čšžČŠŽ]").search,
        re.compile(r"\b(sem|si|je)\b\s+\w+\s+\b(ne)\b"), # Typo fix
    ],
    'es': [
        re.compile(r"[áéíñóúüÁÉÍÑÓÚÜ]").search,
        re.compile(r"\b(yo|soy|es)\b\s+\w+\s+\b(no)\b", re.IGNORECASE), # Typo fix
    ],
    'sv': [
        re.compile(r"[åäöÅÄÖ]").search,
        re.compile(r"\b(är)\b\s+\w+\s+\b(inte)\b"), # Typo fix
    ],
    'tr': [
        re.compile(r"[çğıöşüÇĞIİÖŞÜ]").search, # Typo fix
        re.compile(r"\b(ben)\s+\b(değilim)\b"),
    ],
    'us': [
        re.compile(r"\b(the)\b\s+\w+\s+\b(is|are)\b", re.IGNORECASE),
        re.compile(r"\b(can't|won't|shouldn't)\b", re.IGNORECASE),
    ],
    'ar': [
        re.compile(r"[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]").search, # Typo fix
        re.compile(r"\b(أنا)\s+\b(لست)\b"),
        lambda text: len(re.findall(r"[\u0600-\u06FF]", text)) > 50, # Significant Arabic chars
    ],
}