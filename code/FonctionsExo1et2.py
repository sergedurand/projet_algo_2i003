# -*- coding: utf-8 -*-
"""
Created on Sun Dec  9 14:42:15 2018

@author: Serge Durand et Arthur Limbour


"""



import itertools
import random
import math


def duree(u,Sigmau,tA,tB):
    if(Sigmau==1):
        return tA[u]
    return tB[u]

#complexité : theta(1) car 1 seule comparaison et l'accès au tableau tA comme tB est en temps constant

def valCom(u,v,Sigmau,Sigmav,cAB,cBA):
    if(Sigmau==Sigmav):
        return 0
    elif(Sigmau==1):
        return cAB[v] #v va de 1 à n-1... cAB est de taille n-2.
    return cBA[v]

#complexité en theta(1) également, au plus 2 comparaisons, accès à cAB ou cBA en temps constant

def succ(u,Arbre):
    res = set()
    for i in range(1,len(Arbre)):
        if(Arbre[i] == u):
            res.add(i)
    return res

#complexité en theta(n) = la boucle tourne exactement n fois, il y a n comparaison exactement, et au plus n add. 
#add est une primitive en temps constant pour un set

def CalculDelta(Arbre,tA,tB,cAB,cBA,sigma,u):
    Succ = succ(u,Arbre)
    if(len(Succ)==0):
        return duree(u,sigma[u],tA,tB)
    return duree(u,sigma[u],tA,tB) + max([CalculDelta(Arbre,tA,tB,cAB,cBA,sigma,v)+valCom(u,v,sigma[u],sigma[v],cAB,cBA) for v in Succ])

"""
Complexité :
On fait exactement n appels récursif, peu importe la structure de l'arborescence.
En effet la construction de liste parcours tout les successeurs de la racine, puis tout les successeurs des successeurs etc.
Chaque appel est en complexité theta(n) car l'appel succ(u,Arbre) est toujours en theta de n, peu importe u,
c'est la taille de l'arbre qui compte. Modifié l'arbre à chaque fois ne ferai a priori aucun gain
la complexité est donc n*n = n². 
on fait également n appels en tout à valcom, cela ne change pas la complexité. n² + n est dans theta(n²).
preuve à rédiger par induction structurelle pour être plus rigoureux ?
"""

def convBinaire(n,l):
    """n est le nombre à convertir, l la longueur de la liste
    = le nombre de bits du résultat. On travaille sur les bits plutôt que 
    les opérations arithmétique pour la performance
    left shift de 1 = division par 2. On regarde le dernier bit plutôt que le modulo
    de la division par 2"""
    res =[]
    while(n!=0):
        res.append(n&1)
        n = n>>1
    res.reverse()
    #on remplit par des 0 à gauche le reste de la liste
    res = [0]*(l-len(res)) + res
    return res
    
def CalculListeAllocs(Arbre):
    n = len(Arbre)
    res = []
    for i in range(2**n-1):
        res.append(convBinaire(i,n))
    return res

def CalculSigmaOptimum(Arbre,tA,tB,cAB,cBA):
   # n = len(Arbre)
    #Allocs = [list(tup) for tup in list(itertools.product(range(2), repeat=n))]
    Allocs = CalculListeAllocs(Arbre)
    Lbest = Allocs[0]
    Deltabest = CalculDelta(Arbre,tA,tB,cAB,cBA,Allocs[0],0) #vu qu'on recherche un min on peut pas initialisé à 0
    for sigma in Allocs[1:]: #pas besoin de recalculer pour la première allocation possible
        Deltatemp = CalculDelta(Arbre,tA,tB,cAB,cBA,sigma,0)
        if Deltatemp < Deltabest: #on a trouvé une meilleure allocation
            Deltabest = Deltatemp
            Lbest= sigma
    return (Lbest,Deltabest)
        

