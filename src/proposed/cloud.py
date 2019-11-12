from CryptoAPI import *
from time import time


class Cloud:

    def __init__(self):
        self.h_data   = (0, 0, 0)    # id_h, a, T_H1 
        self.p_data   = (0, 0)    # id_p, NID
        self.d_data   = (0, 0, 0) # id_d, id_p, RD
        self.message  = (0,0,0)    # E2, T_H3, g
        self.database = {}
        self.Sni      = gen_randint()
        self.T_C1 = 0
        self.T_C2 = 0
        self.b = gen_randint # b belongs to Zq*
        self.delta_T = 5000
        self.S1      = 0
        self.g       = gen_randint()


    def ping_to_hospital(self,hospital):
        print(":: phase 1, step 2 ::")
        self.T_C1 = time()
        id_h, a,T_H1 = self.h_data

        if not (self.T_C1 - T_H1) < self.delta_T:
            print("Time Limit Exceeded between cloud and hospital upload")
            exit(1)
        
        self.b = gen_randint()
        b = self.b
        S1   = gen_hash(id_h, a, b, T_H1)
        K1  = gen_hash(id_h, a, T_H1)
        self.T_C2 = time()
        T_C2 = self.T_C2
        E1 = encrypt(K1,[b,S1,T_C2])
        self.S1 = S1
        print("Send <E1, T_C2> to Hospital via PUBLIC channel")
        hospital.c_data = (E1,T_C2)
        
    

    def ping_to_patient(self, patient):
        print(":: phase 2, step 2 ::")
        id_p, NID = self.p_data
        Sig_h   = self.database['Sig_h']
        C_h     = self.database['C_h']
        Sni     = self.Sni

        I   = Sni^NID
        S3  = gen_hash(NID, I, C_h, Sig_h)
        print("Send <I, S3, C_h, Sig_h> to Patient via PUBLIC channel")
        patient.c_data = (I, S3, C_h, Sig_h)

    
    def ping_to_doctor(self, doctor):
        print(":: phase 3, step 2 ::")
        id_d, id_p, RD = self.d_data
        Sig_h   = self.database['Sig_h']
        Sig_p   = self.database['Sig_p']
        C_p     = self.database['C_p']

        SK_dc   = gen_hash(id_d, id_p, RD)
        S5      = gen_hash(SK_dc, Sig_h, Sig_p, C_p)
        C3      = encrypt(SK_dc, [Sig_h, Sig_p, C_p])
        print("Send <S5, C3> to Doctor via PUBLIC channel")
        doctor.c_data = (S5, C3)
    

    def receive_and_store_hospital(self):
        print(":: phase 1, step 4 ::")
        E2, T_H3,g      = self.message
        id_h, a,T_H1 = self.h_data
        S1,b = self.S1,self.b
        self.T_C3 = time()
        self.g = g
        abg = a*b*g
        self.abg = abg
        T_C3 = self.T_C3
        if not (T_C3 - T_H3) < self.delta_T:
            print("Time Limit Exceeded between cloud and hospital upload :: step-4") 
            exit(1)
        
        SK_ch      = gen_hash(id_h, S1, abg,self.T_C1)
        id_p,NID,C_h,S2,Sig_h,T_H3      = decrypt(SK_ch,E2)
        S21        = gen_hash(SK_ch,C_h,Sig_h,T_H3)
        if S2 != S21:
            print("Cannot Authenticate Hospital")
            exit(1)
        
        
        
        print("Hospital authenticated")
        self.database['id_p']   = id_p
        self.database['C_h']    = C_h
        self.database['Sig_h']  = Sig_h
        self.database['NID']    = NID
        print("Saved Hospital data to database")
    

    def receive_and_store_patient(self):
        print(":: phase 2, step 4 ::")
        S4, C2      = self.message
        Sni         = self.Sni
        id_p, NID   = self.p_data
        id_h        = self.id_h

        SK_pc1      = gen_hash(id_p, NID, Sni)
        C_p, Sig_p  = decrypt(SK_pc1, C2)

        if S4 != gen_hash(SK_pc1, C_p, Sig_p):
            print("Unable to authenticate patient")
            exit(1)
        
        self.database['C_p']    = C_p
        self.database['Sig_p']  = Sig_p
        self.database['Sni']    = Sni
        print("Saved Patient data to database")


    def receive_and_store_doctor(self):
        S6, C4 = self.message

        C_d, Sig_d  = decrypt(SK_dc, C4)

        if S6 != gen_hash(SK_dc, C_d, Sig_d):
            print("Cannot authenticate Doctor ")
            exit(1)
        print("Doctor authenticated")

        self.database['C_d']    = C_d
        self.database['Sig_d']  = Sig_d
        print("Saved Doctor data to database")


if __name__ == "__main__":
    # just to test functions
    cloud = Cloud()
    cloud.h_data = (123,23)
    cloud.ping_to_hospital(cloud)