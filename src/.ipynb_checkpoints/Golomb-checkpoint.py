import Math
import numpy as np
class Golomb:
    def Encode(byteManager, k, Merrval, limit,  qbpp):
        M = np.int32(2**k)
        x = np.int32(Math.floor(Merrval / M))
        r = Merrval % Merrval

        if (x < limit - qbpp - 1):
            for i in range (x): 
                byteManager.append(0)
            byteManager.append(1)
            comp = np.int32(2**(k-1))
            for i in range(k,0,-1): 
                if (comp & r) == comp):
                    byteManager.append(1)
                else:
                    byteManager.append(0)
                
                r <<= 1
            
        else:
            for i in range(limit - qbpp - 1):
                byteManager.append(0)
            
            byteManager.append(1)
            Merrval -= 1
            for i in range(qbpp, 0, -1):
                if ((128 & Merrval) == 128):
                    byteManager.append(1)
                else:
                    byteManager.append(0)
                Merrval <<= 1
            
    def Decode (data, M):
        q = 0
        nr = 0
        for i in range(len(data)):
            q = 0
            nr = 0