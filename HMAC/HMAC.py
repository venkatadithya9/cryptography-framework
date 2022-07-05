import numpy as np
import math

from PRG import PRG
from PRF import PRF
from CPA import CPA
from MAC import MAC
from hash import Hash

class HMAC():
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
    
    def setStrLen(self, s, n):
        if len(s) < n:
            for i in range( int(n- len(s))):
                s = "0" + s
        elif len(s) > n:
            s = s[0:n]

        return s

    def getint(self, s):
        n = len(s)
        num = 0
        for i in range(n):
            if(s[i] == '1'):
                num += (2**(n-i-1))
        return num
    
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

    def hmac(self, hash, m, k): # k must be a binstring
        n = int(len(k))
        pad = n - (len(m))%n
        
        for i in range(pad):
            m  = m + "0"
        iv_str = self.genKey(n)
        iv = self.getint(iv_str)
        ipad = self.binstring(54)
        b = len(ipad)
        tmp = ipad
        while len(tmp) < n - b:
            tmp = tmp + ipad 
        ipad = self.setStrLen(tmp, n)
        opad = self.binstring(92)
        b = len(opad)
        tmp = opad
        while len(tmp) < n - b:
            tmp = tmp + opad 
        opad = self.setStrLen(tmp, n)

        m1 = self.getxor(k,ipad) + m
        h1 = hash.hash_final(m1, iv, n)
        m2 = self.getxor(k, opad) + h1
        t = hash.hash_final(m2, iv, n)
        return t

if __name__ == "__main__":
    g, p = input("Please enter g and p values(for discrete logarithm): ").split()
    g = int(g)
    p = int(p)

    prg = PRG(g, p)

    prf = PRF()
    cpa = CPA(0)

    mac = MAC(0)
    hash = Hash()
    hmac = HMAC()

    m = input("Please input message stream: ")
    k = input("Please input key string: ")
    print("Generated H-MAC: ", hmac.hmac(hash, m, k))