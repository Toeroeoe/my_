

def linear(x, multiplicant, addend):

    y                           = x * multiplicant + addend

    return y


def relative_difference(array1, array2, percent = False):

    from my_.math.arithmetic import difference, division

    absolute_difference         = difference(array1, array2)

    relative_difference         = division(absolute_difference, array2)

    if percent == True: return relative_difference * 100

    return relative_difference

