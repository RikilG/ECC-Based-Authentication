from CryptoAPI import *


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
        doctor.PU_p     = self.PU_p
        hospital.NID    = self.NID
        hospital.Ni     = self.Ni
        hospital.id_p   = self.id_p
        hospital.id_d   = doctor.id_d
    

    def ping_to_cloud(self, cloud):
        print(":: phase 2, step 1 :: Patient")
        print("Send <ID_p, NID> to Cloud via SECURE channel")
        cloud.p_data = (self.id_p, self.NID)
    

    def send_message(self, cloud):
        print(":: phase 2, step 3 :: Patient")
        I, S3, C_h, Sig_h = self.c_data
        Ni, NID = self.Ni, self.NID
        id_p, m_b = self.id_p, self.m_b
        id_d    = self.id_d
        PU_h    = self.PU_h
        PR_p    = self.PR_p

        Sni1 = I^NID
        self.Sni = Sni1
        if S3 != gen_hash(NID, I, C_h, Sig_h):
            print("Unable to verify cloud")
            exit(1)
        
        print("Cloud verified")
        SK_pc   = gen_hash(id_p, NID, Sni1)
        key1    = gen_hash(id_p, Ni)
        m_h     = decrypt(key1, C_h)
        MD_h    = gen_hash(m_h)
        MD_p    = gen_hash(m_b)

        # Sig_h   = eval(Sig_h)    # convert signature from string to bytes by evaluating
        if not verify_sig(PU_h, MD_h, Sig_h):
            print("Unable to authenticate Hospital")
            exit(1)
        
        print("Hospital authenticated")
        key_pd  = gen_hash(id_p, id_d, Ni)
        print("key_pd: ", key_pd)
        C_p     = encrypt(key_pd, [m_h, m_b])
        Sig_p   = gen_sig(PR_p, MD_p)
        C2      = encrypt(SK_pc, [C_p, Sig_p])
        S4      = gen_hash(SK_pc, C_p, Sig_p)

        print("Send message to Cloud via PUBLIC channel")
        cloud.message = (S4, C2)