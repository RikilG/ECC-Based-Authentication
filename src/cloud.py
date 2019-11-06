import random
import hashlib


class Cloud:

    def __init__(self):
        self.x = random.randint(0,2**8-1)
        self.h_data = (0,0)

    def send_to_hospital(self,hospital):
        A = (str(self.h_data[0])+str(self.h_data[1])+str(self.x))
        A = str.encode(A)
        A = hashlib.sha256(A).hexdigest()
        A = str.encode(A)
        s1 = hashlib.sha256(A).hexdigest() 
        B = self.h_data[0]^self.x
        hospital.c_data = (s1,B)
    

    def get_cloud_randomnumber(self):
        return self.x
    