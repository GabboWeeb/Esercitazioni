'''define a class Int Pair:
the main attributes will be two integers a and b '''

class IntPair:
    
    def __init__(self,a=1,b=1):
        self.a=a
        self.b=b
    
    def __str__(self):
        return f"({self.a},{self.b})"
    
    def mul(self):
        return(self.a*self.b)
    
class IntPairK(IntPair):
    
    def __init__(self,a=1,b=1,k=2):
        super().__init__(a,b)
        self.k=k
        
    def __str__(self):
        return f"({self.a},{self.b},{self.k})"
    
    def mul(self):
        return(self.a*self.b*self.k)
    


couple=IntPair(1,1)
print(couple)
print(couple.mul())


couple2=IntPairK(2,3,4)
print(couple2)
print(couple2.mul())
