import sys
sys.path.append('./medical-record-management/src')
from flask import Flask, request, Response
from datetime import datetime
from src.medical_record.physic_medical_record import PhysicMedicalRecord

app = Flask(__name__)


@app.route('/api/medical_record/physic/save', methods=['POST'])
def save_physic_medical_record():
    body = request.get_json()
    patient_id = body.get('patient_id')
    speciality_id = body.get('speciality_id')
    created_at = body.get('created_at')
    medical_record_local_path = body.get('medical_record_local_path')
    if patient_id and speciality_id and created_at and medical_record_local_path:
        medical_record = PhysicMedicalRecord(
            patient_id=patient_id,
            speciality_id=speciality_id,
            created_at=datetime.strptime(created_at, '%Y%m%d')
        )
        medical_record.save(medical_record_local_path=medical_record_local_path)
        message = 'medical record inserted with success.'
        status = 400
    else:
        message = 'all fields are required.'
        status = 400
    return Response(message, status=status)


@app.route('/api/medical_record/physic/', methods=['GET'])
def download_physic_medical_record():
    medical_record_id = request.args.get('medical_record_id')
    if medical_record_id is not None:
        medical_record = PhysicMedicalRecord(patient_id=None, speciality_id=None, created_at=None)
        medical_record_exists = medical_record.retrieve_medical_record(medical_record_id=medical_record_id)
        if medical_record_exists is True:
            message = 'medical record was downloaded with success.'
            status = 200
        else:
            message = 'medical record not found.'
            status = 404
    else:
        message = 'query param medical_record_id is missing.'
        status = 400
    return Response(message, status=status)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
