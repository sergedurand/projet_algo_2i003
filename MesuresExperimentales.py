# -*- coding: utf-8 -*-
"""
Created on Sun Dec  9 14:42:15 2018

@author: Serge Durand et Arthur Limbour


"""

import time
import math
import numpy as np
import matplotlib.pyplot as plt
import random
import csv

#création d'arbres et d'instances :
def CalculArbreComplet(hauteur):
    arbre = []
    arbre.append(0)
    n = (2**hauteur) - 1
    for i in range(1,n):
        newV = ((i+1)//2)-1
        arbre.append(newV)
    return arbre

def InstanceAleatoire(n,M):
    tA = [random.randrange(0, M) for i in range(n)]
    tB = [random.randrange(0, M) for i in range(n)]
    cAB = [random.randrange(0, M) for i in range(n)]
    cBA = [random.randrange(0, M) for i in range(n)]
    cAB[0]=0
    cBA[0]=0
    return (tA,tB,cAB,cBA)

#permet de simplifier la génération d'arbre et l'appel des fonctions CalculSigmaOptimum...
def InstanciationComplet(h):
    n = (2**h)-1
    Arbre = CalculArbreComplet(h)
    (tA,tB,cAB,cBA)=InstanceAleatoire(n,50)
    return (Arbre,tA,tB,cAB,cBA)

 
def CalculArbreDroit(n):
    res = [0]
    for i in range(n-1):
        res.append(i)
    return res

def CalculArbreh2(n):
    res = [0]*n
    return res

#fonction de test sur algo 1:
def testCalculSigma1(t,n):
    """t = nombre de test, n = hauteur arbres. 
    Permet de faire t tests sur des arbres de même taille
    utilité : lisser les résultats de durée d'execution"""
    res = []
    for i in range(t):
        Arbre = CalculArbreDroit(n)
        (tA,tB,cAB,cBA) = InstanceAleatoire(n,50)
        tdeb = time.perf_counter_ns()
        CalculSigmaOptimum(Arbre,tA,tB,cAB,cBA)
        tfin = time.perf_counter_ns()-tdeb
        res.append(tfin)
    return np.median(res)

def testMasseCalculSigma1(n,t):
    """n = dernière valeur de n voulue"""
    Ln = []
    Ltemps = []
    for i in range(1,n+1):
        Ln.append(i)
        Ltemps.append(testCalculSigma1(t,i))
    
    return(Ln,Ltemps)


#tests de CalculBorneInf
def testCalculBorneInf(h):
    Arbre = CalculArbreComplet(h)
    n = len(Arbre)
    (tA,tB,cAB,cBA)= InstanceAleatoire(n,50)
    dA = [0]*n
    dB = [0]*n
    tdeb = time.perf_counter_ns()
    CalculBorneinf(Arbre,Arbre,set(),tA,tB,cAB,cBA,dA,dB,0)
    tfin = time.perf_counter_ns()-tdeb
    return tfin

def testMasseCalculBorneInfh(h):
    Ln = []
    Ltemp=[]
    i = 2
    while(i<=h):
        res = 0
        temp = []
        for j in range(40):
            temp.append(testCalculBorneInf(i))
        res=np.median(temp)
        Ltemp.append(res)
        Ln.append(2**i-1)
        i=i+1
    return (Ln,Ltemp)

def testCalculSigma2(h,t):
    """n doit être une puissance de 2 - 1"""
    res = []
    for i in range(t):
        (Arbre,tA,tB,cAB,cBA)=InstanciationComplet(h)
        dA = [0]*len(Arbre)
        dB = [0]*len(Arbre)
        Sigma = [0]*len(Arbre)
        Marques = [0]*len(Arbre)
        tdeb = time.perf_counter_ns()
        CalculBorneinf(Arbre,Arbre,set(),tA,tB,cAB,cBA,dA,dB,0)
        CalculSigmaOptimum2(Arbre,tA,tB,cAB,cBA,dA,dB,Sigma,Marques,0)
        tfin = time.perf_counter_ns()-tdeb
        res.append(tfin)
    return np.median(res)

def testMasseCalculSigma2(h,t):
    Ln=[]
    Ltemps=[]
    for i in range(2,h+1):
        n=2**i-1
        print(n)
        Ln.append(n)
        temp = testCalculSigma2(i,t)
        Ltemps.append(temp)
    return(Ln,Ltemps)

def testSigma2(h,t):
    res = []
    for i in range(t):
        (Arbre,tA,tB,cAB,cBA)=InstanciationComplet(h)
        dA = [0]*len(Arbre)
        dB = [0]*len(Arbre)
        Sigma = [0]*len(Arbre)
        Marques = [0]*len(Arbre)
        tdeb = time.perf_counter()
        CalculBorneInf2(Arbre,tA,tB,cAB,cBA,dA,dB)
        CalculSigmaOptimum2(Arbre,tA,tB,cAB,cBA,dA,dB,Sigma,Marques,0)
        tfin = time.perf_counter()-tdeb
        res.append(tfin)
    return np.median(res)

def testMasseSigma2(h,t):
    Ln=[]
    Ltemps=[]
    for i in range(2,h+1):
        n=2**i-1
        print(n)
        Ln.append(n)
        temp = testSigma2(i,t)
        Ltemps.append(temp)
    return(Ln,Ltemps)

#test de Calcul
#fonctions traçage de graphe
def graphe(L1,L2): #graphe obtenu par les mesures
    x = np.array(L1)
    y = np.array(L2)
    fig = plt.figure()
    plt.xlim(L1[0],L1[len(L1)-1])
    plt.plot(x,y)
    fig.savefig('CalculSigma2.png')
    #plt.show()


    
    
def CalculPente(Lx,Ly):
    """Lx contient les abscisses (ici les tailles des arbres testés)
    Ly les ordonnées (ici le temps d'exécution)"""
    res = []
    for i in range(len(Lx)-2):
        pente = (Ly[i+1]-Ly[i])/(Lx[i+1]-Lx[i])
        res.append(pente)
    pente = np.median(res)
    return pente