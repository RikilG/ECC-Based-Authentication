import hashlib
from cloud import Cloud
from hospital import Hospital
from patient import Patient


def hospital_upload_phase(hospital,cloud):
    hospital.ping_to_cloud(cloud)
    cloud.ping_to_hospital(hospital)
    hospital.send_message(cloud)
    cloud.receive_and_store()


# def patient_data_upload_phase():
#     pass


# def treatment_phase():
#     pass


# def checkup_phase():
#     pass


def main():
    # initialize class objects
    hospital = Hospital()
    patient = Patient()
    cloud = Cloud()

    # section 4.1 - Healthcare centre upload phase
    hospital_upload_phase(hospital, cloud)
    # patient_data_upload_phase()
    # treatment_phase()
    # checkup_phase()


if __name__ == "__main__":
    main()