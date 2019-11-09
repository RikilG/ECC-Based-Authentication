from CryptoAPI import *

class Doctor():

    def __init__(self, patient):
        # patient id
        self.id_p = patient.id_p
        # doctor id
        self.id_d = 747
        self.RD = gen_randint()
    

    def ping_to_cloud(self, cloud):
        print("phase2, step1")
        id_p, id_d, RD = self.id_p, self.id_d, self.RD
        cloud.d_data = (id_p, id_d, RD)
        print("send <ID_p, ID_d, RD> to Cloud via SECURE channel")