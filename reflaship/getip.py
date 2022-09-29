def getip():
    fname = 'reflaship/ip.txt'
    f = open(fname,'r')
    ip = f.readline()
    f.close()
    f = open(fname,'w')
    f.write('')
    f.close()
    return ip
#print(getip())