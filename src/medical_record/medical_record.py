from src.services.rds_service import set_rds_connection
from uuid import uuid1

class MedicalRecord:
  def __init__(self, patient_id: int, speciality_id: int):
    self.patient_id = patient_id
    self.speciality_id = speciality_id

  def save(self):
    try:
      print('Trying to save medical record.')
      s3_filename = uuid1()
      sql_query = (
        'insert into stage.medical_record (patient_id, speciality_id, s3_filename) ' +
        f"values({self.patient_id}, {self.speciality_id}, '{s3_filename}');"
      )
      connection = set_rds_connection()
      with connection.cursor() as cursor:
        cursor.execute(query=sql_query)
      connection.commit()
      print('Medical record saved with success.')
    except Exception as e:
      print(f'Error while executing command {sql_query}: {e}')