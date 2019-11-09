from CryptoAPI import *


class Cloud:

    def __init__(self):
        self.h_data = (0,0)     # id_h, R
        self.message = (0,0)    # S2, C1
        self.d_data = (0, 0, 0) # id_d, id_p, RD
        self.database = {}


    def ping_to_hospital(self,hospital):
        print("::phase1, step2")
        id_h, R = self.h_data
        self.id_h = id_h

        x   = gen_randint()
        A   = gen_hash(id_h, R, x)
        S1  = gen_hash(A)
        B   = id_h^x
        print("Send <S1, B> to Hospital via PUBLIC channel")
        # print(f"Send <S1, B> = <{S1}, {B}> to Hospital via PUBLIC channel")
        hospital.c_data = (S1,B)
        self.A = A
        self.B = B

    
    def ping_to_doctor(self, doctor):
        print("phase2, step2")
        id_d, id_p, RD = self.d_data

        SK_dc = gen_hash(id_d, id_p, RD)
        S5 = gen_hash(SK_dc, Sig)
    

    def receive_and_store_hospital(self):
        print("::phase1, step4")
        id_h, A, B = self.id_h, self.A, self.B
        S2, C1 = self.message
        SK1_hc  = gen_hash(id_h, A, B)

        if S2 != gen_hash(SK1_hc, C1):
            print("Cannot Authenticate Hospital")
            exit(1)
        
        print("Hospital authenticated")
        id_p, id_d, C_h, Sig_h, NID = decrypt(SK1_hc, C1)
        # database.store(id_p, C_h, Sig_h, SID)
        print("Data received: ")
        print(id_p.decode())
        print(id_d.decode())
        print(C_h.decode())
        print(Sig_h.decode())
        print(NID.decode())
        self.database['id_p'] = id_p.decode()
        self.database['C_h'] = C_h
        self.database['Sig_h'] = Sig_h
        self.database['NID'] = NID.decode()
    

    def receive_and_store_doctor(self):
        pass


if __name__ == "__main__":
    # just to test functions
    cloud = Cloud()
    cloud.h_data = (123,23)
    cloud.ping_to_hospital(cloud)