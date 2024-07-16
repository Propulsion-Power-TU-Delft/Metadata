# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 12:59:46 2024

@author: lgalieti
"""

import numpy as np
import os

from scipy.interpolate import interpn



KisSpacing    = np.load(os.path.dirname(os.path.realpath(__file__)) + '/Meshes/MeshKis.npy', allow_pickle=True)
NsSpacing     = np.load(os.path.dirname(os.path.realpath(__file__)) + '/Meshes/MeshNs.npy', allow_pickle=True)
VratioSpacing = np.load(os.path.dirname(os.path.realpath(__file__)) + '/Meshes/MeshVratio.npy', allow_pickle=True)
SigmaSpacing  = np.load(os.path.dirname(os.path.realpath(__file__)) + '/Meshes/Meshsigma1.npy', allow_pickle=True)
ZSpacing      = np.load(os.path.dirname(os.path.realpath(__file__)) + '/Meshes/MeshZ.npy', allow_pickle=True)
InputMeshes     = [KisSpacing,NsSpacing, VratioSpacing, SigmaSpacing, ZSpacing]
etaTSMesh     = np.load(os.path.dirname(os.path.realpath(__file__)) + '/Meshes/MeshEtaTS.npy', allow_pickle=True)
BetaTTMesh    = np.load(os.path.dirname(os.path.realpath(__file__)) + '/Meshes/MeshBetaTT.npy', allow_pickle=True)
BetaTSMesh    = np.load(os.path.dirname(os.path.realpath(__file__)) + '/Meshes/MeshBetaTS.npy', allow_pickle=True)
H0RmMesh      = np.load(os.path.dirname(os.path.realpath(__file__)) + '/Meshes/MeshH0Rm.npy', allow_pickle=True)
H1RmMesh      = np.load(os.path.dirname(os.path.realpath(__file__)) + '/Meshes/MeshH1Rm.npy', allow_pickle=True)
H3RmMesh      = np.load(os.path.dirname(os.path.realpath(__file__)) + '/Meshes/MeshH3Rm.npy', allow_pickle=True)
ZetaRotorMesh = np.load(os.path.dirname(os.path.realpath(__file__)) + '/Meshes/MeshZetaRotor.npy', allow_pickle=True)
VoutMesh     = np.load(os.path.dirname(os.path.realpath(__file__)) + '/Meshes/MeshVout.npy', allow_pickle=True)
WoutMesh     = np.load(os.path.dirname(os.path.realpath(__file__)) + '/Meshes/MeshWout.npy', allow_pickle=True)

Kis = 2.2
Ns = 0.7
Vratio_TS = 4
sigma1 = 50
Z_0T = 0.75
Interpolation = 'linear'
Extrapolate = False
eta_TS = interpn(InputMeshes,etaTSMesh,[Kis, Ns, Vratio_TS, sigma1, Z_0T], method=Interpolation, bounds_error=Extrapolate, fill_value = None)[0]
print(eta_TS)