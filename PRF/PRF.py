import numpy as np
import math
from PRG import PRG


class PRF():
    def __init__(self):
        pass

    def binstring(self, x):
        n = 0
        if x != 0:
            n = math.floor(math.log(x))
        else:
            x += 1
            n = math.floor(math.log(x))

        mask = int(1)
        x = int(x)
        out = ""
        for i in range(n):
            if (mask&x) >= 1:
                out = "1" + out
            else:
                out = "0" + out
            mask = mask*2
        return out
    
    def genKey(self, n):
        toss = np.random.randint(0,2)
        out = "1"
        while(len(out) < n):
            if toss == 0:
                out = out + "0"
            else:   
                out = out + "1"
            toss = np.random.randint(0,2)
        return out
    
    def getint(self, s):
        n = len(s)
        num = 0
        for i in range(n):
            if(s[i] == '1'):
                num += (2**(n-i-1))
        return num

    def setStrLen(self, s, n):
        if len(s) < n:
            for i in range( int(n- len(s))):
                s = "0" + s
        elif len(s) > n:
            s = s[0:n]

        return s

    def getxor(self, s1, s2):
        n = len(s1)
        if len(s1) != len(s2):
            print("Strings must be of same length")
            return -1
        out = ""
        for i in range(n):
            if s1[i] == s2[i]:
                out = out + "0"
            else:
                out = out + "1"
        return out

    def prf_basic(self, prg, k, x):
        n = len(k)
        if len(x) != n:
            print("Input and key must be of same length")
            print(n , len(x))
            return -1
        
        out = k
        G = ""

        for i in range(n):
            G = prg.encrypt(out, 2*n)
            if x[i] == '0':
                out = G[:n]
            else:
                out = G[n:]
        
        return out


    def cpa(self, prg, m, k=None):
        n = len(m)
        
        if k is None:
            k = self.binstring(np.random.randint(0,(2**n)))
            if len(k) != n:
                k = self.setStrLen(k, n)

        r = self.binstring(np.random.randint(0,(2**n)))
        if len(r) != n:
            r = self.setStrLen(r,n)

        F_r = self.prf_basic(prg, k, r)
        #num = self.getint(F_r) ^ self.getint(m)
        c = self.getxor(F_r, m)
        c = r + c
        return c

    def cpa_dec(self, prg, c, k):
        n = int(len(c)/2)
        r = c[0:n]
        F_r = self.prf_basic(prg, k, r)
        tmp = c[n:]
        m = self.getxor(F_r, tmp)
        return m

if __name__ == "__main__":
    g, p = input("Please enter g and p values(for discrete logarithm): ").split()
    g = int(g)
    p = int(p)

    prg = PRG(g, p)

    prf = PRF()

    m = input("Please input message in binary format: ")
    k = input("Please input key in binary format: ")
    print("Output: ", prf.prf_basic(prg,k,m))