#2^n allocations possibles. à vérifier, calcul de la construction de la liste de toutes les allocs possibles, doc itertools
            
def CalculBorneinf(Arbre,Candidats,Marques,tA,tB,cAB,cBA,dA,dB,cpt):
    """Au premier appel Candidats = Arbre, Marques = set vide.
    dA = dB = [0]*len(Arbre)
    cpt n'est là que pour compter les appels récursifs, on le met à 0...
    """
    #Marques est le set vide au départ. On y ajoute les sommets calculés à chaque étape.
    #Candidat est un set pour éviter les doublons. Il représente les sommets dont on veut calculer dA et dB.
    #au premier appel il contient l'arbre, et on le transforme immédiatement en l'ensemble des feuilles par une fonction auxiliaire (linéaire)
    #puis les parents de ces feuilles uniquement si tout leurs successeurs ont été marqués, et on remonte jusqu'à la racine
    if({0}==Candidats): #temps constant : 2 comparaisons maxi...
        dA[0]=max([min([dA[v],dB[v]+cAB[v]]) for v in succ(0,Arbre)]) + tA[0]
        dB[0] = max([min([dB[v],dA[v]+cBA[v]]) for v in succ(0,Arbre)]) + tB[0]
        Marques.add(0) #inutile mais histoire d'avoir tout marqué...
        cpt += 1
        #print(cpt)
        return #la fonction pourrait faire un retour vide, ce qui compte c'est que dA et dB ont été modifiés
        
    NCandidats = set()
    if(len(Arbre)==len(Candidats)): #on rentre forcément dans ce cas pour le premier appel, car on prend Candidat = Arbre lors du premier appel
        Candidats = Feuille(Arbre) 
        for u in Candidats:
            dA[u] = tA[u]
            dB[u] = tB[u]
            #on ajoute les parents des feuilles qui seront utilisé dans l'appel récursif
            #ici on utilise le set car les feuilles peuvent partager le même parent
            if(succ(Arbre[u],Arbre)<=Candidats):#on ne retient que les candidats dont tout les 
                #successeurs ont été explorés. A <= B signifie A inclu dans B pour les set.
                #lors du premier appel les sommets marqués sont les feuilles=Candidats construit pour le premier appel
                NCandidats.add(Arbre[u])
        cpt += 1
        CalculBorneinf(Arbre,NCandidats,Candidats,tA,tB,cAB,cBA,dA,dB,cpt) #dA et dB ont été changées, ainsi que les candidats à calculer
    else: #cas où ce n'est ni le premier appel, ni le dernier. 
        for u in Candidats:
            dA[u] = max([min([dA[v],dB[v]+cAB[v]]) for v in succ(u,Arbre)]) + tA[u]
            dB[u] = max([min([dB[v],dA[v]+cBA[v]]) for v in succ(u,Arbre)]) + tB[u]
            Marques.add(u)
            #par construction les dA[v] et dB[v] ont bien leur valeur
            #encore une fois on ajoute uniquement si les successeurs des candidats ont tous été explorés.
            if(succ(Arbre[u],Arbre)<=Marques):
                NCandidats.add(Arbre[u]) #les prochains candidats sont les parents des candidats actuels. 
                #ceux qui n'ont pas été ajouté le seront forcément plus tard...
        cpt += 1
        CalculBorneinf(Arbre,NCandidats,Marques,tA,tB,cAB,cBA,dA,dB,cpt)


def Feuille(Arbre):
    L = [0]*len(Arbre)
    res= set()
    for i in range(len(Arbre)):
        L[Arbre[i]] = 1           
    for i in range(len(Arbre)):
        if(L[i]==0):
            res.add(i)
            
    return res
#les feuilles sont les i tels que L[i] = 0. Temps linéaire, 2 boucles.

