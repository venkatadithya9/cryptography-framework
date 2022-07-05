import numpy as np
import math

class Hash():
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

    def G(self, n, num):
    #from n find value of (2^(n+1) - 1) and 2^(n)
    #find all multiples of 8 in this range
    #randomly choose one multiple of 8 and get p = multiple of 8 -1
    # q = (p-1)/2
    # pick a random number h such that h^((p-1)/q) != 1
    # Then g = 2 will give G with order q
        max_lim = int(2**(n+1))//8
        min_lim = int(2**(n))//8
        if max_lim*8 - 1 < 2*num + 1:
            print("G cannot be found")
            return -1
        else:
            min_lim = max(2*num + 1, 2**n)//8
        print("In G: ",max_lim*8 - 1, min_lim*8 - 1, 2*num + 1, n)
        p = (np.random.randint(min_lim, max_lim))*8 - 1
        while p < 2*num + 1:
            p = (np.random.randint(min_lim, max_lim + 1))*8 - 1
        q = int((p-1)/2)
        
        h = np.random.randint(0, p - 1)
        chk = h**((p-1)/q)

        while chk == 1:
            h = np.random.randint(0, p - 1)
            chk = (h**((p-1)/q))%p

        grp = []
        g = chk
        print(g,q,p)

        print("Generating group")
        while True:
            grp.append(g)
            if g!= 1:
                print(g)
            g = int((g*g)%p)
            #print(g)
            if g == 2:
                break

        ind = np.random.randint(0, len(grp))
        return p, q, g, grp[ind]
    
    def gcd(self,a ,b):
        if (a == 0):
            return b
        return self.gcd(b % a, a)

    def G_add(self, n, num):
        max_lim = 2**(n)
        min_lim = min(num, 2**(n-1))
        q = min_lim + np.random.randint(max_lim-min_lim)
        g = 1
        for i in range(2, q):
            if (self.gcd(i, q) == 1):
                g = i
                break
        ind = np.random.randint(max_lim-min_lim)
        h = 0 + ind
        return q, q, g, h

    def G_final(self):    
        out = []
        p = 52981
        key_value = len(bin(p)) - 2
        tmp = (1, p-1)
        out.append(tmp)
        q = (p-1)//2
        out.append(q)
        x = np.random.randint(2, p-2)
        out.append((x**2)%p)
        h = np.random.randint(1, q-1)
        out.append(h)
        return out

    def hash_simple(self, n, x):
        x1 = self.getint(x[0:n])
        x2 = self.getint(x[n:2*n])
        s = self.G_final()
        #print(s)
        q = s[1]
        out = bin((pow(s[2], x1, q)*pow(s[3], x2, q))%q)[2:].zfill(len(bin(52981)) - 2)
        #out = self.binstring(out)
        if len(out) != n:
            out = self.setStrLen(out, n)
        return out
       
    def hash_final(self, x, iv= None, n = None):
        l = len(x)
        if n is None:
            n = len(bin(52981)) - 2
        
        pad = n - l%n
        for i in range(pad):
            x = x + "0"
        
        if iv is None:
            iv_str = self.genKey(n)
            iv = self.getint(iv_str)
        else:
            iv_str = self.binstring(iv)
        if len(iv_str) != n:
            iv_str = self.setStrLen(iv_str, n)
        zi = iv_str
        #p  rint("Entering for loop")
        for i in range(int(len(x)/n)):
            xi = x[i*n:n*(i+1)]
            tmp = xi + zi
            zi = self.hash_simple(n, tmp)
            print("zi=",zi, i)
        
        return zi
    


if __name__ == "__main__":
    hash = Hash()
    n = int(input("Please enter desired length of the output hash: "))
    m = input("Please input message string: ")

    print("Hash generated : ", hash.hash_simple(n, m))
