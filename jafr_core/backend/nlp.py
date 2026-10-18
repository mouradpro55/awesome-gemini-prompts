import re

tashkeel_regex = re.compile(r'[\u064B-\u0652\u0640\u0653-\u065F]')
non_arabic_regex = re.compile(r'[^\u0621-\u064A\s]')

def clean_and_normalize(input_text, unify_hamzat=True, expand_shaddah=False):
    if expand_shaddah:
        res = []
        for i, char in enumerate(input_text):
            if char == '\u0651':
                # find last letter
                for j in range(i - 1, -1, -1):
                    if '\u0621' <= input_text[j] <= '\u064A':
                        res.append(input_text[j])
                        break
            else:
                res.append(char)
        cleaned = "".join(res)
    else:
        cleaned = input_text

    cleaned = tashkeel_regex.sub('', cleaned)
    cleaned = non_arabic_regex.sub('', cleaned)

    res = []
    for char in cleaned:
        if unify_hamzat:
            if char in ['أ', 'إ', 'آ', 'ء', 'ئ', 'ؤ']:
                char = 'ا'
            elif char == 'ة':
                char = 'ه'
            elif char == 'ى':
                char = 'ي'

        if not char.isspace() and not ('\u0621' <= char <= '\u064A'):
            continue

        res.append(char)

    return "".join(res).strip()
