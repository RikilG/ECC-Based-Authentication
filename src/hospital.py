import random
import hashlib


class Hospital:

    def __init__(self):
        self.id_h = 1
        self.R = random.randint(0,2**8)
        self.c_data = (0,0)

    # def get_hospital_id(self):
    #     return self.id_h

    # def get_hospital_randomnumber(self):
    #     return self.R

    def send_to_cloud(self,cloud):
        cloud.h_data = (self.id_h,self.R)


    def verify_and_send_key(self,cloud):
        s1,B = self.c_data
        x1 = B^self.id_h

        A = (str(self.id_h)+str(x1)+str(B))
        A = str.encode(A)
        A1 = hashlib.sha256(A).hexdigest()
        val = str.encode(A)
        s1_check = hashlib.sha256(val).hexdigest()

        hold=False

        if(s1_check==s1):
            hold=True

        if hold is True:
            temp = str(self.id_h)+str(A1)+str(B)
            temp = str.encode(temp)
            SKhc = hashlib.sha256(temp).hexdigest
            temp = str(self.id_h)+str(Ni)
            temp = str.encode(temp)
            key1 = hashlib.sha256(temp).hexdigest

        