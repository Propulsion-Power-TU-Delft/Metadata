import numpy as np


def check_bounds(Vr, SP, Ns):
    if not 3 <= Vr <= 25:
        raise Exception('Vr out of bond for 1 Stage turbine model')
    if not 0.05 <= SP <= 1.0:
        raise Exception('SP out of bond for 1 Stage turbine model')
    if not 0.1 <= Ns <= 0.8:
        raise Exception('SP out of bond for 1 Stage turbine model')


def eta_is(Vr, SP, Ns, extrapolate):
    # complexity 39, L1 norm 0.0037, Max, Min, Mean error, 4.759837699446012 8.82583563566186e-05 0.4944921690999964
    if not extrapolate:
        check_bounds(Vr, SP, Ns)

    return ((((((SP + (Vr ** SP)) ** (1.0248506910018547 ** Vr)) * 0.018928539481210576) + (((0.003258418783593659 / SP) / SP) * ((1.9035136453171813 / Vr) + Vr))) + 1.5091490734390494) ** -0.19404236345720333) + (Vr * -0.0039417625980297435)


def Dm(Vr, SP, Ns, extrapolate):
    # complexity 19, L1 norm 0.0737, Max, Min, Mean error % 35.48435339810073 0.012703764966969986 4.884726800963348
    if not extrapolate:
        check_bounds(Vr, SP, Ns)

    return ((((6.097771741034312 + Vr) * (SP ** (SP ** 0.3650504258632848))) * -0.009191510467089362) + (SP + SP)) / (SP + 0.008434797631485608)

def Dmax(Vr, SP, Ns, extrapolate):
    # complexity 45, L1 norm 0.031, Max, Min, Mean error % 15.454140480822245 0.001401830736988298 2.7833672338428035
    if not extrapolate:
        check_bounds(Vr, SP, Ns)

    return (((SP + (SP * ((((-0.6063946161560474 + np.exp(SP)) + ((((Ns / 0.20148107791011535) ** np.exp(1.4401663877830373)) + (Vr ** (0.23206187626915276 / SP))) * (((2.20415633142453 + ((1.229809287103663 ** Vr) / SP)) / Vr) / 0.36798522167062214))) + np.exp(2.0425370211955585)) ** -0.39818002058995))) / Ns) + SP) / -(-0.8141543976892793)