def CalculSigmaOptimumAux(Arbre,tA,tB,cAB,cBA,dA,dB,Sigma,v):
    if(v==0):
        if (dA[0] <= dB[0]):
            Sigma[0]=1
        return Sigma[v]
    if(Sigma[Arbre[v]]==1):#u est dans A
        if(dA[v]<(dB[v]+cAB[v])):
            Sigma[v]=1
        else:
            Sigma[v]=0
        return Sigma[v]
    else:#u est dans B
        if(dB[v]>=(dA[v]+cBA[v])): #on inverse le test par rapport au sujet
            Sigma[v]=1
        else:
            Sigma[v]=0
        return Sigma[v]
def CalculSigmaOptimum2(Arbre,tA,tB,cAB,cBA,dA,dB,Sigma,Marques,u):
    """on considère sigma initialisé à 0 partout
    Marques est ici une liste de booleen : Marques[u] = 0 indique que Sigma[u] n'a pas été calculé"""
   
    Marques[u]=1
    Sigma[u] = CalculSigmaOptimumAux(Arbre,tA,tB,cAB,cBA,dA,dB,Sigma,u)
    for v in succ(u,Arbre):
        if(Marques[v]==0):
            CalculSigmaOptimum2(Arbre,tA,tB,cAB,cBA,dA,dB,Sigma,Marques,v)
    #ci-dessous version itérative
    """ f = []
    f.append(u)
    Marques[u]=1
    while(len(f)!=0):
        u = f.pop()
        CalculSigmaOptimumAux(Arbre,tA,tB,cAB,cBA,dA,dB,Sigma,u)
        for v in succ(u,Arbre):
            if(Marques[v]==0):
                f.append(v)
                Marques[v]=1"""




def CalculSigmaAlgo2(Arbre,tA,tB,cAB,cBA):
    """cette fonction utilise le deuxième algorithme pour calculer 
    l'allocation optimale. """
    dA = [0]*len(Arbre)
    dB = [0]*len(Arbre)
    CalculBorneinf(Arbre,Arbre,set(),tA,tB,cAB,cBA,dA,dB,0)
    Sigma = [0]*len(Arbre)
    Marques = [0]*len(Arbre)
    CalculSigmaOptimum2(Arbre,tA,tB,cAB,cBA,dA,dB,Sigma,Marques,0)
    return (Sigma,min(dA[0],dB[0]))




#jeux de tests : 

#num1
Arbre1 = [0, 0, 1, 2, 3]
tA1 = [5, 2, 3, 3, 2]
tB1 = [2, 5, 1, 8, 1]
cAB1 = [0,1, 4, 1, 2]
cBA1 = [0,2, 1, 4, 3]

#num2

Arbre2 = [0, 3, 0, 0, 2, 3, 2]
tA2 = [1, 3, 6, 3, 3, 2, 1]
tB2 = [2, 4, 5, 2, 3, 2, 4]
cAB2 = [0,2, 1, 2, 4, 1, 2]
cBA2 = [0,2, 1, 1, 2, 1, 1]

#num3

Arbre3 = [0, 0, 0, 0, 0, 0]
tA3 = [13, 10, 12, 13, 4, 1]
tB3 = [10, 15, 12, 9, 2, 3]
cAB3 = [0,4, 8, 1, 9, 2]
cBA3 = [0,7, 3, 8, 7, 5]

#num4

Arbre4 = [0, 6, 3, 0, 6, 0, 0, 3, 5, 5]
tA4 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
tB4 = [2, 1, 8, 2, 7, 3, 6, 4, 5, 10]
cAB4 = [0,4, 7, 5, 2, 3, 1, 1, 1, 5]
cBA4 = [0,3, 8, 4, 5, 3, 1, 2, 3, 2]

#num5

Arbre5 = [0, 4, 0, 4, 0]
tA5= [10, 7, 11, 5, 8]
tB5 = [12, 5, 10, 11, 3]
cAB5 = [0,2, 5, 6, 2]
cBA5 = [0,3, 4, 7, 1]
