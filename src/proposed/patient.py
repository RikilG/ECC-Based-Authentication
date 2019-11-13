from CryptoAPI import *
from time import time


class Patient:

    def __init__(self):
        self.id_p   = 999
        self.NID    = gen_randint()
        self.Ni     = gen_randint()
        self.m_b    = "data from body sensors"
        self.c_data = (0, 0) # E7, T_C11
        self.PR_p, self.PU_p = gen_sig_keys()
        self.x      = 0  # x belongs to Zq*
        self.T_P4   = 0
    

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
        cloud.p_data = (self.id_p,time())
    

    def send_message(self, cloud):
        print(":: phase 2, step 3 ::")
        E3,I,T_c5 = self.c_data
        Ni, NID = self.Ni, self.NID
        id_p, m_b = self.id_p, self.m_b
        id_d    = self.id_d
        PU_h    = self.PU_h
        PR_p    = self.PR_p

        Y = I^int(gen_hash(NID,id_p),16)
        Sig_h,C_h,S3,id_h,c,T_c5 = decrypt(gen_hash(Y),E3)
        S31 =gen_hash(NID,Y,C_h,Sig_h,c,T_c5)

        if S3 != S31 :
            print("Couldn't authenicate the message")
            exit(1)
        
        print("authenicated !")

        d = gen_randint()
        SK_pc = gen_hash(id_p,id_h,C_h,S31,T_c5)
        K3 = gen_hash(id_p,id_h,NID)
        m_h = decrypt(K3,C_h)
        m_h = list(m_h)

        if not verify_sig(PU_h,gen_hash(m_h),Sig_h):
            print("Unable to authenticate Hospital")
            exit(1)
        
        print("Cloud verified")

        K4      = gen_hash(id_p,id_d,Y)
        C_p     = encrypt(K4,[m_h,m_b])
        Sig_p   = gen_sig(PR_p,gen_hash(m_b))
        T_p3    = time()
        S4      = gen_hash(SK_pc,C_p,Sig_p,S31,T_p3)
        E4      = encrypt(gen_hash(Y),[d,S4,Sig_p,C_p,T_p3])

        print("Send message to Cloud via PUBLIC channel")
        cloud.message = (E4,T_p3,SK_pc)

    def ping_download_request(self, cloud):
        print(":: phase 4, step 1 :: Patient")
        Sni     = self.Sni
        id_p    = self.id_p
        x       = gen_randint()
        self.x  = x
        T_P4    = time()
        self.T_P4 = T_P4
        NID     = self.NID
        print("Send <id_p, NID, Sni, x, T_P4> to Cloud via SECURE channel")
        cloud.p_data = (id_p, NID, Sni, x, T_P4)
    

    def send_message_checkup(self, cloud):
        print(":: phase 4, step 3 :: Patient")
        E7,T_C11 = self.c_data
        SK_pc   = self.SK_pc
        key_pd  = self.key_pd
        key_p   = self.key_p
        PU_d    = self.PU_d

        T_P4 = self.T_P4
        if not (T_P4 - T_C11) < self.delta_T:
            print("Time Limit Exceeded between cloud and patient upload :: step-3") 
            exit(1)

        S7,id_d,Sig_d,C_d,y,T_C11 = decrypt(SK_pc,E7)
        
        S71 = gen_hash(SK_pc,id_p,id_d,C_d,xyg,Sig_p,T_C11)


        if S7 != S71:
            print("Unable to verify Cloud")
            print("Patient terminating session")
            exit(1)
        print("Cloud verified")

        m_h, m_b, m_d = decrypt(K4, C_d)
        MD_d    = gen_hash(m_d)

        if not verify_sig(PU_d, MD_d, Sig_d):
            print("Cannot Authenticate Doctor")
            exit(1)
        print("Doctor authenticated")

        T_P6    = time()
        self.T_P6 = T_P6

        C_e     = encrypt(K4, [m_h, m_b, m_d])
        S8      = gen_hash(SK_pc,S71,C_e,Sig_p,Sig_d,xyg,T_P6)

        E8 = encrypt(SK_pc,[C_e,S8,T_P6])
        cloud.message = (E8, T_P6)
