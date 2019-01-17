# -*- coding: utf-8 -*-
"""
Created on Sun Dec  9 14:41:55 2018

@author: Serge Durand et Arthur Limbour
ce fichier contient des fonctions de tests divers, de première ébauches etc.
"""

#Algo 2 version récursion croisée. Exponentiel
def CalculdA(Arbre,tA,tB,cAB,cBA,dA,dB,u):
    Succ = succ(u,Arbre)
    if(len(Succ)==0):
        dA[u]=tA[u]
        return dA[u]
    
    else:
        dA[u] = max([min([CalculdA(Arbre,tA,tB,cAB,cBA,dA,dB,v),CalculdB(Arbre,tA,tB,cAB,cBA,dA,dB,v)+cAB[v]]) for v in Succ]) + tA[u]
        return dA[u]
def CalculdB(Arbre,tA,tB,cAB,cBA,dA,dB,u):
    Succ = succ(u,Arbre)
    if(len(Succ)==0):
        dB[u] = tB[u]
        return tB[u]
    else:
        dB[u] =  max([min([CalculdB(Arbre,tA,tB,cAB,cBA,dA,dB,v),CalculdA(Arbre,tA,tB,cAB,cBA,dA,dB,v)+cBA[v]]) for v in Succ]) + tB[u]
        return dB[u]
    
def CalculBorneInf2(Arbre,tA,tB,cAB,cBA,dA,dB):
        CalculdA(Arbre,tA,tB,cAB,cBA,dA,dB,0)
        CalculdB(Arbre,tA,tB,cAB,cBA,dA,dB,0)
        return(dA,dB)


#tests sur la fonction Delta
def testCalculDelta(n): #réalisation d'un test sur un seul arbre généré aléatoirement
    Arbre = CalculArbreDroit(n)
    (tA,tB,cAB,cBA) = InstanceAleatoire(n,50)
    sigma = [random.randrange(2) for i in range(n)]
    tdep = time.perf_counter_ns()
    CalculDelta(Arbre,tA,tB,cAB,cBA,sigma,0)
    tfin = time.perf_counter_ns()-tdep
    return tfin
    
def testMasseCalculDelta(n,p): #réalisation de plusieurs tests 
    """n = taille finale des arbres
    p = pas. si p = 1 on fait des tests sur tout les arbres. 
    si on veut tester une grande plage de valeur pour n c'est
    intéressant d'augmenter la valeur de p. 
    """
    Ln = []
    Ltemps= []
    #en cas de valeurs absurde sur les petites tailles initialiser le premier i plus haut
    i = 2
    while(i<n):
        res=0
        temp = []
        for j in range(100): #pour lisser les valeurs hors normes
            #baisser cette valeur si les tests prennent trop de temps...
            temp.append(testCalculDelta(i))
        res=np.median(temp)    
        Ltemps.append(res)
        Ln.append(i)
        i=i+p
        
    return(Ln,Ltemps)
    
#les deux fonctions suivantes servent à faire le test pour des arbres à 2 étages : 
#toutes les tâches sont reliées à la tâche 0.
def testCalculDelta2(n):
    Arbre = CalculArbreh2(n)
    (tA,tB,cAB,cBA) = InstanceAleatoire(n,50)
    sigma = [random.randrange(2) for i in range(n)]
    tdep = time.clock()
    CalculDelta(Arbre,tA,tB,cAB,cBA,sigma,0)
    tfin = time.clock()-tdep
    return tfin
    
def testMasseCalculDelta2(n,p):
    """n = taille finale des arbres
    p = pas
    """
    Ln = []
    Ltemps= []
    #en cas de valeurs absurde sur les petites tailles initialiser le premier i plus haut
    i = 2 
    while(i<n):
        res=0
        temp = []
        for j in range(100): #pour lisser les valeurs hors normes
            temp.append(testCalculDelta2(i))
        res=np.median(temp)    
        Ltemps.append(res)
        Ln.append(i)
        i=i+p
    return(Ln,Ltemps)
 

