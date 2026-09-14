import math

# Simple Arabic Tafqeet implementation
def tafqeet(amount):
    """
    Convert a numeric amount in Algerian Dinar to Arabic text.
    Handles whole numbers and centimes.
    """
    try:
        amount = float(amount)
    except:
        return ""

    if amount == 0:
        return "صفر دينار جزائري"

    dinar = int(math.floor(amount))
    centimes = int(round((amount - dinar) * 100))

    ones = ["", "واحد", "اثنان", "ثلاثة", "أربعة", "خمسة", "ستة", "سبعة", "ثمانية", "تسعة"]
    tens = ["", "عشرة", "عشرون", "ثلاثون", "أربعون", "خمسون", "ستون", "سبعون", "ثمانون", "تسعون"]
    hundreds = ["", "مائة", "مائتان", "ثلاثمائة", "أربعمائة", "خمسمائة", "ستمائة", "سبعمائة", "ثمانمائة", "تسعمائة"]

    # Needs a robust engine, doing a basic one for standard salaries up to millions.
    def convert_group(n):
        if n == 0: return ""
        if n < 10: return ones[n]
        if n == 10: return "عشرة"
        if 11 <= n <= 19:
            teens = ["", "أحد عشر", "اثنا عشر", "ثلاثة عشر", "أربعة عشر", "خمسة عشر", "ستة عشر", "سبعة عشر", "ثمانية عشر", "تسعة عشر"]
            return teens[n-10]
        if n < 100:
            t = n // 10
            o = n % 10
            if o == 0: return tens[t]
            return ones[o] + " و" + tens[t]

        h = n // 100
        rem = n % 100
        if rem == 0:
            return hundreds[h]
        else:
            return hundreds[h] + " و" + convert_group(rem)

    def convert_number(num):
        if num == 0: return "صفر"
        parts = []

        # Millions
        m = num // 1000000
        if m > 0:
            if m == 1: parts.append("مليون")
            elif m == 2: parts.append("مليونان")
            else: parts.append(convert_group(m) + " ملايين")
            num %= 1000000

        # Thousands
        th = num // 1000
        if th > 0:
            if th == 1: parts.append("ألف")
            elif th == 2: parts.append("ألفان")
            elif 3 <= th <= 10: parts.append(convert_group(th) + " آلاف")
            else: parts.append(convert_group(th) + " ألفاً")
            num %= 1000

        # Units
        if num > 0:
            parts.append(convert_group(num))

        return " و".join(parts)

    text_parts = []

    if dinar > 0:
        dinar_text = convert_number(dinar)
        # grammar adjustment
        if dinar_text.endswith("ألفاً"):
            text_parts.append(dinar_text[:-2] + " دينار جزائري")
        else:
            text_parts.append(dinar_text + " دينار جزائري")

    if centimes > 0:
        cent_text = convert_number(centimes)
        if centimes in [1, 2]:
            text_parts.append(cent_text + " سنتيم")
        elif 3 <= centimes <= 10:
            text_parts.append(cent_text + " سنتيمات")
        else:
            text_parts.append(cent_text + " سنتيماً")

    return " و ".join(text_parts).replace("  ", " ").strip()

if __name__ == "__main__":
    print(tafqeet(44800.0))
    print(tafqeet(1523.50))
