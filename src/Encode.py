import numpy as np
import math
from Bits import *
from TestEncoding import *
from Golomb import Golomb


# init value

def Populate(arr, value : int):
            n = len(arr)
            for i in range(n):
                arr[i] = value   



class JPEGLSEncode:
    def __init__(self):
        self.posX = 0
        self.posY = 0
        self.width = 0
        self.height = 0
        self.MAXVAL = 255
        self.PrevRunIndex = 0
        self.NEAR =  0
        self.C_MAX = 127
        self.C_MIN = -128
        self.MAXVAL = 255
        self.bpp = 0
        self.LIMIT = 0
        self.SIGN = 1
        self.RANGE =0
        self.qbpp=0
        self.N = [0]*367
        self.Nn = [0]*367
        self.A = [0]*367
        self.B = [0]*365
        self.C = [0]*365
        self.RESET = 64
        self.RunIndex = 0
        self.SIGNinterupt = False
        self.J = [
                    0, 0, 0, 0,
                    1, 1, 1, 1,
                    2, 2, 2, 2,
                    3, 3, 3, 3,
                    4, 4, 5, 5,
                    6, 6, 7, 7,
                    8, 9, 10, 11,
                    12, 13, 14, 15
                ]
        self.T = [3, 7, 21]
        self.D = [0, 0, 0]
        self.Q = [0, 0, 0]
        self.RUNindex = 0
        self.bitLine = 0
        self.data_buffer=  []
        self.count = 0
        # self.LD = []
        # self.x =  0   
        # self.a =0
        # self.b =0
        # self.c = 0
        # self.d = 0
        # self.Errval = 0
        # self.RItype = 0
        # self.RUNval = 0
        # self.Runval = 0
        # self.N_MAX =  0
        # self.C_MIN =0
        # self.C_MAx = 0
        # self.contextOfX = 0
        # self
    byteManager = Bits()
    
    def Encode(self, data):
        #self.image = System.Drawing.Bitmap(image)
        self.image = data
        # self.width = data.shape[1]
        # self.height = data.shape[0]
        self.width = 4
        self.height = 4
        self.bpp = np.int32(max(2, math.ceil(math.log(self.MAXVAL + 1, 2))))
        self.LIMIT = 2 * (self.bpp + max(8, self.bpp))
        self.RANGE = abs(self.MAXVAL + 2*self.NEAR) / (2*self.NEAR + 1) + 1
        self.qbpp = int(math.log(self.RANGE,2))
        Populate(self.N, 1)
        Populate(self.Nn, 0)
        Populate(self.B, 0)
        Populate(self.C, 0)
        Populate(self.A,int( max(2, (self.RANGE + 32) / 64)))
        # self.__init__(n)

        # Testing
        # self.LD = TestingEncoding.Input8()
        # bitsE = TestingEncoding.Result8()
        # bitLine = 0

        # self.width = 4
        # self.height = 4
        count = 0
        for x in range(self.height):
            for y in range (self.width):
                self.LD = self.image[x]
                self.GetNextSample()
                if (abs(self.D[0]) <= self.NEAR and 
                    abs(self.D[1]) <= self.NEAR and
                    abs(self.D[2]) <= self.NEAR):
                    self.RunModeProcessing()
                    pass
                else:
                    self.RegularModeProcessing()
                self.data_buffer.append(self.PrintBits())
                self.byteManager.bits.clear()
        print(self.count)
        return self.data_buffer
        
        
                    
    def GetNextSample(self):
        self.SetVariablesABCD()
        self.D[0] = self.d - self.b
        self.D[1] = self.b - self.c
        self.D[2] = self.c - self.a

        self.posX += 1

        if (self.posX == self.width):
            self.posX = 0
            self.posY = 0
        return False

    #set Ra, Rb, Rc, Rd, Rx
    def SetVariablesABCD(self):
        #set a
        if (self.posX == 0 and self.posY == 0):
            self.a = 0
        elif (self.posY > 0 and self.posX == 0):
            self.a = self.LD[(self.posY - 1)*self.width]
        elif (self.posY == 0 and self.posX > 0):
            self.a = self.LD[self.posX - 1]
        else:
            self.a = self.LD[(self.posY*self.width) + self.posX - 1]

        #set b
        if (self.posY == 0):
            self.b = 0
        else:
            self.b = self.LD[(self.posY - 1)*self.width + self.posX]
        
        #set c
        if (self.posY == 0 or (self.posY == 1 and self.posX == 0)):
            self.c = 0
        elif (self.posY > 1 and self.posX == 0):
            self.c = self.LD[(self.posY - 2)*self.width]
        else:
            self.c = self.LD[(self.posY - 1)* self.width + self.posX - 1]

        #set d
        if (self.posY == 0):
            self.d = 0
        elif (self.posY > 0 and self.posX == self.width - 1):
            self.d = self.LD[(self.posY - 1) * self.width + self.posX]
        else:
            self.d = self.LD[((self.posY - 1) * self.width) + self.posX + 1];

        #set x
        self.x = self.LD[self.posY*self.width + self.posX]

    def PrintBits(self):
        # result = []
        # for i in self.byteManager.bits:
        #     self.count +=1
        #     result.append(i)
        # return result
        result = ""
        for  i in self.byteManager.bits:
            result += str(i)
        return result
        # self.data_buffer.append(self.byteManager.bits)

    #run mode
    def RunModeProcessing(self):
        self.RunLengthDetermination()
        self.EncodeRunLengthSegment()
        self.EncodeInteruptedValue()

    def RunLengthDetermination(self):
        self.RUNval = self.a
        self.RUNcnt = 0  #represent the run length
        while (abs(self.x - self.RUNval) <= self.NEAR):
            self.RUNcnt += 1
            self.Rx = self.RUNval
            if (self.posX == 0):
                break
            else:
                self.GetNextSample()

    def EncodeRunLengthSegment(self):
        while (self.RUNcnt >= (1 << self.J[self.RunIndex])):
            self.byteManager.add(1)
            self.RUNcnt = self.RUNcnt - (1 << self.J[self.RunIndex])
            if (self.RunIndex < 31):
                self.RunIndex += 1
        
        self.PrevRunIndex = self.RunIndex
        self.SIGNinterupt = False
        if (abs(self.x - self.RUNval) > self.NEAR):
            self.SIGNinterupt = True
            self.byteManager.add(0)
            for i in range(self.J[self.RUNindex], 0,-1):               
                if ((self.RUNcnt & self.J[self.RUNindex]) == 1):
                    self.byteManager.add(1)
                else:
                    self.byteManager.add(0)

                self.RUNcnt <<= 1

            if (self.RUNindex > 0):
                self.RUNindex = self.RUNindex - 1
        
        elif (self.RUNcnt > 0):
            self.byteManager.add(1)

    def EncodeInteruptedValue(self):
        self.IndexComuptation()
        self.Errval = self.PredictionErrorRunInteruption()
        self.Errval = self.ErrorCumpotationForRunInterruption(self.Errval)
            
        #
        TEMP = 0
        if (self.RItype == 0):
            TEMP = self.A[365]
        else:
            TEMP = self.A[366] + (self.N[366] >> 1)

        self.contextOfX = self.RItype + 365
        k = 0
        while ((self.N[self.contextOfX] << k) < TEMP):
            k+=1

        #
        mmap = 0
        if ((k == 0) and (self.Errval > 0) and (2 * self.Nn[self.contextOfX] < self.N[self.contextOfX])):
            mmap = 1
        elif ((self.Errval < 0) and (2 * self.Nn[self.contextOfX] >= self.N[self.contextOfX])):
            mmap = 1
        elif ((self.Errval < 0) and (k != 0)):
            mmap = 1
        else:
            mmap = 0

        #
        EMErrval = int (2 * abs(self.Errval) - self.RItype - mmap)

        if (not self.SIGNinterupt):
            return
        #print(self.byteManager, k, EMErrval, self.LIMIT - self.J[self.PrevRunIndex] - 1, self.qbpp)
        GB = Golomb()
        self.byteManager = GB.Encode(self.byteManager, k, EMErrval, self.LIMIT - self.J[self.PrevRunIndex] - 1, self.qbpp)

        #
        if (self.Errval < 0):
            self.Nn[self.contextOfX] += 1

        self.A[self.contextOfX] += ((EMErrval + 1 - self.RItype) >> 1)
        
        if (self.N[self.contextOfX] == self.RESET):
            self.A[self.contextOfX] = self.A[self.contextOfX] >> 1
            self.N[self.contextOfX] = self.N[self.contextOfX] >> 1
            self.Nn[self.contextOfX] = self.Nn[self.contextOfX] >> 1

        self.N[self.contextOfX] = self.N[self.contextOfX] + 1


    def IndexComuptation(self):
        if (abs(self.a - self.b) <= self.NEAR):
            self.RItype = 1
        else:
            self.RItype = 0

    def PredictionErrorRunInteruption(self):
        if (self.RItype == 1):
            self.Px = self.a
        else:
            self.Px = self.b
        return self.x - self.Px

    def ErrorCumpotationForRunInterruption(self,Errval):
        if (self.RItype == 0 and self.a > self.b):
            Errval = -Errval
            self.SIGN = -1
        else:
            self.SIGN = 1

        
        self.Rx = self.x

        self.ReductionOfError(Errval)

        return Errval

    def RegularModeProcessing(self):
        self.Quantize()
        self.PredictionPx()
        self.PredictionCorrect()
        errval = self.CalculateErrorValue()
        errval = self.ComputeRx(errval)
        errval = self.ReductionOfError(errval)

        k = 0
        while ((self.N[self.contextOfX] << k) < self.A[self.contextOfX]):
            k+=1

        MError = int (self.ErrorMapping(errval, k))
        GB = Golomb()
        self.byteManager = GB.Encode(self.byteManager, k, MError, self.LIMIT, self.qbpp)
        self.UpdateVariables(errval)
        self.UpdateBiasVariable()
        
    def Quantize(self):
        self.GetQuantizationGradients()

        self.SIGN = 1

        if (self.Q[0] < 0 or
            (self.Q[0] == 0 and self.Q[1] < 0) or
            (self.Q[0] == 0 and self.Q[1] == 0 and self.Q[2] < 0)):

            self.Q[0] = -self.Q[0]
            self.Q[1] = -self.Q[1]
            self.Q[2] = -self.Q[2]
            self.SIGN = -1

        self.contextOfX = 81 * self.Q[0] + 9 * self.Q[1] + self.Q[2]


    def GetQuantizationGradients(self):
        for i in range(0,3):
            if (self.D[i] <= -self.T[2]):
                self.Q[i] = -4
            elif (self.D[i] <= -self.T[1]): 
                self.Q[i] = -3
            elif (self.D[i] <= -self.T[0]): 
                self.Q[i] = -2
            elif (self.D[i] < -self.NEAR): 
                self.Q[i] = -1
            elif (self.D[i] <= self.NEAR):
                self.Q[i] = 0
            elif (self.D[i] < self.T[0]): 
                self.Q[i] = 1
            elif (self.D[i] < self.T[1]): 
                self.Q[i] = 2
            elif (self.D[i] < self.T[2]):
                self.Q[i] = 3
            else: 
                self.Q[i] = 4

    #edge-detecting predictor
    def PredictionPx(self):
        if (self.c >= max(self.a, self.b)):
            self.Px = min(self.a, self.b)
        else:
            if (self.c <= min(self.a, self.b)):
                self.Px = max(self.a, self.b)
            else:
                self.Px = self.a + self.b - self.c

    #prediction correction from the bias
    def PredictionCorrect(self):
        if (self.SIGN == 1):
            self.Px = self.Px + self.C[self.contextOfX]
        else:
            self.Px = self.Px - self.C[self.contextOfX]

        if (self.Px > self.MAXVAL):
            self.Px = self.MAXVAL
        elif (self.Px < 0):
            self.Px = 0
        
    def CalculateErrorValue(self):
        errval = self.x - self.Px
        if (self.SIGN == -1):
            errval = -errval
        return errval

    #computation of prediction error
    def ComputeRx(self, errval):
        if(self.NEAR == 0):
            self.Rx = self.x
        else:
            if (errval > 0):
                errval = (errval + self.NEAR) / (2 * self.NEAR + 1)
            else:
                errval = -(self.NEAR - errval) / (2 * self.NEAR + 1)

            self.Rx = self.Px + self.SIGN * errval * (2 * self.NEAR + 1)

            if (self.Rx < 0):
                self.Rx = 0
            elif (self.Rx > self.MAXVAL):
                self.Rx = self.MAXVAL
        return errval

    def ReductionOfError(self, errval):
        if (errval < 0):
            errval = errval + self.RANGE
        if (errval >= (self.RANGE + 1) / 2):
            errval = errval - self.RANGE
        return errval

    def ErrorMapping(self,errval, gK):
        if (self.NEAR == 0 and gK == 0 and (2 * self.B[self.contextOfX] <= -self.N[self.contextOfX])):
            if (errval >= 0):
                MErrval = 2 * errval + 1
            else:
                MErrval = -2 * (errval + 1)
        else:
            if (errval >= 0):
                MErrval = 2 * errval
            else:
                MErrval = -2 * errval - 1
        
        return MErrval

    def UpdateVariables(self, errval):
        #print(self.A[self.contextOfX]. self.B[self.contextOfX], self.C[self.contextOfX])
        # print("hoamayman")
        # print(self.contextOfX)
        # print(self.A)
        # print(self.A)
        self.B[self.contextOfX] = int(self.B[self.contextOfX] + errval * (2 * self.NEAR + 1))
        self.A[self.contextOfX] = int (self.A[self.contextOfX] + abs(errval))
        if (self.N[self.contextOfX] == self.RESET):
            self.A[self.contextOfX] = self.A[self.contextOfX] >> 1
            if (self.B[self.contextOfX] >= 0):
                self.B[self.contextOfX] = self.B[self.contextOfX] >> 1
            else:
                self.B[self.contextOfX] = -((1 - self.B[self.contextOfX]) >> 1)

            self.N[self.contextOfX] = self.N[self.contextOfX] >> 1
        
        self.N[self.contextOfX] = self.N[self.contextOfX] + 1

    def UpdateBiasVariable(self):
        if (self.B[self.contextOfX] <= -self.N[self.contextOfX]):            
            self.B[self.contextOfX] = int (self.B[self.contextOfX] + self.N[self.contextOfX])
            if (self.C[self.contextOfX] > self.C_MIN):
                self.C[self.contextOfX] = int (self.C[self.contextOfX] - 1)
            if (self.B[self.contextOfX] <= -self.N[self.contextOfX]):
                self.B[self.contextOfX] = -int (self.N[self.contextOfX] + 1)

        elif (self.B[self.contextOfX] > 0):
            self.B[self.contextOfX] = self.B[self.contextOfX] - self.N[self.contextOfX]
            if (self.C[self.contextOfX] < self.C_MAX):
                self.C[self.contextOfX] += 1
            if (self.B[self.contextOfX] > 0):
                self.B[self.contextOfX] = 0

#return max value
def mmax(i, j):
    return j if j > i else i

def mmin(i, j):
    return j if j < i else i
