"""
radici di un'eq di 2° grado
"""

import math

print("ax^2 + bx + c = 0")
a=float(input("dimmi un numero: ").replace(',','.'))


print("%.2fx^2 + bx + c = 0" % (a))
b=input("dimmi un numero: ")
b=float(b.replace(',','.'))

print("%.2fx^2 + %.2fx + c = 0" % (a,b))
cstr=input("dimmi un numero: ")
c=float(cstr.replace(',','.'))
print("%.2fx^2 + %.2fx + %.2f = 0" % (a,b,c))

delta=b**2-4*a*c

if delta>0:
    delta=math.sqrt(delta)
    x1,x2=(-b+delta)/(2*a),(-b-delta)/(2*a)
    print("L'equazione ha due radici distinte in %f e in %f" % (x1,x2))
elif delta==0:
    x1=-b/2*a
    print("L'equazione ha due radici coincidenti in %f" % (x1))
else:
    delta=math.sqrt(-delta)
    re1=-b/(2*a)
    im1=delta/(2*a)
    im2=-delta/(2*a)
    print("Le radici sono immaginarie: %f %f*i e %f %f*i" % (re1,im1,re1,im2))