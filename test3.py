import math

class Vektor():
    @staticmethod
    def vektornomieren(vektor):
        leange = math.sqrt(vektor[0]**2+vektor[1]**2)
        return Vektor.vektormult(vektor,1/leange)
    
    @staticmethod
    def vektormult(vektor,n):
        return(vektor[0]*n,vektor[1]*n)
    
    @staticmethod
    def vektadd(v1,v2):
        return(v1[0]+v2[0],v1[1]+v2[1])

    

v  = (2,8)
print(Vektor.vektormult(v,2))

v2 = Vektor.vektornomieren(v)
print(v2)
print(math.sqrt(v2[0]**2+v2[1]**2))
print(Vektor.vektadd(v,v2))