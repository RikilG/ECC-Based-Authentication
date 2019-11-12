from CryptoAPI import *
import time

class Patient:

    def __init__(self):
        self.id_p   = 999
        self.NID    = gen_randint()
        self.Ni     = gen_randint()
        self.m_b    = "data from body sensors"
        self.c_data = (0, 0, 0, 0)  # I, S3, C_h, Sig_h
        self.PR_p, self.PU_p = gen_sig_keys()
    

    def meet(self, doctor, hospital):
        self.id_d       = doctor.id_d
        self.PU_h       = hospital.PU_h
        doctor.id_p     = self.id_p
        doctor.Ni       = self.Ni
        doctor.PU_h     = hospital.PU_h
        hospital.NID    = self.NID
        hospital.Ni     = self.Ni
        hospital.id_p   = self.id_p
        hospital.id_d   = doctor.id_d
    

    def ping_to_cloud(self, cloud):
        print(":: phase 2, step 1 ::")
        print("Send <ID_p, NID> to Cloud via SECURE channel")
        cloud.p_data = (self.id_p, time.time())
    

    def send_message(self, cloud):
        print(":: phase 2, step 3 ::")
        E3,I,T_c5 = self.c_data
        Ni, NID = self.Ni, self.NID
        id_p, m_b = self.id_p, self.m_b
        id_d    = self.id_d
        PU_h    = self.PU_h
        PR_p    = self.PR_p

        Y = I^gen_hash(NID,id_p)
        Sig_h,C_h,S3,id_h,c,T_c5 = decrypt(Y,E3)
        S31 =gen_hash(NID,Y,C_h,Sig_h,c,T_c5)

        if S3 != S31 :
            print("Couldn't authenicate the message")
            exit(1)
        
        d = gen_randint()
        SK_pc = gen_hash(id_p,id_h,C_h,S31,T_c5)
        K3 = gen_hash(id_p,id_h,NID)
        m_h = decrypt(K3,C_h)

        if not verify_sig(PU_h,m_h, Sig_h):
            print("Unable to authenticate Hospital")
            exit(1)
        
        print("Cloud verified")

        K4      = gen_hash(id_p,id_d,Y)
        C_p     = encrypt(K4,[m_h,m_b])
        Sig_p   = gen_sig(PR_p,gen_hash(m_b))
        T_p3    = time.time()
        S4      = gen_hash(SK_pc,C_p,Sig_p,S31,T_p3)
        E4      = encrypt(Y,[d,S4,Sig_p,C_p,T_p3])

        print("Send message to Cloud via PUBLIC channel")
        cloud.message = (E4,T_p3)