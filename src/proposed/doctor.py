from CryptoAPI import *
from time import time

class Doctor():

    def __init__(self):
        self.id_p   = 0
        self.id_d   = 747
        self.Ni     = 0
        self.r      = gen_randint()
        self.c_data = (0, 0)    # E5, J, T_cs
    

    def ping_to_cloud(self, cloud):
        print(":: phase 3, step 1 ::")
        id_d, r = self.id_d, self.r
        T_d1 = int(time())
        print("Send <ID_d, r, T_d1> to Cloud via SECURE channel")
        cloud.d_data = (id_d, r, T_d1)
    

    def send_message(self, cloud):
        print(":: phase 3, step 3 ::")
        E5, J, T_cs = self.c_data

        if T_d2-T_cs > dT:
            print("Request time limit exceded")

        Z       = J ^ gen_hash(id_d, r)
        Sig_p, Sig_h, NID, C_p, S5, s, T_cs = decrypt(Z, E5)
        S51     = gen_hash(id_p, id_d, Sig_h, Sig_p, C_p, T_cs)

        if S51 != S5:
            print("Cannot Authenticate Cloud")
            exit(1)
        print("Cloud authenticated")

        K5      = gen_hash(id_p, id_h, NID)
        m_h, m_b= decrypt(K5, C_p)

        if not validate_sig(PU_h, gen_hash(m_h), Sig_h):
            print("Unable to verify Hospital signature")
            exit(1)
        print("Hospital signature verified")

        if not validate_sig(PU_p, gen_hash(m_b), Sig_p):
            print("Unable to verify Patient signature")
            exit(1)
        print("Patient signature verified")

        m_d     = [id_p, data_d]
        C_d     = encrypt(K5, [m_h, m_b, m_d])
        Sig_d   = gen_sig(PR_d, gen_hash(m_d))
        S6      = gen_hash(id_p, id_d, C_d, Sig_d, Sig_p, T_d3)
        SK_dc   = gen_hash(S6, id_p, id_d, Sig_d, Sig_p, r*s*g, T_d3)
        E6      = encrypt(Z, [Sig_d, C_d, S6, T_d3])
        print("Send <E6, T_d3> to Cloud via PUBLIC channel")
        cloud.message = (E6, T_d3)