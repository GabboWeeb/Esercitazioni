"""
Calcolo di interesse composto
"""

cap= float(input ('Dimmi un capitale iniziale: '))
tasso= float(input ('Dimmi un tasso: '))
yr= int(input ('Dimmi il numero di anni: '))

importo_finale=cap*(1+tasso/100)**yr

print(importo_finale)




