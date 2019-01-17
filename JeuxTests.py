# -*- coding: utf-8 -*-
"""
Created on Sun Dec  9 14:42:15 2018

@author: Serge Durand et Arthur Limbour


"""
import itertools
import random
import time
import matplotlib.pyplot as plt
import numpy as np
import math

"""rappels : fonctions dispos:
CalculSigmaOptimum(Arbre,tA,tB,cAB,cBA)
CalculSigmaAlgo2(Arbre,tA,tB,cAB,cBA)
"""
#Arbre du sujet
Arbre = [0,0,3,0,1,1,3,3]
tA = [2,3,3,4,10,3,20,5]
tB = [3,10,1,2,2,15,5,1]
cAB = [0,1,2,4,2,3,3,3]
cBA = [0,4,3,3,4,2,3,4]
sigma = [1,1,0,0,0,1,0,0]
Marques = set()

#num1 : arbre droit ("unaire")
Arbre1 = [0, 0, 1, 2, 3]
tA1 = [5, 2, 3, 3, 2]
tB1 = [2, 5, 1, 8, 1]
cAB1 = [0,1, 4, 1, 2]
cBA1 = [0,2, 1, 4, 3]
print("Algo 1 : ",CalculSigmaOptimum(Arbre1,tA1,tB1,cAB1,cBA1))
print("Algo 2 : ",CalculSigmaAlgo2(Arbre1,tA1,tB1,cAB1,cBA1))

#num2 : Arbre binaire complet hauteur 3
Arbre2 = [0, 3, 0, 0, 2, 3, 2]
tA2 = [1, 3, 6, 3, 3, 2, 1]
tB2 = [2, 4, 5, 2, 3, 2, 4]
cAB2 = [0,2, 1, 2, 4, 1, 2]
cBA2 = [0,2, 1, 1, 2, 1, 1]
print("Algo 1 : ",CalculSigmaOptimum(Arbre2,tA2,tB2,cAB2,cBA2))
print("Algo 2 : ", CalculSigmaAlgo2(Arbre2,tA2,tB2,cAB2,cBA2))

#num3 Arbre de hauteur 2 : 1 racine et que des feuilles
Arbre3 = [0, 0, 0, 0, 0, 0]
tA3 = [13, 10, 12, 13, 4, 1]
tB3 = [10, 15, 12, 9, 2, 3]
cAB3 = [0,4, 8, 1, 9, 2]
cBA3 = [0,7, 3, 8, 7, 5]
print("Algo 1 : ",CalculSigmaOptimum(Arbre3,tA3,tB3,cAB3,cBA3))
print("Algo 2 : ",CalculSigmaAlgo2(Arbre3,tA3,tB3,cAB3,cBA3))

#num4 arbre de hauteur 3, équilibré, pas d'arité fixe.
Arbre4 = [0, 6, 3, 0, 6, 0, 0, 3, 5, 5]
tA4 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
tB4 = [2, 1, 8, 2, 7, 3, 6, 4, 5, 10]
cAB4 = [0,4, 7, 5, 2, 3, 1, 1, 1, 5]
cBA4 = [0,3, 8, 4, 5, 3, 1, 2, 3, 2]

print("Algo 1 : ",CalculSigmaOptimum(Arbre4,tA4,tB4,cAB4,cBA4))
print("Algo 2 : ",CalculSigmaAlgo2(Arbre4,tA4,tB4,cAB4,cBA4))

#num5 Arbre binaire déséquilibré
Arbre5 = [0, 4, 0, 4, 0]
tA5= [10, 7, 11, 5, 8]
tB5 = [12, 5, 10, 11, 3]
cAB5 = [0,2, 5, 6, 2]
cBA5 = [0,3, 4, 7, 1]

print("Algo 1 : ",CalculSigmaOptimum(Arbre5,tA5,tB5,cAB5,cBA5))
print("Algo 2 : ",CalculSigmaAlgo2(Arbre5,tA5,tB5,cAB5,cBA5))
