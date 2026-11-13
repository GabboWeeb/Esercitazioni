class IntPair:
    def __init__ (self,a=0,b=0):
        """Costruttore"""
        self.a=a
        self.b=b
    def __str__(self):
        """override del metodo __str__"""
        return "({},{})".format(self.a,self.b)
    
    def mul(self):
        """restituisce il prodotto dei due interi"""
        assert isinstance(self.a,int), "Metti gli interi nella coppia"
        assert isinstance(self.b,int), "Metti gli interi nella coppia"
        return self.a*self.b

class IntPairK(IntPair):
    def __init__(self,a,b,k=0):
        super().__init__()
        self.k=k
    def __str__(self):
        """override del metodo __str__ della classe IntPairK"""
        return "({},{})".format(self.a,self.b)
    def mul(self):
        """restituisce il prodotto dei due interi"""
        assert isinstance(self.a,int), "Metti gli interi nella coppia"
        assert isinstance(self.b,int), "Metti gli interi nella coppia"
        assert isinstance(self.k,int), "Metti gli interi nella coppia"
        return self.a*self.b*self.k
    def __str__(self):
        """override del metodo __str__"""
        return "({},{};{})".format(self.a,self.b,self.k)
    
    

couple= IntPair(2,0)
print(couple)
print(couple.mul())

triple= IntPairK(2,0,1)
print(triple)
print(triple.mul())
