from CryptoAPI import *

class Doctor():

    def __init__(self):
        self.id_p   = 0
        self.id_d   = 747
        self.Ni     = 0
        self.RD     = gen_randint()
        self.c_data = (0, 0)    # S5, C3
        self.m_d    = "here is doctor's data based of m_h and m_b"
        self.data_d = "medical report based of m_d and m_b: "
        self.PR_d, self.PU_d = gen_sig_keys()
    

    def ping_to_cloud(self, cloud):
        print(":: phase 3, step 1 :: Doctor")
        id_p, id_d, RD = self.id_p, self.id_d, self.RD
        print("Send <ID_p, ID_d, RD> to Cloud via SECURE channel")
        cloud.d_data = (id_d, id_p, RD)
    

    def send_message(self, cloud):
        print(":: phase 3, step 3 :: Doctor")
        id_d    = self.id_d
        id_p    = self.id_p
        RD, Ni  = self.RD, self.Ni
        S5, C3  = self.c_data
        PU_h    = self.PU_h
        PU_p    = self.PU_p
        PR_d    = self.PR_d
        m_d, data_d = self.m_d, self.data_d

        SK_dc1  = gen_hash(id_d, id_p, RD)
        Sig_h, Sig_p, C_p = decrypt(SK_dc1, C3)

        if S5 != gen_hash(SK_dc1, Sig_h, Sig_p, C_p):
            print("Unable to verify Cloud")
            exit(1)
        print("Cloud verified")

        key_pd  = gen_hash(id_p, id_d, Ni)
        m_h, m_b= decrypt(key_pd, C_p)
        MD_h    = gen_hash(m_h)
        MD_p    = gen_hash(m_b)
        
        if not verify_sig(PU_h, MD_h, Sig_h):
            print("Unable to verify Hospital")
            exit(1)
        print("Hospital verified")

        if not verify_sig(PU_p, MD_p, Sig_p):
            print("Unable to verify Patient")
            exit(1)
        print("Patient verified")

        data_d  = data_d + m_h + m_b
        m_d     = [id_p, data_d]
        C_d     = encrypt(key_pd, [m_h, m_b, m_d])
        MD_d    = gen_hash(m_d)
        Sig_d   = gen_sig(PR_d, MD_d)
        C4      = encrypt(SK_dc1, [C_d, Sig_d])
        S6      = gen_hash(SK_dc1, C_d, Sig_d)
        print("Send <S6, C4> to Cloud via PUBLIC channel")
        cloud.message = (S6, C4)