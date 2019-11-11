from CryptoAPI import *


class Patient:

    def __init__(self):
        self.id_p   = 999
        self.NID    = gen_randint()
        self.Ni     = gen_randint()
        self.m_b    = "data from body sensors"
        self.c_data = (0, 0, 0, 0)  # I, S3, C_h, Sig_h
        self.Sni    = 0
        self.id_d   = 0
        self.SK_pc  = 0
        self.key_pd = 0
        self.key_p  = gen_AES_key()
        self.PR_p, self.PU_p = gen_sig_keys()
    

    def meet(self, doctor, hospital):
        self.id_d       = doctor.id_d
        self.PU_h       = hospital.PU_h
        self.PU_d       = doctor.PU_d
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
        self.Sni = Sni1
        if S3 != gen_hash(NID, I, C_h, Sig_h):
            print("Unable to verify cloud")
            exit(1)
        
        print("Cloud verified")
        SK_pc   = gen_hash(id_p, NID, Sni1)
        self.SK_pc = SK_pc
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
        self.key_pd = key_pd
        C_p     = encrypt(key_pd, [m_h, m_b])
        Sig_p   = gen_sig(PR_p, MD_p)
        C2      = encrypt(SK_pc, [C_p, Sig_p])
        S4      = gen_hash(SK_pc, C_p, Sig_p)

        print("Send message to Cloud via PUBLIC channel")
        cloud.message = (S4, C2)
    

    def ping_download_request(self, cloud):
        print(":: phase 4, step 1 :: Patient")
        Sni     = self.Sni
        id_p    = self.id_p
        id_d    = self.id_d
        print("Send <id_p, id_d, Sni> to Cloud via SECURE channel")
        cloud.p_data = (id_p, id_d, Sni)
    

    def send_message_checkup(self, cloud):
        print(":: phase 4, step 3 :: Patient")
        S8, C_d, Sig_d = self.c_data
        SK_pc   = self.SK_pc
        key_pd  = self.key_pd
        key_p   = self.key_p
        PU_d    = self.PU_d

        if S8 != gen_hash(SK_pc, C_d, Sig_d ):
            print("Unable to verify Cloud")
            exit(1)
        print("Cloud verified")

        m_h, m_b, m_d = decrypt(key_pd, C_d)
        MD_d    = gen_hash(m_d)

        if not verify_sig(PU_d, MD_d, Sig_d):
            print("Cannot Authenticate Doctor")
            exit(1)
        print("Doctor authenticated")

        C5      = encrypt(key_p, [m_h, m_b, m_d])
        S9      = gen_hash(SK_pc, C5)
        cloud.message = (S9, C5)