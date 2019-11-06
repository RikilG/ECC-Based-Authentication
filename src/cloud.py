from CryptoHelper import *


class Cloud:

    def __init__(self):
        self.h_data = (0,0)     # id_h, R
        self.message = (0,0)    # S2, C1


    def ping_to_hospital(self,hospital):
        id_h, R = self.h_data
        x   = gen_randint()
        A   = gen_hash(id_h, R, x)
        s1  = gen_hash(A)
        B   = id_h^x
        print("Send <S1, B> to Hospital via PUBLIC channel")
        hospital.c_data = (s1,B)
        self.A = A
        self.B = B
    

    def receive_and_store():
        id_h, A, B = self.id_h, self.A, self.B
        S2, C1 = self.message
        SK1_hc  = gen_hash(id_h, A, B)

        if S21 != gen_hash(SK1_hc, C1):
            print("Cannot Authenticate Hospital")
            exit()
        
        id_p, id_d, C_h, Sig_h, SID = decrypt(SK_hc, C1)
        # database.store(id_p, C_h, Sig_h, SID)
        print("Data received: ")
        print(id_p, C_h, Sig_h, SID)
    

    # def get_cloud_randomnumber(self):
    #     return self.x

if __name__ == "__main__":
    # just to test functions
    cloud = Cloud()
    cloud.h_data = (123,23)
    cloud.ping_to_hospital(cloud)