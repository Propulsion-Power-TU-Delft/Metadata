import numpy as np


def check_bounds(Vr, SP, Ns):
    if not 3 <= Vr <= 60:
        raise Exception('Vr out of bond for 1 Stage turbine model')
    if not 0.05 <= SP <= 1.0:
        raise Exception('SP out of bond for 1 Stage turbine model')
    if not 0.1 <= Ns <= 0.8:
        raise Exception('Ns out of bond for 1 Stage turbine model')


def eta_is(Vr, SP, Ns, extrapolate):
    # complexity 69, L1 Norm 0.0019, Max, Min, Mean error  1.061864156647796 0.0007729287290758613 0.1918775396155933
    if not extrapolate:
        check_bounds(Vr, SP, Ns)

    return np.exp((((((((-1.0197754945710527 + 1.0406420258831093) / Ns) / SP) ** np.exp(np.exp(0.6232405650526583))) * ((Vr * Vr) * Vr)) ** -(-0.13345122283723557)) + np.exp((np.exp(np.exp(Ns)) * (Vr + ((((Ns ** Ns) / 0.7364188955320303) ** Vr) + ((((((((np.exp((Ns / (SP / Ns)) / np.exp(1.1172566650413305)) * Ns) * Ns) ** Ns) ** Ns) / SP) / np.exp(Vr)) + (0.25780072271876614 * 1.0662555639301086)) / Ns)))) ** 0.10008908874086957)) * -0.015897764689540305)


def Dm(Vr, SP, Ns, extrapolate):
    # complexity 24, L1 Norm 0.058, Max, Min, Mean error % 17.692355606157317 0.02418563907283535 4.178247036998675
    if not extrapolate:
        check_bounds(Vr, SP, Ns)

    return ((((((Vr + (np.exp(0.929963902002334 ** Vr) / Ns)) * SP) * (-0.00037622888584017545 / Ns)) + SP) / Ns) ** 1.0462568574447788) + (0.26464710900899546 * SP)

def Dmax(Vr, SP, Ns, extrapolate):
    # complexity 41, L1 norm 0.0459, Max, Min, Mean error %
    if not extrapolate:
        check_bounds(Vr, SP, Ns)

    return (SP + ((SP ** 1.051614542261716) / (1.1327828832742857 * Ns))) + (((-(((np.exp(Ns) * 1.8624800638269328) ** Ns) + ((((0.8962044357459933 / Vr) ** SP) / Ns) ** (SP ** 0.4701619459079903))) + ((0.10125049222650727 / Ns) ** (0.2900813986363742 * Vr))) * SP) * -0.0999107887768247)