import numpy as np


def check_bounds(Vr, SP, psi_is):
    if not 3 <= Vr <= 60:
        raise Exception('Vr out of bond for 1 Stage turbine model')
    if not 0.01 <= SP <= 0.5:
        raise Exception('SP out of bond for 1 Stage turbine model')
    if not 0.7 <= psi_is <= 1.6:
        raise Exception('SP out of bond for 1 Stage turbine model')


def eta_is(Vr, SP, psi_is, extrapolate):
    # complexity 51, L2 norm 0.05, Max, Min, Mean error 1.165413874326461 0.0005311762105719708 0.21087278126343953
    if not extrapolate:
        check_bounds(Vr, SP, psi_is)

    return 0.01*(psi_is + (((-0.007863799466904128 * (psi_is + ((((Vr ** -(psi_is)) + ((psi_is / 1.221888472205559) ** 19.278464013958914)) / Vr) ** -0.27555777733465103))) / SP) + ((((((0.8793678410679834 / psi_is) / psi_is) ** 4.534677203619187) + SP) * -0.6242954550512632) + ((-((psi_is ** psi_is) ** psi_is) + ((-0.049409097278818946 * Vr) / psi_is)) + (1.8866047473112633 / 0.02002867905132041)))))

def Dmax(Vr, SP, psi_is, extrapolate):
    # complexity 51, L2 norm 0.05, Max, Min, Mean error 1.165413874326461 0.0005311762105719708 0.21087278126343953
    if not extrapolate:
        check_bounds(Vr, SP, psi_is)

    return SP + (((SP * (psi_is + (((((((0.0015582858273317803 * Vr) + -0.5550897137238979) / 1.3567133936738118) / psi_is) / 0.644613715526949) + psi_is) * ((((((psi_is * psi_is) ** psi_is) ** psi_is) ** psi_is) * -0.025057250530484642) + (((0.0006012364349776816 ** psi_is) * ((1.0332369889473891 ** Vr) / 0.005193116718162386)) + 0.45755870815689836))))) / 0.6525845360628764) / psi_is)