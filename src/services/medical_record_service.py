from flask import Flask, request, jsonify
from datetime import datetime
from src.medical_record.medical_record import MedicalRecord

app = Flask(__name__)


@app.route('/api/medical_record/save', methods=['POST'])
def save_medical_record():
    body = request.get_json()
    patient_id = body.get('patient_id')
    speciality_id = body.get('speciality_id')
    created_at = body.get('created_at')
    medical_record_local_path = body.get('medical_record_local_path')

    if patient_id and speciality_id and created_at and medical_record_local_path:
        medical_record = MedicalRecord(
            patient_id=patient_id,
            speciality_id=speciality_id,
            created_at=datetime.strptime(created_at, '%Y%m%d')
        )
        medical_record.save(medical_record_local_path=medical_record_local_path)
        message = 'medical record inserted with success.'

    else:
        message = 'all fields are required.'
    return jsonify({'message': message})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
