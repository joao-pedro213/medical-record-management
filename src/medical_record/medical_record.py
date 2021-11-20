import boto3
import re
from datetime import date
from src.services.rds_service import RDSService


class MedicalRecord:
    def __init__(self, patient_id: int, speciality_id: int, created_at: date) -> None:
        self.patient_id = patient_id
        self.speciality_id = speciality_id
        self.created_at = created_at
        self.medical_record_local_path = None
        self.s3_bucket = boto3.resource('s3').Bucket('mrmgmt')
        self.mysql_connection = RDSService.get_connection()

    def save(self, medical_record_local_path: str) -> None:
        self.medical_record_local_path = medical_record_local_path
        self._write_stage_table()
        self._upload_file_to_bucket()

    def _write_stage_table(self) -> None:
        try:
            print('Saving medical record in MySql.')
            s3_file_name = self._get_medical_record_file_name()
            sql_query = (
                'insert into stage.medical_record (patient_id, speciality_id, s3_file_name, created_at) ' +
                f"values({self.patient_id}, {self.speciality_id}, '{s3_file_name}', " +
                f"'{self.created_at.strftime('%Y-%m-%d')}');"
            )
            print(sql_query)
            with self.mysql_connection.cursor() as cursor:
                cursor.execute(query=sql_query)
            self.mysql_connection.commit()
        except Exception as e:
            raise RuntimeError(f'Error while executing command: {e}')

    def _get_medical_record_file_name(self) -> str:
        file_name = f"{self.patient_id}-{self.speciality_id}-{self.created_at.strftime('%Y%m%d')}"
        file_extension = re.search(r"(\..*)", self.medical_record_local_path).group(0)
        return file_name + file_extension

    def _upload_file_to_bucket(self) -> None:
        try:
            print('Saving file in s3 bucket.')
            data = open(self.medical_record_local_path, 'rb')
            s3_file_name = self._get_medical_record_file_name()
            self.s3_bucket.put_object(Key=s3_file_name, Body=data)
        except Exception as e:
            raise RuntimeError(f'Error while trying to save file to s3 bucket: {e}')
