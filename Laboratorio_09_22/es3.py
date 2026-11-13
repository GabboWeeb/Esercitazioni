"""
Fattoriale di un numero
"""

n=input("Dimmi un numero: ")
while not n.isdigit():
    print("Inserisci SOLO interi positivi, senza segno.")
    n=input("Dimmi un numero: ")
    
acc=1
for i in range(1,int(n)+1):
    acc=acc*i
    
print("%s! = %d" %(n,acc))    
