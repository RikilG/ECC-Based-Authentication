from CryptoAPI import *

class Doctor():

    def __init__(self):
        self.id_p   = 0
        self.id_d   = 747
        self.Ni     = 0
        self.RD     = gen_randint()
        self.c_data = (0, 0)    # S5, C3
    

    def ping_to_cloud(self, cloud):
        print(":: phase 3, step 1 ::")
        id_p, id_d, RD = self.id_p, self.id_d, self.RD
        print("Send <ID_p, ID_d, RD> to Cloud via SECURE channel")
        cloud.d_data = (id_d, id_p, RD)
    

    def send_message(self, cloud):
        print(":: phase 3, step 3 ::")
        id_d    = self.id_d
        id_p    = self.id_p
        RD, Ni  = self.RD, self.Ni
        S5, C3  = self.c_data
        PU_h    = self.PU_h

        SK_dc1  = gen_hash(id_d, id_p, RD)
        Sig_h, Sig_p, C_p = decrypt(SK_dc1, C3)

        if S5 != gen_hash(SK_dc1, Sig_h, Sig_p, C_p):
            print("Unable to verify Cloud")
            exit(1)
        print("Cloud verified")

        key_pd  = gen_hash(id_p, id_d, Ni)
        m_h, m_b= decrypt(key_pd, C_p)
        MD_h    = gen_hash(m_h)
        
        print(C_p)
        if not verify_sig(PU_h, MD_h, Sig_h):
            print("Unable to verify Hospital")
            exit(1)
        print("Hospital verified")

        if not verify_sig(PU_p, gen_hash(m_b), Sig_p):
            print("Unable to verify Patient")
            exit(1)
        print("Patient verified")

        m_d     = (id_p, data_d)
        C_d     = encrypt(key_pd, [m_h, m_b, m_d])
        MD_d    = gen_hash(m_d)
        Sig_d   = gen_sig(PR_d, MD_d)
        C4      = encrypt(SK_dc1, [C_d, Sig_d])
        S6      = gen_hash(SK_dc1, C_d, Sig_d)
        print("Send <S6, C4> to Cloud via PUBLIC channel")
        cloud.message = (S6, C4)