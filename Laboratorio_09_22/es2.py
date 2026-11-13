"""
Conteggio delle cifre
"""
"""
n=int(input("Dimmi un numero: "))
#non avrebbe controllato se il numero è negativo
x=n

cifre=0

while x>1:
    x=x/10
    cifre+=1
    print(x)
print("Il numero " , n , " ha ", cifre, " cifre." )
"""

n=input("Dimmi un numero: ")
while n.isdigit()==0:
    print("Inserisci solo numeri positivi!")
    n=input("Dimmi un numero: ")

#int(1n)>0
#n[0]!='-'
print("Il numero %s ha %d cifre" % (n,len(n)))

#print(n+" ha ", len(n), " cifre.")    




