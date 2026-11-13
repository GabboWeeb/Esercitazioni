x="global "

def foo():
    global x
    y="local"
    x=x*2
    print("x: ",x,"\ny: ",y)

print(foo())