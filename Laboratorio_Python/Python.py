#Buono Gabriele
def rilevamento_duplicati(rcvpkt): #rcvpkt -> lista contenente gli identificativi dei pacchetti
    setid = set() #set di identificativi comparsi piu' di una volta
    listpkt = [] #lista che conterra' la prima occorrenza preservando l'ordine
    
    for pkt in rcvpkt:
        if pkt in setid:
            print("duplicato: ", pkt)
        else:
            setid.add(pkt) #aggiorno il set
            listpkt.append(pkt) #aggiorno la lista
    #print(setid)
    print(listpkt)
    
rilevamento_duplicati([1,2,3,4,4,4,5,3,2,5,6])
#############################################################
#rcvip e' una sequenza/lista di indirizzi IP. K e' il valore che indica il numero di accessi che si possono effettuare prima di risultare sospetti
def analisi_accessi(rcvip,k): 
    setsospetti = set() #set -> ip sospetti
    listcont = [] #lista di liste che contiene ip e numero di accessi
    
    for ip in rcvip:
        if (rcvip.count(ip) > k) and (not(ip in setsospetti)): #se il numero di occorrenze e' maggiore di k e l'ip che sto visionando non si trova nel setsospetti
            print("L'ip ",ip," ha effettuato piu di ", k, " accessi")
            setsospetti.add(ip) #aggiorno set
            listcont.append([ip,rcvip.count(ip)]) #aggiungo la coppia IP + Contatore di accessi
    print(setsospetti)
    print(listcont)
        
        
analisi_accessi(["IP1","IP2","IP3","IP4","IP3","IP2","IP5","IP2","IP6","IP6","IP6"],2)
#############################################################
def max_window(idprocess): #sequenza/lista di identificativi di processi
    listcontigua = []
    indiceiniziale = 0
    maxfinale = 0
    maxlunghezza = 0
    
    for idpindice in range(len(idprocess)):
        
        while idprocess[idpindice] in listcontigua:
            listcontigua.remove(idprocess[indiceiniziale])
            indiceiniziale = indiceiniziale +1
        
        listcontigua.append(idprocess[idpindice])
        
        lunghezza = len(listcontigua)
        
        if lunghezza > maxlunghezza:
            maxlunghezza = lunghezza
            maxfinale = idpindice
            
    print(listcontigua)

max_window([1,2,3,4,5,11,7,1,12,14,15,16,11,30,40,1,31,32,33,34,35,36])
#############################################################
def confronto_sistemi(sys1,sys2,sys3):
    setsys1, setsys2, setsys3 = set(), set(), set()
    listunion = []
    listtre = []
    listdue = []
    listuno = []
    
    setsys1.update(sys1)
    setsys2.update(sys2)
    setsys3.update(sys3)
    
    listunion = list(setsys1 | setsys2 | setsys3)
    
    for log in listunion:
        presenza = 0

        if log in setsys1:
            presenza = presenza +1
        if log in setsys2:
            presenza = presenza +1
        if log in setsys3:
            presenza = presenza +1

        if presenza == 3:
            listtre.append(log)
        elif presenza == 2:
            listdue.append(log)
        elif presenza == 1:
            listuno.append(log)

    print("Unione: ",listunion)
    print("tre: ",listtre)
    print("due: ",listdue)
    print("uno: ",listuno)

confronto_sistemi([1,2,3,4,5,6,7,8],[1,2,4,6,8,9,10],[2,3,4,5,7,9,10,11])
#############################################################
def analisi_richieste(requestlist):
    sequenza = []
    listcontigua = []
    primo = True
    
    for i in range(0, len(requestlist)):
        if primo:
            sequenza.append(requestlist[i])
            primo = False
        else: 
            if requestlist[i-1] < requestlist[i]:
                sequenza.append(requestlist[i])
            else:
                listcontigua.append(sequenza)
                sequenza = [requestlist[i]]
    listcontigua.append(sequenza)
    sequenza = [requestlist[i]]
    
    lunghezzamax = len(listcontigua[0])
    for i in range(1, len(listcontigua)):
        lunghezza = len(listcontigua[i])
        if(lunghezzamax < lunghezza):
            lunghezzamax = lunghezza
            differenza = listcontigua[i][0]-listcontigua[i][lunghezzamax-1]
    
    print("la lunghezza della sequenza piu lunga e': ", lunghezzamax)
    print("La differenza tra il primo elemento e l'ultimo della sequenza piu lunga e': ", differenza)
    print(listcontigua)
analisi_richieste([1,2,3,4,2,3,4,5,3,4,5,6,7,4,5,6,7,8,9,2,3,4,5,6,7,8,9,10,11])