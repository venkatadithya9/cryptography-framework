import math
import numpy as np
from PRG import PRG
from PRF import PRF
from CPA import CPA
from MAC import MAC

class CCA():
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
                

    def cca(self, prg, prf, cpa, mac, n, m):
        k1 = self.genKey(n)
        k2 = self.genKey(n)
        m_len = len(m)
        if m_len%n != 0:
            pad = n - m_len%n
            for i in range(pad):
                m = m + "0"
        print(len(m))
        m_len = len(m)
        l = int(m_len/n)
        if self.mode == 0:
            #print("In cca.cca:",l, n, m_len)
            #print(type(l), type(m), type(k1))
            c, iv_init, k1 = cpa.rcm(prg, prf, l, m, k1)
        else:
            c, iv_init, k1 = cpa.ofb(prg, prf, l, m, k1)
        
        print("length of cipher: ", len(c))
        #Encrypt then authenticate
        t = mac.mac(prg, prf, c , n = n, k = k2)
        if t == -1:
            print("MAC error")
            return -1
        out = c + t
        print("In cca", len(c), len(t))
        return out, iv_init, k1, k2, m_len

    def cca_dec(self, prg, prf, cpa, mac, k1, k2, cip, iv_init, m_len):
        n = int(len(k1))
        c = cip[0:m_len]
        t = cip[m_len:]
        print(len(cip), len(c), len(t))
        if mac.mac_vrfy(prg, prf, k2, c, t) == 1:
            if self.mode == 0:
                m = cpa.rcm_dec(prg,prf, iv_init, k1, c)
                return True
            else:
                m = cpa.ofb_dec(prg,prf, iv_init, k1, c)
                return True
        else:
            return False

if __name__ == "__main__":
    g, p = input("Please enter g and p values(for discrete logarithm): ").split()
    g = int(g)
    p = int(p)

    prg = PRG(g, p)

    prf = PRF()
    cpa = CPA(0)

    mac = MAC(0)
    cca = CCA(0)

    m = input("Please input message for CCA: ")
    bl_sz = int(input("Please input block size: "))
    out, iv_init, k1, k2, m_len = cca.cca(prg, prf, cpa, mac, bl_sz, m)
    print("Output cipher: ", out)
    print("Decryption output: ", cca.cca_dec(prg, prf, cpa, mac, k1, k2, out, iv_init, m_len))
