import unicodedata

def simplify_float(number):
    vf = "VULGAR FRACTION "
    vulgars = {0.125 : unicodedata.lookup(vf + "ONE EIGHTH"),
               0.2   : unicodedata.lookup(vf + "ONE FIFTH"),
               0.25  : unicodedata.lookup(vf + "ONE QUARTER"),
               0.375 : unicodedata.lookup(vf + "THREE EIGHTHS"),
               0.4   : unicodedata.lookup(vf + "TWO FIFTHS"),
               0.5   : unicodedata.lookup(vf + "ONE HALF"),
               0.6   : unicodedata.lookup(vf + "THREE FIFTHS"),
               0.625 : unicodedata.lookup(vf + "FIVE EIGHTHS"),
               0.75  : unicodedata.lookup(vf + "THREE QUARTERS"),
               0.8   : unicodedata.lookup(vf + "FOUR FIFTHS"),
               0.875 : unicodedata.lookup(vf + "SEVEN EIGHTHS")}

    decimal = int(number)
    if number == decimal:
        return str(decimal)

    vulgar = vulgars.get(number - decimal)
    if vulgar:
        if decimal == 0:
            return vulgar
        return "%d%s" % (decimal, vulgar)
    return "%.1f" % number