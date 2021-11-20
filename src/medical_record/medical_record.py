import re
from datetime import datetime, timedelta, date
from src.services.rds_service import RDSService
from src.utils.s3_utils import remove_files_from_bucket, upload_file_to_bucket


class MedicalRecord:
    def __init__(self, patient_id: int, speciality_id: int, created_at: date) -> None:
        self.patient_id = patient_id
        self.speciality_id = speciality_id
        self.created_at = created_at

    def save(self, medical_record_local_path: str) -> None:
        s3_file_name = self._get_medical_record_file_name(medical_record_local_path=medical_record_local_path)
        insert_fields = '(patient_id, speciality_id, s3_file_name, created_at)'
        values = (
                f"({self.patient_id}, {self.speciality_id}, '{s3_file_name}', " +
                f"'{self.created_at.strftime('%Y-%m-%d')}');"
        )
        RDSService().insert_into_stage(table_name='medical_record', insert_fields=insert_fields, values=values)
        upload_file_to_bucket(
            file_path=medical_record_local_path,
            new_file_name=s3_file_name
        )

    def _get_medical_record_file_name(self, medical_record_local_path: str) -> str:
        file_name = f"{self.patient_id}-{self.speciality_id}-{self.created_at.strftime('%Y%m%d')}"
        file_extension = re.search(r"(\..*)", medical_record_local_path).group(0)
        return file_name + file_extension

    @staticmethod
    def remove_expired_medical_records_data():
        try:
            print('Removing all data related to the expired medical records.')
            medical_records_to_remove = MedicalRecord.retrieve_expired_medical_records()
            if len(medical_records_to_remove) > 0:
                RDSService().delete_from_stage(
                    table_name='medical_record',
                    where_condition="s3_file_name in ('" + "', '".join(medical_records_to_remove) + "')"
                )
                remove_files_from_bucket(medical_records_to_remove)
            else:
                print('All documents are valid, nothing to remove.')
        except Exception as e:
            raise RuntimeError(f'Error while trying to remove expired medical records data: {e}.')

    @staticmethod
    def retrieve_expired_medical_records() -> list:
        try:
            print('Getting expired dates from stage table.')
            mysql_connection = RDSService().mysql_connection
            cutoff_date = (datetime.utcnow() - timedelta(days=7300)).strftime('%Y-%m-%d')
            sql_query = f"select s3_file_name from stage.medical_record where created_at < '{cutoff_date}';"
            with mysql_connection.cursor() as cursor:
                cursor.execute(query=sql_query)
                expired_file_names = cursor.fetchall()
            return [row['s3_file_name'] for row in expired_file_names]
        except Exception as e:
            raise RuntimeError(f'Error while trying to get expired medical records file names: {e}.')

