from Encode import *
class  Program:
    def main():
        args = list()
        print("Enter args:")
        s = input()
        args = list(s.split(' '))
        if (len(args) > 2):
            if (args[0] == "-E" and len(args) == 4):
                jpgls = JPEGLSEncode()
                encodeData = jpgls.Encode(args[2], int(args[1][(len(args[1]) - 1)::1]))
                f = open(args[3],'wb+')
                f.write(encodeData)
                f.close()
        
            elif (args[0] == "-D"):
                f = open(args[1],'r')
                reader = f.read()

            else: 
                print("Check arguments against")
            
        else:
            print("Input arguments")
        
