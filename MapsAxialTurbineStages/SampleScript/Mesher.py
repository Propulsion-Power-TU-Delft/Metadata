# -*- coding: utf-8 -*-
"""
Created on Sun Apr  7 12:06:41 2024

@author: lgalieti
"""

import pandas as pd
import numpy as np
Dataframe = pd.read_csv('./CSVFiles/'+ 'RepairedOptimizationResults.csv')
Dataframe.sort_values(['K_is', 'Ns', 'Vr', 'N','Z'], inplace = True)
np.save('./Meshes/' + 'MeshKis', np.sort(np.unique(Dataframe['K_is'])))
np.save('./Meshes/' + 'MeshNs', np.sort(np.unique(Dataframe['Ns'])))
np.save('./Meshes/' + 'MeshVratio', np.sort(np.unique(Dataframe['Vr'])))
np.save('./Meshes/' + 'MeshSigma1', np.sort(np.unique(Dataframe['N'])))
np.save('./Meshes/' + 'MeshZ', np.sort(np.unique(Dataframe['Z'])))



Dim0 = len(np.unique(Dataframe['K_is']))
Dim1 = len(np.unique(Dataframe['Ns']))
Dim2 = len(np.unique(Dataframe['Vr']))
Dim3 = len(np.unique(Dataframe['N']))
Dim4 = len(np.unique(Dataframe['Z']))


MeshEtaTS = np.empty([Dim0, Dim1, Dim2, Dim3, Dim4])
MeshBetaTT = np.empty([Dim0, Dim1, Dim2, Dim3, Dim4])
MeshBetaTS = np.empty([Dim0, Dim1, Dim2, Dim3, Dim4])
MeshH0Rm   = np.empty([Dim0, Dim1, Dim2, Dim3, Dim4])
MeshH1Rm   = np.empty([Dim0, Dim1, Dim2, Dim3, Dim4])
MeshH3Rm   = np.empty([Dim0, Dim1, Dim2, Dim3, Dim4])
MeshV3   = np.empty([Dim0, Dim1, Dim2, Dim3, Dim4])
MeshW3   = np.empty([Dim0, Dim1, Dim2, Dim3, Dim4])
count = 0
for i in range(Dim0):
    for j in range(Dim1):
        for k in range(Dim2):
            for l in range(Dim3):
                for m in range(Dim4):
                    MeshEtaTS[i,j,k,l,m] = Dataframe['etaTS'].iloc[count]
                    MeshBetaTT[i,j,k,l,m] = Dataframe['PratioTT'].iloc[count]
                    MeshBetaTS[i,j,k,l,m] = Dataframe['PratioTS'].iloc[count]
                    MeshH0Rm[i,j,k,l,m] = Dataframe['H0_div_Rm'].iloc[count]
                    MeshH1Rm[i,j,k,l,m] = Dataframe['H1_div_Rm'].iloc[count]
                    MeshH3Rm[i,j,k,l,m] = Dataframe['H3_div_Rm'].iloc[count]
                    MeshV3[i,j,k,l,m] = Dataframe['V3(m/s)'].iloc[count]
                    MeshW3[i,j,k,l,m] = Dataframe['W3(m/s)'].iloc[count]
                    count+= 1
                    # print(count)
                    

np.save('./Meshes/' + 'MeshEtaTS' , MeshEtaTS)
np.save('./Meshes/' + 'MeshBetaTT' , MeshBetaTT )                    
np.save('./Meshes/' + 'MeshBetaTS' , MeshBetaTS ) 
np.save('./Meshes/' + 'MeshH0Rm' , MeshH0Rm)
np.save('./Meshes/' + 'MeshH1Rm' , MeshH1Rm )                    
np.save('./Meshes/' + 'MeshH3Rm' , MeshH3Rm )
# np.save('./Meshes/' + 'MeshVout' , MeshV3 )                    
# np.save('./Meshes/' + 'MeshWout' , MeshW3 )