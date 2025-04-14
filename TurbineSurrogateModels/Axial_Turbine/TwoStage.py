import numpy as np


def check_bounds(Vr, SP, Ns):
    if not 1.2 <= Vr <= 65:
        raise Exception('Vr out of bond for 2 Stage turbine model')
    if not 0.05 <= SP <= 1.0:
        raise Exception('SP out of bond for 2 Stage turbine model')
    if not 0.1 <= Ns <= 0.8:
        raise Exception('Ns out of bond for 2 Stage turbine model')


def eta_is(Vr, SP, Ns, extrapolate):
    # complexity 69, L1 Norm 0.0022, Max, Min, Mean error  1.0877761029268296 0.0001684121714196074 0.20890973240704505
    if not extrapolate:
        check_bounds(Vr, SP, Ns)

    return (((np.exp(Vr / (1.075506101192769 ** Vr)) + (Vr / 0.1750911374730535)) + np.exp((2.67945345271631 / Vr) + ((SP + ((Vr + 1.9273455936182344) * (((0.10274980065266806 / SP) / Ns) + (((((0.10806476094195912 / Ns) ** Vr) * SP) + (((Vr + ((np.exp((np.exp(-((Vr ** np.exp(1.2150883718460082)) + -0.6310255907833575)) / SP) * Ns) / Vr) + 0.09900940235559227)) / 1.0538692674911623) ** (Ns + -0.5181886054104045))) ** Ns)))) ** 0.4411111442338427))) ** -0.022867296400574912) / 0.9752014170406826


def Dm(Vr, SP, Ns, extrapolate):
    # complexity 31, L1 Norm 0.06, Max, Min, Mean error % 17.631279571236977 0.01000650906983433 3.146330560058704
    if not extrapolate:
        check_bounds(Vr, SP, Ns)

    return (((1.3660189397066709 + (-0.019256692821957567 / SP)) + ((-0.6153591073203054 + (Vr * -0.044325917755651575)) * (0.034544010281346085 + ((((Vr * Vr) ** -0.6761024660428698) / np.exp(np.exp(3.087334393611056))) ** Ns)))) / (Ns / SP)) + 0.027801224618743153


def Dmax(Vr, SP, Ns, extrapolate):
    # complexity 28 , L1 norm 0.06, Max, Min, Mean error % 19.530094459381473 0.0012839920897520403 6.41041979731562
    if not extrapolate:
        check_bounds(Vr, SP, Ns)

    return 1.0608226430381036 * (SP + ((SP / Ns) * ((((((np.exp(-0.10789111178347) ** Vr) ** (0.09856577679218424 / Ns)) * SP) * (Vr + 1.3384079989469897)) + Ns) ** (0.007813412096321713 / Ns))))