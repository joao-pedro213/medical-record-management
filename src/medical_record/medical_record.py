from abc import ABC


class MedicalRecord(ABC):
    def __init__(self) -> None:
        pass

    def save(self) -> None:
        pass

    def retrieve_medical_record(self) -> None:
        pass

    @staticmethod
    def remove_expired_medical_records_data() -> None:
        pass


