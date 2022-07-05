import math
class PRG():
    def  __init__(self, g, p):
        self.g = g
        self.p = p
        self.n = 0
    
    def setInputLen(self, x):
        self.n = len(x)
    
    def setStrLen(self, s, n):
        if len(s) < n:
            for i in range( int(n- len(s))):
                s = "0" + s
        elif len(s) > n:
            s = s[0:n]

        return s

    def binstring(self, x):
        out = ""
        i =0
        while(x > 0):
            i+=1
            if x%2 == 1:
                out = "1" + out
            else:
                out = "0" + out
            x = int(x/2)
        #print(out, i, x)
        out = self.setStrLen(out, self.n)
        return out

    
    def dlp(self, x):
        num = int(x, 2)
        ans = ((self.g)%(self.p))**(num)
        #print("giving binstring = ",ans%(self.p) )
        return self.binstring(ans%(self.p))

    def msb(self, x):
        if int(x,2) <= (p-1)/2:
            return "1"
        else:
            return "0"
    
    def prg_1(self, s):
        self.setInputLen(s)
        ans = self.dlp(s)
        ans = ans + self.msb(s)
        return ans
    
    def encrypt(self, x, expFactor):
        t = x
        out = ""

        for i in range(expFactor):
            t = self.prg_1(t)
            out = out + t[len(t)-1]
            t = t[:-1]
        
        return out

if __name__ == "__main__":
    g, p = input("Please enter g and p values(for discrete logarithm): ").split()
    g = int(g)
    p = int(p)

    prg = PRG(g, p)
    s = input("Input seed as binary string: ")
    expFactor = int(input("Input desired output length: "))
    print("Output: ", prg.encrypt(s, expFactor))


