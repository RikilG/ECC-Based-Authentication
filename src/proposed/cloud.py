from CryptoAPI import *
import time

class Cloud:

    def __init__(self):
        self.h_data   = (0, 0)    # id_h, R
        self.p_data   = (0, 0)    # id_p, TP1
        self.d_data   = (0, 0, 0) # id_d, id_p, RD
        self.message  = (0,0)    # S2, C1 || S4, C2
        self.database = {}
        self.Sni      = gen_randint()


    def ping_to_hospital(self,hospital):
        print(":: phase 1, step 2 ::")
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
    

    def ping_to_patient(self, patient):
        print(":: phase 2, step 2 ::")
        id_p, TP1 = self.p_data
        Sig_h   = self.database['Sig_h']
        C_h     = self.database['C_h']
        NID     = self.database['NID']
        id_h    = self.database['id_h']
        Sni     = self.Sni

        I1    = gen_hash(NID,id_p)
        I     = Sni^I1
        T_c5  = time.time()
        c     = gen_randint() 
        S3    = gen_hash(NID,id_p,C_h,Sig_h,c,T_c5)
        E3    = encrypt(Sni,[Sig_h,C_h,S3,I,id_h,c,T_c5])

        self.database['S3'] = S3
        print("Send <E3,I,T_c5> to Patient via PUBLIC channel")
        patient.c_data = (E3,I,T_c5)

    
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
        E4,T_p3 = self.message
        id_p, TP1 = self.p_data
        Sig_h   = self.database['Sig_h']
        C_h     = self.database['C_h']
        NID     = self.database['NID']
        id_h    = self.database['id_h']
        S3      = self.database['S3']
        Sni     = self.Sni

        d, S4, Sig_p, C_p, T_p3 = decrypt(self.Sni,E4)
        T_c5  = time.time()
        SK_cp = gen_hash(id_p,id_h,C_h,S3,T_c5)
        S41 = gen_hash(SK_cp,C_p,Sig_p,S3,T_p3)
        
        if S4 != S41 :
            print("Couldn't authenicate")
            exit(1)
        print("Hospital authenticated")

        self.database['C_p']   = C_p
        self.database['id_p']    = id_p
        self.database['Sig_p']  = Sig_p
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