#ici on travaille sur les arbres binaires. h est la hauteur.
def testCalculDelta3(h):
    Arbre = CalculArbreComplet(h)
    n = len(Arbre)
    (tA,tB,cAB,cBA) = InstanceAleatoire(n,50)
    sigma = [random.randrange(2) for i in range(n)]
    tdep = time.clock()
    CalculDelta(Arbre,tA,tB,cAB,cBA,sigma,0)
    tfin = time.clock()-tdep
    return tfin


def testMasseCalculDelta3(h): 
    """n = taille finale des arbres
    p = pas
    """
    Ln = []
    Ltemps= []
    #on commence à h = 2 pour éviter les valeurs minuscules
    i = 2 
    while(i<=h):
        res=0
        temp = []
        for j in range(10): #pour lisser les valeurs hors normes
            temp.append(testCalculDelta3(i))
        res=np.median(temp)    
        Ltemps.append(res)
        Ln.append(i)
        i=i+1 #on augmente la taille exponentiellement, le pas de 1 suffit largement...
    
    return(Ln,Ltemps)
    
def scatter(L1,L2): #idem mais sous la forme d'un nuage de point
    x = np.array(L1)
    y = np.array(L2)
    plt.scatter(x,y)
    plt.show()

def graphe_line(L1,L2):
    x = np.array(L1)
    y = np.array(L2)
    y = np.array([j/i for i,j in zip(x,y)])
    plt.plot(x,y,label="lineaire")
    plt.legend()
    plt.show()

def graphe_quadra(L1,L2):
    x = np.array(L1)
    y = np.array(L2)
    y = np.array([j/i for i,j in zip(x,y)])
    y = np.array([j/i for i,j in zip(x,y)])
    plt.plot(x,y,label="quadra")
    plt.legend()
    plt.show()
    
def graphe_expo(L1,L2):
    x = np.array(L1)
    y = np.array(L2)
    y = np.array([j/(2**i) for i,j in zip(x,y)])
    plt.plot(x,y,label="expo")
    plt.legend()
    plt.show()
    
def graphe_nlogn(L1,L2):
    x = np.array(L1)
    y = np.array(L2)
    y = np.array([j/(i*(math.log(i))) for i,j in zip(x,y)])
    plt.plot(x,y,label="n log(n)")
    plt.legend()
    plt.show()
    
def graphe_nsqrtn(L1,L2):
    x = np.array(L1)
    y = np.array(L2)
    y = np.array([j/(i**2.5) for i,j in zip(x,y)])
    plt.plot(x,y,label="n sqrt(n)")
    plt.legend()
    plt.show()

#donne la courbe théorique linaire modulo une constante. (ce n'est pas juste y = x, mais y = ax)...
#même logique pour quadra2, c'est une courbe théorique calculée que sur les n, pas sur les mesures.
#utilitée : comparer avec le graphe. 

def graphe_line2(L1,L2):
    x = np.array(L1)
    c = np.median(L2)/np.median(L1)
    y = x*c
    plt.plot(x,y,label="lineaire 2")
    plt.legend()
    plt.show()
    
def graphe_quadra2(L1,L2):
    x = np.array(L1)
    y = np.array([i**2 for i in x])
    plt.plot(x,y,label="quadra 2")
    plt.legend()
    plt.show()	
def ParcoursLargeur(Arbre,u,marques):
    f = []
    f.append(u)
    marques[u]=1
    while(len(f)!=0):
        u = f.pop()
        print(u)
        for v in succ(u,Arbre):
            if(marques[v]==0):
                f.append(v)
                marques[v]=1

def ParcoursProfondeur(Arbre,u,marques):
    marques[u]=1
    print(u)
    for v in succ(u,Arbre):
        if(marques[v]==0):
            ParcoursProfondeur(Arbre,v,marques)