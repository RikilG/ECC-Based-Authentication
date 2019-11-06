from CryptoHelper import *
from CryptoWrapper import eccEncrypt


class Hospital:

    def __init__(self):
        self.id_h = 1
        self.R = gen_randint()
        self.c_data = (0,0)

    # def get_hospital_id(self):
    #     return self.id_h

    # def get_hospital_randomnumber(self):
    #     return self.R

    def ping_to_cloud(self,cloud):
        print("Send <ID_h, R> to Cloud via SECURE channel")
        cloud.h_data = (self.id_h,self.R)
    

    def send_message(cloud):
        S1, B = self.c_data
        id_h  = self.id_h

        x1 = B^id_h
        A1 = gen_hash(id_h, x1, B)

        if S1 != gen_hash(A1):
            print("Unable to verify cloud")
            exit()

        print("Cloud verified")

        SK_hc   = gen_hash(id_h, A1, B)
        key1    = gen_hash(id_p, Ni)
        C_h     = encrypt(key1, m_h)
        MD_h    = gen_hash(m_h)
        Sig_h   = gen_sig(PR_h, MD_h)
        C1      = encrypt(SK_hc, id_p, id_d, C_h, Sig_h, NID)
        S2      = gen_hash(SK_hc, C1)

        print("Sending message to cloud via PUBLIC channel")
        cloud.message = (S2, C1)

        