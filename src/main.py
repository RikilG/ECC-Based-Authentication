import hashlib
from cloud import Cloud
from hospital import Hospital
from patient import Patient



def hospital_upload_phase(hospital,cloud):

    
    A = (str(hospital.id_h)+str(hospital.R)+str(cloud.get_cloud_randomnumber()))
    s1 = hashlib.sha256(b'A').hexdigest()

    B = hospital.get_hospital_id()^cloud.get_cloud_randomnumber()



def patient_data_upload_phase():
  hello = 3


def treatment_phase():
  hello = 4

def  checkup_phase():
  hello = 5

def main():
  hospital = Hospital()
  patient = Patient()
  cloud = Cloud()
  hospital.send_to_cloud(cloud)
  cloud.send_to_hospital(hospital)
  hospital_upload_phase(hospital,cloud)
  # patient_data_upload_phase()
  # treatment_phase()
  # checkup_phase()


if __name__ == "__main__":
  main()

  

