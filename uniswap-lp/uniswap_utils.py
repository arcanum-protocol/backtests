from math import sqrt

def liquidity0(amount, pa, pb):
    if pa > pb:
        pa, pb = pb, pa
    return amount * (sqrt(pa) * sqrt(pb)) / (sqrt(pb) - sqrt(pa))

def liquidity1(amount, pa, pb):
    if pa > pb:
        pa, pb = pb, pa
    return amount / (sqrt(pb) - sqrt(pa))

def calc_amount0(liq, pa, pb):
    if pa > pb:
        pa, pb = pb, pa
    return liq * (sqrt(pb) - sqrt(pa)) / sqrt(pa) / sqrt(pb)


def calc_amount1(liq, pa, pb):
    if pa > pb:
        pa, pb = pb, pa
    return liq * (sqrt(pb) - sqrt(pa))

def calc_x(liq, pa, pb):
    # if pa > pb:
    #     pa, pb = pb, pa
    return liq * (1/sqrt(pb) - 1/sqrt(pa))