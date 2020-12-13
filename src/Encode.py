import numpy as np
import Math
import System.Drawing

class JPEGLSEncode:
    byteManager = Bits()

    def __init__(self, near):
        self.PrevRunIndex = 0
        self.NEAR = near
        self.C_MAX = 127
        self.C_MIN = -128
        self.MAXVAL = 255
        self.bpp = np.int32(max(2, Math.ceil(Math.log(MAXVAL + 1, 2))))
        self.LIMIT = 2 * (bpp + max(8, bpp))
        self.SIGN = 1
        self.RANGE = Math.abs(MAXVAL + 2*NEAR) / (2*NEAR + 1) + 1
        self.qbpp = int(Math.log(self.RANGE,2))

        self.N = [0]*367
        self.Nn = [0]*367
        self.A = [0]*367
        self.B = [0]*365
        self.C = [0]*365
        self.Populate(self.N, 1)
        self.Populate(self.Nn, 0)
        self.Populate(self.B, 0)
        self.Populate(self.C, 0)
        self.Populate(self.A, max(2, (RANGE + 32) / 64))
        self.RESET = 64
        self.RunIndex = 0
        self.SIGNinterupt = false
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
        self.width = image.Width
        self.height = image.Height
    
    def Encode(image, n = 0):
        self.image = System.Drawing.Bitmap(image)
        self.__init__(n)

        # Testing
        self.LD = TestingEncoding.Input8()
        bitsE = TestingEncoding.Result8()
        bitLine = 0

        self.width = 4
        self.height = 4

        while ((posX + 1)*(posY+1) < width*height):
            self.GetNextSample()
            if (Math.abs(self.D[0]) <= NEAR and 
                Math.abs(self.D[1]) <= NEAR and
                Math.abs(self.D[2]) <= NEAR):
                self.RunModeProcessing()
                pass
            else:
                self.RegularModeProcessing()
            
            #Testing
            bitsS = PrintBits()
            if (bitsS != bitsE[bitLine]):
                print("ERROR")
                print(bitsS + " " + bitsE[bitLine])
            
            byteManager.bits.clear()
            if (posY + 1 > height):
                break
            
            bitLine += 1
        
        print("FINISH")
        return byte[1]
        pass

        #get next sample of image
        def GetNextSample():
            self.SetVariablesABCD()
            self.D[0] = self.d - self.b
            self.D[1] = self.b - self.c
            self.D[2] = self.c - self.a

            posX += 1

            if (posX == width):
                posX = 0
                posY += 1
            return false

        #set Ra, Rb, Rc, Rd, Rx
        def SetVariablesABCD():
            #set a
            if (posX == 0 and posY == 0):
                self.a = 0
            elif (posY > 0 and posX == 0):
                self.a = self.LD[(posY - 1)*width]
            elif (posY == 0 and posX > 0):
                self.a = self.LD[posX - 1]
            else:
                self.a = self.LD[(posY*width) + posX - 1]

            #set b
            if (posY == 0):
                self.b = 0
            else:
                self.b = self.LD[(posY - 1)*width + posX]
            
            #set c
            if (posY == 0 or (posY == 1 and posX == 0)):
                self.c = 0
            elif (posY > 1 and posX == 0):
                self.c = self.LD[(posY - 2)*width]
            else:
                self.c = self.LD[(posY - 1)* width + posX - 1]

            #set d
            if (posY == 0):
                self.d = 0
            elif (posY > 0 and posX == width - 1):
                self.d = self.LD[(posY - 1) * width + posX]
            else:
                self.d = self.LD[((posY - 1) * width) + posX + 1];

            #set x
            self.x = self.LD[posY*width + posX]

        def PrintBits():
            result = ""
            for i in byteManager.bits:
                result += str(i) #i = 1||0   
                print(str(i))
            return result

        #run mode
        def RunModeProcessing():
            RunLengthDetermination()
            EncodeRunLengthSegment()
            EncodeInteruptedValue()
        
        def RunLengthDetermination():
            RUNval = self.a
            RUNcnt = 0  #represent the run length
            while (Math.abs(self.x - RUNval) <= NEAR):
                RUNcnt += 1
                Rx = RUNval
                if (posX == 0):
                    break
                else:
                    GetNextSample()
        
        def EncodeRunLengthSegment():
            while (RUNcnt >= (1 << J[RunIndex])):
                byteManager.append(1)
                RUNcnt = RUNcnt - (1 << J[RunIndex])
                if (RunIndex < 31):
                    RunIndex += 1
            
            self.PrevRunIndex = RunIndex
            self.SIGNinterupt = false
            if (Math.abs(self.x - RUNval) > NEAR):
                SIGNinterupt = true
                byteManager.append(0)
                for i in range(J[RUNindex], 0,-1):               
                    if ((RUNcnt & J[RUNindex]) == 1):
                        byteManager.append(1)
                    else:
                        byteManager.append(0)

                    RUNcnt <<= 1

                if (RUNindex > 0):
                    RUNindex = RUNindex - 1
            
            elif (RUNcnt > 0):
                byteManager.append(1)

        def EncodeInteruptedValue():
            IndexComuptation()
            Errval = PredictionErrorRunInteruption()
            Errval = ErrorCumpotationForRunInterruption(Errval)
             
            #
            TEMP = 0
            if (RItype == 0):
                TEMP = A[365]
            else:
                TEMP = A[366] + (N[366] >> 1)

            contextOfX = RItype + 365
            k = 0
            while ((N[contextOfX] << k) < TEMP):
                k+=1

            #
            mmap = 0
            if ((k == 0) and (Errval > 0) and (2 * Nn[contextOfX] < N[contextOfX])):
                mmap = 1
            elif ((Errval < 0) and (2 * Nn[contextOfX] >= N[contextOfX])):
                mmap = 1
            elif ((Errval < 0) and (k != 0)):
                mmap = 1
            else:
                mmap = 0

            #
            EMErrval = 2 * Math.abs(Errval) - RItype - mmap

            if (not SIGNinterupt):
                return

            GB = Golomb()
            GB.Encode(byteManager, k, EMErrval, (LIMIT - J[PrevRunIndex] - 1), qbpp)

            #
            if (Errval < 0):
                Nn[contextOfX] += 1

            A[contextOfX] += ((EMErrval + 1 - RItype) >> 1)
            
            if (N[contextOfX] == RESET):
                A[contextOfX] = A[contextOfX] >> 1
                N[contextOfX] = N[contextOfX] >> 1
                Nn[contextOfX] = Nn[contextOfX] >> 1

            N[contextOfX] = N[contextOfX] + 1

        
        def IndexComuptation():
            if (Math.abs(a - b) <= NEAR):
                RItype = 1
            else:
                RItype = 0
        
        def PredictionErrorRunInteruption():
            if (RItype == 1):
                Px = self.a
            else:
                Px = self.b
            return x - Px
        
        def ErrorCumpotationForRunInterruption(Errval):
            if (RItype == 0 and a > b):
                Errval = -Errval
                SIGN = -1
            else:
                SIGN = 1

            # if (NEAR > 0):
            #     #Errval = Quantize()
            #     #x = ComputeX()
            # else:
                Rx = x

            ReductionOfError(Errval)

            return Errval

        def RegularModeProcessing():
            self.Quantize()
            self.PredictionPx()
            self.PredictionCorrect()
            errval = CalculateErrorValue()
            self.ComputeRx()
            self.ReductionOfError()

            k = 0
            while ((N[contextOfX] << k) < A[contextOfX]):
                k+=1

            MError = self.ErrorMapping(errval, k)
            GB = Golomb()
            GB.Encode(byteManager, k, MError, LIMIT, qbpp)
            self.UpdateVariables(errval)
            self.UpdateBiasVariable()
            
        def Quantize():
            self.GetQuantizationGradients()

            SIGN = 1

            if (Q[0] < 0 or
                (Q[0] == 0 and Q[1] < 0) or
                (Q[0] == 0 and Q[1] == 0 and Q[2] < 0)):

                Q[0] = -Q[0]
                Q[1] = -Q[1]
                Q[2] = -Q[2]
                SIGN = -1

            contextOfX = 81 * Q[0] + 9 * Q[1] + Q[2]

        
        def GetQuantizationGradients():
            for i in range(0,3):
                if (D[i] <= -T[2]):
                    Q[i] = -4
                elif (D[i] <= -T[1]): 
                    Q[i] = -3
                elif (D[i] <= -T[0]): 
                    Q[i] = -2
                elif (D[i] < -NEAR): 
                    Q[i] = -1
                elif (D[i] <= NEAR):
                    Q[i] = 0
                elif (D[i] < T[0]): 
                    Q[i] = 1
                elif (D[i] < T[1]): 
                    Q[i] = 2
                elif (D[i] < T[2]):
                    Q[i] = 3
                else: 
                    Q[i] = 4

        #edge-detecting predictor
        def PredictionPx():
            if (c >= max(a, b)):
                Px = min(a, b)
            else:
                if (c <= min(a, b)):
                    Px = max(a, b)
                else:
                    Px = a + b - c
        
        #prediction correction from the bias
        def PredictionCorrect():
            if (SIGN == 1):
                Px = Px + C[contextOfX]
            else:
                Px = Px - C[contextOfX]

            if (Px > MAXVAL):
                Px = MAXVAL
            elif (Px < 0):
                Px = 0
            
        def CalculateErrorValue():
            errval = x - Px
            if (SIGN == -1):
                errval = -errval
            return errval
        
        #computation of prediction error
        def ComputeRx():
            global errval
            if(NEAR == 0):
                Rx = x
            else:
                if (errval > 0):
                    errval = (errval + NEAR) / (2 * NEAR + 1)
                else:
                    errval = -(NEAR - errval) / (2 * NEAR + 1)

                Rx = Px + SIGN * errval * (2 * NEAR + 1)

                if (Rx < 0):
                    Rx = 0
                elif (Rx > MAXVAL):
                    Rx = MAXVAL

        def ReductionOfError():
            global errval
            if (errval < 0):
                errval = errval + RANGE
            if (errval >= (RANGE + 1) / 2):
                errval = errval - RANGE

        def ErrorMapping(errval, gK):
            if (NEAR == 0 and gK == 0 and (2 * B[contextOfX] <= -N[contextOfX])):
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

        def UpdateVariables(errval):
            B[contextOfX] = B[contextOfX] + errval * (2 * NEAR + 1)
            A[contextOfX] = A[contextOfX] + Math.abs(errval)
            if (N[contextOfX] == RESET):
                A[contextOfX] = A[contextOfX] >> 1
                if (B[contextOfX] >= 0):
                    B[contextOfX] = B[contextOfX] >> 1
                else:
                    B[contextOfX] = -((1 - B[contextOfX]) >> 1)

                N[contextOfX] = N[contextOfX] >> 1
            
            N[contextOfX] = N[contextOfX] + 1
        
        def UpdateBiasVariable():
            if (B[contextOfX] <= -N[contextOfX]):            
                B[contextOfX] = B[contextOfX] + N[contextOfX]
                if (C[contextOfX] > C_MIN):
                    C[contextOfX] = C[contextOfX] - 1
                if (B[contextOfX] <= -N[contextOfX]):
                    B[contextOfX] = -N[contextOfX] + 1

            elif (B[contextOfX] > 0):
                B[contextOfX] = B[contextOfX] - N[contextOfX]
                if (C[contextOfX] < C_MAX):
                    C[contextOfX] += 1
                if (B[contextOfX] > 0):
                    B[contextOfX] = 0

        #return max value
        def mmax(i, j):
            return j if j > i else i

        def mmin(i, j):
            return j if j < i else i

        def Populate(arr, value):
            n = len(arr)
            for i in range(n):
                arr[i] = value