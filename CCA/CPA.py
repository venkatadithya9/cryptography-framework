import math
import numpy as np
from PRG import PRG
from PRF import PRF

class CPA():
    def __init__(self, t):
        self.mode = t

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
    
    def rcm(self, prg, prf, l, m, k = None): #RE CHECK
        #print(len(m))
        if len(m)%l != 0:
            print("Length of the input stream must be a multiple of l")
            return -1

        n = int(len(m)/l)
        
        if k is None:
            k = self.genKey(n)
        else:
            n = len(k)
        print("n calculated:",n)
        
        
        c_full = ""
        iv = np.random.randint(0,2**n)
        ctr = ""
        iv_init = iv

        for i in range(l):
            iv = (iv + 1)%(2**n)
            ctr = self.binstring(iv)
            if len(ctr) != n:
                ctr = self.setStrLen(ctr, n)
                print(len(ctr), n, ctr)
            
            mi = m[int(i*n):int(n*(i+1))]
            print(len(k), k)
            c = prf.prf_basic(prg, k, ctr)
            #print(len(c))
            if c != -1:
                c = self.binstring((self.getint(c))^(self.getint(mi)))
            else:
                print("ERROR in getting PRF", ctr, len(ctr), n, l, len(m))
            if len(c) != n:
                c = self.setStrLen(c, n)
            c_full = c_full + c
        
        return c_full, iv_init, k
    
    def ofb(self, prg, prf, l, m, k=None):
        if len(m)%l != 0:
            print("Length of the input stream must be a multiple of l")
            return -1

        n = len(m)/l
        
        if k is None:
            k = self.genKey(n)
        
        c_full = ""
        iv = np.random.randint(0,2**n)
        iv_init = iv
        iv_str = self.binstring(iv)
        if(len(iv_str) != n):
            iv_str = self.setStrLen(iv_str, n)

        for i in range(l):
            iv_str = prf.prf_basic(prg, k, iv_str)
            c = ""
            if iv_str != -1:
                #c = self.binstring((self.getint(c))^(self.getint(m[int(n*i):int(n*(i+1))])))
                c = self.getxor(iv_str, m[int(n*i):int(n*(i+1))])
            if len(c) != n:
                c = self.setStrLen(c, n)
            c_full = c_full + c
        
        return c_full, iv_init, k

    #DECRYPTION FOR EACH OF THESE SECURE MODES

    def rcm_dec(self, prg, prf, iv_init, k, c):
        iv = iv_init
        n = len(k)
        l = int(len(c)//n)

        m_full = ""
        ctr = ""
        iv = iv_init 

        for i in range(l):
            iv = (iv + 1)%(2**n)
            ctr = self.binstring(iv)
            if len(ctr) != n:
                ctr = self.setStrLen(ctr, n)
            
            ci = c[int(i*n):int(n*(i+1))]
            m = prf.prf_basic(prg, k, ctr)
            #print(len(c))
            if m != -1:
                m = self.binstring((self.getint(m))^(self.getint(ci)))
            
            if len(m) != n:
                m = self.setStrLen(c, n)
            m_full = m_full + m
        
        return m_full

if __name__ == "__main__":
    g, p = input("Please enter g and p values(for discrete logarithm): ").split()
    g = int(g)
    p = int(p)

    prg = PRG(g, p)

    prf = PRF()
    cpa = CPA(0)

    l, num = input("Please enter the length of input stream and length of cipher block: ").split()
    l = int(l)
    num = int(num)
    inp = input("Please enter input stream for PRF: ")
    c_full, iv_init, k = cpa.rcm(prg, prf, int(l/num), inp)
    print("Output: ",c_full)

    #print("Decrypted message: ", cpa.rcm_dec(prg, prf, iv_init, k, c_full))
