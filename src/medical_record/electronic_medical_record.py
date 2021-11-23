from datetime import datetime, timedelta, date
from src.medical_record.medical_record import MedicalRecord
from src.services.rds_service import RDSService


class ElectronicMedicalRecord(MedicalRecord):
    def __init__(self, patient_id: int, speciality_id: int, created_at: date) -> None:
        self.patient_id = patient_id
        self.speciality_id = speciality_id
        self.created_at = created_at

    def save(self) -> None:
        insert_fields = '(patient_id, speciality_id, s3_file_name, is_electronic, created_at)'
        values = (
                f"({self.patient_id}, {self.speciality_id}, null, true, " +
                f"'{self.created_at.strftime('%Y-%m-%d')}');"
        )
        RDSService().insert_into_stage(table_name='medical_record', insert_fields=insert_fields, values=values)

    def retrieve_medical_record(self, medical_record_id: int) -> dict:
        try:
            mysql_connection = RDSService().mysql_connection
            sql_query = (
                "select mr.medical_record_id, pat.name, " +
                "date_format(pat.birth_date, '%Y-%m-%d') as created_at, spec.name as speciality " +
                'from stage.medical_record mr ' +
                'inner join patient pat on mr.patient_id = pat.patient_id ' +
                'inner join speciality spec on mr.speciality_id = spec.speciality_id ' +
                f'where mr.medical_record_id = {medical_record_id} and mr.is_electronic = true;'
            )
            with mysql_connection.cursor() as cursor:
                cursor.execute(query=sql_query)
                result = cursor.fetchone()
            if result is not None:
                return result
            else:
                print('Medical record not found.')
                return None
        except Exception as e:
            raise RuntimeError(f'Error while trying to retrieve medical record: {e}.')

    @staticmethod
    def remove_expired_medical_records_data():
        try:
            print('Removing all data related to the expired medical records.')
            cutoff_date = (datetime.utcnow() - timedelta(days=7300)).strftime('%Y-%m-%d')
            RDSService().delete_from_stage(
                table_name='medical_record',
                where_condition=f"created_at < '{cutoff_date}' and is_electronic = true"
            )
        except Exception as e:
            raise RuntimeError(f'Error while trying to remove expired medical records data: {e}.')

