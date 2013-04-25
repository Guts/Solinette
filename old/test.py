i =0
print 'youpi'
truc = test
while i <len(truc):
    f = truc[i][0].decode('utf8').rstrip()
    truc.remove(truc[i])
    #try: # para guadar enteros ,por ejemplo en el caso de los id
        #lista.insert(i,int(f))
    #except:
    truc.insert(i, f)
    i = i+1
# End of function

for i in range(len(truc)):
    try:
        truc[i][0].decode('utf8').rstrip()
    except UnicodeDecodeError:
        unicode(truc[i][0].decode('tatin1').rstrip())


