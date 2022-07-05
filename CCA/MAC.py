import math
import numpy as np
from PRG import PRG
from PRF import PRF
from CPA import CPA

class MAC():
    def __init__(self, t):
        self.mode = t
    
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
                

    def mac_simple(self, prg, prf, m, k=None):
        n = len(m)

        if k is None:
            k = self.genKey(n)
        t = ""
        print("In mac: ", len(k), len(m))
        t = prf.prf_basic(prg, k, m)
        return t 

    def mac(self, prg, prf, m, n=None, k=None):
        l = len(m)
        if n is None:
            if k is not None:
                n = len(k)
            else:
                n = int(4*math.floor(math.log2(l)))

        pad = n - l%n
        if pad != n:
            for i in range(pad):
                m = m + "0"
        else:
            pad = 0
        
        print("length of msg in mac:", l, n, pad, len(k))

        
        l_str = prf.binstring(l)
        l_str = prf.setStrLen(l_str, int(n/4))

        if k is None:
            k = self.genKey(n)
        #print(k)
        r = self.genKey(int(n/4))
        d = int(4*(l+pad)/n)
        t = r
        ti = ""
        #print("In mac.mac:",d, d*(n/4), l, n, r)
        for i in range(d):
            i_str = prf.binstring(i)
            i_str = prf.setStrLen(i_str, int(n/4))

            mi = m[int(i*(n/4)):int((n/4)*(i+1))]
            inp = r + l_str + i_str + mi
            if len(inp) != len(k):
                print(k, inp, r, l_str, i_str, mi)
            #print("Length: ", len(inp), len(mi), len(l_str), len(i_str), len(r), n)
            ti = self.mac_simple(prg,prf,m = inp, k= k)
            t = t + ti
        #print("Length of t in mac.mac:",len(t))
        return t
    
    def mac_vrfy(self, prg, prf, k, m, t):
        l = len(m)
        n = len(k)
        pad = n - l%n
        if pad != n:
            for i in range(pad):
                m = m + "0"
        l = len(m)
        tl = len(t)
        d = int((4*l)/n)
        d1 = int((tl - int(n/4))/n)
        '''
        if n < int(4*math.floor(math.log2(l))):
            print("Due to condition 1")
            return -1
        
        if d != d1:
            print("Due to condition 2", d, d1, l ,tl, n)
            return -1
        '''        
        r = t[0:int(n/4)]
        l_str = prf.binstring(l)
        l_str = prf.setStrLen(l_str, int(n/4))
        t1 = r
        
        for i in range(d):
            i_str = prf.binstring(i)
            i_str = prf.setStrLen(i_str, int(n/4))
            
            mi = m[int(i*(n/4)):int((n/4)*(i+1))]
            inp = r + l_str + i_str + mi
            ti = self.mac_simple(prg,prf,inp, k)
            t1 = t1 + ti
        print("In mac.vrfy",d, r, len(t1), len(t))
        #print(t1, t)
        if t1 == t:
            return 1 # THIS IS NOT HAPPENING ---- RECHECK -----
        return -1

if __name__ == "__main__":   
    g, p = input("Please enter g and p values(for discrete logarithm): ").split()
    g = int(g)
    p = int(p)

    prg = PRG(g, p)

    prf = PRF()
    cpa = CPA(0)

    mac = MAC(0)

    s = input("Please enter input binary string for generating MAC: ")
    k = input("Please input key for mac: ")
    if k == 0:
        print("Generated MAC: ", mac.mac_simple(prg, prf, s))
    else:
        print("Generated MAC: ", mac.mac_simple(prg, prf, s, k=k))
        
            





            
