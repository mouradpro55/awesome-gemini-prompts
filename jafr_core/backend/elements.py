ELEMENTS_MAP = {
    'ا': "fire", 'ه': "fire", 'ط': "fire", 'م': "fire", 'ف': "fire", 'ش': "fire", 'ذ': "fire",
    'ب': "earth", 'و': "earth", 'ي': "earth", 'ن': "earth", 'ص': "earth", 'ت': "earth", 'ض': "earth",
    'ج': "air", 'ز': "air", 'ك': "air", 'س': "air", 'ق': "air", 'ث': "air", 'ظ': "air",
    'د': "water", 'ح': "water", 'ل': "water", 'ع': "water", 'ر': "water", 'خ': "water", 'غ': "water",
}

def calculate_elements(text: str):
    counts = {"fire": 0, "earth": 0, "air": 0, "water": 0}
    for char in text:
        if not char.isspace() and char in ELEMENTS_MAP:
            counts[ELEMENTS_MAP[char]] += 1

    dominant = "fire"
    max_val = counts["fire"]

    for elem in ["earth", "air", "water"]:
        if counts[elem] > max_val:
            max_val = counts[elem]
            dominant = elem

    return counts, dominant
