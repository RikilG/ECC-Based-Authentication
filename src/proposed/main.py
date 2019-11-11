from cloud import Cloud
from doctor import Doctor
from patient import Patient
from hospital import Hospital


def main():
    # initialize class objects
    patient  = Patient()
    doctor   = Doctor()
    hospital = Hospital()
    cloud    = Cloud()
    patient.meet(doctor, hospital)

    # section 4.1 - Healthcare centre upload phase
    hospital_upload_phase(hospital, cloud)
    # section 4.2 - Patient data upload phase
    patient_data_upload_phase(patient, cloud)
    # section 4.3 - Treatment phase
    treatment_phase(doctor, cloud)
    # section 4.4 - Check up phase
    checkup_phase()


def hospital_upload_phase(hospital,cloud):
    print("\n########## Phase1 ##########")
    hospital.ping_to_cloud(cloud)
    cloud.ping_to_hospital(hospital)
    hospital.send_message(cloud)    # also verify
    cloud.receive_and_store_hospital()


def patient_data_upload_phase(patient, cloud):
    print("\n########## Phase2 ##########")
    patient.ping_to_cloud(cloud)
    cloud.ping_to_patient(patient)
    patient.send_message(cloud)
    cloud.receive_and_store_patient()

    
def treatment_phase(doctor, cloud):
    print("\n########## Phase3 ##########")
    doctor.ping_to_cloud(cloud)
    cloud.ping_to_doctor(doctor)
    doctor.send_message(cloud)
    cloud.receive_and_store_doctor()


def checkup_phase():
    print("\n########## Phase4 ##########")


if __name__ == "__main__":
    main()