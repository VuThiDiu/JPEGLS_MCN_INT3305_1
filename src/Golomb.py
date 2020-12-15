import math
import numpy as np
from Bits import *
import math
class Golomb:
    def Encode(self, byteManager, k, Merrval, limit,  qbpp):
        M = np.int32(2**k)
        x = np.int32(math.floor(Merrval / M))
        r = int (Merrval % M)
        if (x < limit - qbpp - 1):
            for i in range (x): 
                byteManager.add(0)
            byteManager.add(1)
            comp = np.int32(2**(k-1))
            for i in range(k,0,-1): 
                if ((comp & r) == comp):
                    byteManager.add(1)
                else:
                    byteManager.add(0)
                
                r <<= 1
            
        else:
            for i in range(limit - qbpp - 1):
                byteManager.add(0)
            
            byteManager.add(1)
            Merrval -= 1
            for i in range(qbpp, 0, -1):
                if ((128 & Merrval) == 128):
                    byteManager.add(1)
                else:
                    byteManager.add(0)
                Merrval <<= 1
        return byteManager    
        
    def Decode (self, data, M):
        q = 0
        nr = 0
        for i in range(len(data)):
            q = 0
            nr = 0

# bit = Bits()
# bit.add(1)
# GB =  Golomb()
# GB.Encode(bit,1,1,1,1)