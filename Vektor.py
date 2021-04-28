import math,random


def vektornomieren(vektor):
    """Methode gibt normierten Vektor zurück

    Args:
        vektor (list): zu normierender Vektor

    Returns:
        list: normierter Vektor
    """
    leange = math.sqrt(vektor[0]**2+vektor[1]**2)
    return vektormult(vektor,1/leange)

def vektorleange(vektor):
    """Gibt die Länge des Vektors Zurück

    Args:
        vektor (list): Vektor

    Returns:
        float: Länge des vektors
    """
    return math.sqrt(vektor[0]**2+vektor[1]**2)

def vektormult(vektor,n):
    """Vektormultiplikation

    Args:
        vektor (list): Vektor  
        n (int): Zahl mit der multipliziert wird
    """

    return[vektor[0]*n,vektor[1]*n]

def matrixVektmult(matrix,vektor):
    """Matrix Vektor Multiplikation

    
    """

    return [matrix[0][0]*vektor[0]+matrix[0][1]*vektor[1],matrix[1][0]*vektor[0]+matrix[1][1]*vektor[1]]
def vektadd(v1,v2):
    """Vektor Addition

    """
    return[v1[0]+v2[0],v1[1]+v2[1]]


def vektsub(v1,v2):
    """Vektor Subtraktion
    """
    return[v1[0]-v2[0],v1[1]-v2[1]]


def rotationsmatrix(a):
    """Erstellt Rotationsmatrix für a Grad
    """
    alpha = math.radians(a)

    return  [[round(math.cos(alpha),5),round(-math.sin(alpha),5)],[round(math.sin(alpha),5),round(math.cos(alpha),5)]]


def vektscale(v,s):
    """Skaliert den Vektor um Faktor s
    """
    
    vn = vektornomieren(v)

    return vektormult(vn,s)

def randomnormiertvekt():
    """gibt zufälligen Einheitsvektor zurück

    """
   

    return matrixVektmult(rotationsmatrix(random.randint(0,360)),(1,0))

def vektrotation(vektor,a):
    """Gibt um a Grad rotierten Vektor zurück
    """

    return matrixVektmult(rotationsmatrix(a),vektor)

#kleine Testfunktion
def test():

    vektor = (1,0)
    rm = (rotationsmatrix(90))
    matrix = ([1,2],[3,4])
    print(rm)
    print(vektrotation(vektor,90))
    print(randomnormiertvekt())

if __name__ == "__main__":
    test()