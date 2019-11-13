from CryptoAPI import *
from time import time

class Cloud:

    def __init__(self):
        self.h_data     = (0, 0, 0)    # id_h, a, T_H1 
        self.p_data     = (0, 0)    # id_p, NID
        self.d_data     = (0, 0, 0) # id_d, id_p, RD
        self.message    = (0,0,0)    # E2, T_H3, g
        self.database   = {}
        self.Sni        = gen_randint()
        self.T_C1       = 0
        self.T_C2       = 0
        self.T_C10      = 0 
        self.T_C11      = 0
        self.b          = gen_randint # b belongs to Zq*
        self.delta_T    = 5
        self.S1         = 0
        self.g          = gen_randint()
        self.s          = gen_randint()
        self.y          = 0  # y belongs to Zq*


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
        id_p, TP1 = self.p_data
        Sig_h   = self.database['Sig_h']
        C_h     = self.database['C_h']
        NID     = self.database['NID']
        id_h    = self.database['id_h']
        Sni     = self.Sni

        I1    = gen_hash(NID,id_p)
        I     = Sni^int(I1, 16)
        T_c5  = time()
        c     = gen_randint() 
        S3    = gen_hash(NID,Sni,C_h,Sig_h,c,T_c5)
        E3    = encrypt(gen_hash(Sni),[Sig_h,C_h,S3,id_h,c,T_c5])

        self.database['S3'] = S3
        self.database['T_c5'] = T_c5
        print("Send <E3,I,T_c5> to Patient via PUBLIC channel")
        patient.c_data = (E3,I,T_c5)

    
    def ping_to_doctor(self, doctor):
        print(":: phase 3, step 2 ::")
        id_d, r, T_d1 = self.d_data
        s           = self.s, 
        sni         = self.Sni
        id_p, NID   = self.p_data
        Sig_h   = self.database['Sig_h']
        Sig_p   = self.database['Sig_p']
        C_p     = self.database['C_p']

        if time() - T_d1 > self.delta_T:
            print("Request time limit excedeed")
            exit(1)
        
        J       = sni ^ int(gen_hash(id_d, r), 16)
        T_cs    = time()
        S5      = gen_hash(id_p, id_d, Sig_h, Sig_p, C_p, T_cs)
        E5      = encrypt(gen_hash(sni), [Sig_p, Sig_h, NID, C_p, S5, s, T_cs])
        print("Send <E5, J, T_cs> to Doctor via PUBLIC channel")
        doctor.c_data = (E5, J, T_cs)
    

    def receive_and_store_hospital(self):
        print(":: phase 1, step 4 ::")
        E2, T_H3,g  = self.message
        id_h, a,T_H1= self.h_data
        S1,b        = self.S1,self.b
        self.T_C3   = time()
        self.g      = g
        abg         = a*b*g
        self.abg    = abg
        T_C3        = self.T_C3
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
        self.database['id_h']   = id_h
        print("Saved Hospital data to database")
    
    def receive_and_store_patient(self):
        print(":: phase 2, step 4 ::")
        E4,T_p3,SK_pc = self.message
        Sni         = self.Sni
        id_p, NID   = self.p_data
        id_h        = self.database['id_h']
        C_h         = self.database['C_h']
        S3          = self.database['S3']
        T_c5        = self.database['T_c5']

        d, S4, Sig_p, C_p, T_p3  = decrypt(gen_hash(Sni),E4)
        SK_cp = gen_hash(id_p,id_h,C_h,S3,T_c5)
        S41 = gen_hash(SK_pc,C_p,Sig_p,S3,T_p3) 

        if S4 != S41 :
            print("Unable to authenticate patient")
            exit(1)
        
        print("Successfully authenicated the patient!")
        
        self.database['C_p']    = C_p
        self.database['Sig_p']  = Sig_p
        self.database['id_p']   = id_p
        print("Saved Patient data to database")


    def receive_and_store_doctor(self):
        print(":: phase 3, step 4::")
        E6, T_d3    = self.message
        id_p, NID   = self.p_data
        sni, id_d   = self.Sni, self.d_data[0]
        Sig_p       = self.database['Sig_p']

        if time()-T_d3 > self.delta_T:
            print("Request timed out")
            exit(1)

        Sig_d, C_d, S6, T_d3  = decrypt(gen_hash(sni), E6)

        if S6 != gen_hash(id_p, id_d, C_d, Sig_d, Sig_p, T_d3):
            print("Cannot authenticate Doctor")
            exit(1)
        print("Doctor authenticated")

        SK_cd = gen_hash(id_p, id_d, C_d, Sig_d, Sig_p, T_d3)

        self.database['C_d']    = C_d
        self.database['Sig_d']  = Sig_d
        print("Saved Doctor data to database")


    def ping_download_request(self, patient):
        print(":: phase 4, step 2::")
        id_p, NID, Sni, x, T_P4 = self.p_data
        T_C10 = time()
        self.T_C10 = T_C10
        if not (T_C10 - T_P4) < self.delta_T:
            print("Time Limit Exceeded between cloud and patient upload :: step-1") 
            exit(1)

        y = gen_randint()
        self.y = y

        # check database record using id_p, id_d, Sni
        NID     = self.database['NID']
        C_d     = self.database['C_d']
        Sig_d   = self.database['Sig_d']
        

        T_C11 = time()
        self.T_C11 = T_C11
        S7      = gen_hash(SK_cp,id_p,id_d,C_d,xyg,Sig_p,T_C11)
        E7      = encrypt(SK_cp,[S7,id_d,Sig_d,C_d,y,T_C11])
        print("Send <E7, T_C11> to Patient via PUBLIC channel")
        patient.c_data = (E7, T_C11)


    def save_patient_data(self):
        print(":: phase 4, step 4 ::")
        E8,T_P6  = self.message
        SK_cp  = self.SK_cp

        T_C12 = time()
        self.T_C12 = T_C12
        if not (T_C12 - T_P6) < self.delta_T:
            print("Time Limit Exceeded between cloud and patient upload :: step-4") 
            exit(1)

        C_e,S8,T_P6 = decrypt(SK_cp,E8)
        S81 = gen_hash(SK_cp,S7,C_e,Sig_p,Sig_d,xyg,T_P6)

        if S8 != S81:
            print("Unable to verify Patient")
            exit(1)
        print("Patient verified")

        self.database['C_e'] = C_e
        print("Saved patient data to database")
        print("Decryption key lies with patient")
        print("SUCCESS! completed TMIS transaction using proposed Protocol")



if __name__ == "__main__":
    # just to test functions
    cloud = Cloud()
    cloud.h_data = (123,23)
    cloud.ping_to_hospital(cloud)