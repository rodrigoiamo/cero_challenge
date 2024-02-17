from dataclasses import dataclass
from datetime import datetime
from ceroai_challenge.utils import from_iso_format
from ceroai_challenge.enums import (
    AppointmentStatus,
    AppointmentType,
    Specialty,
    Policlinic,
)


@dataclass
class Appointment:
    appointment_id: int
    organization_id: str
    date: datetime
    patient_id: str
    doctor_name: str
    doctor_id: str
    specialty: Specialty
    policlinic: Policlinic
    type: AppointmentType
    status: AppointmentStatus

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            appointment_id=data["appointment_id"],
            organization_id=data["organization_id"],
            date=from_iso_format(data["date"]),
            patient_id=data["patient_id"],
            doctor_name=data["doctor_name"],
            doctor_id=data["doctor_id"],
            specialty=Specialty(data["specialty"]),
            policlinic=Policlinic(data["policlinic"]),
            type=AppointmentType(data["type"]),
            status=AppointmentStatus(data["status"]),
        )

    def __str__(self):
        return (
            f"Appointment {self.appointment_id} with {self.doctor_name} on {self.date}"
        )

    def __repr__(self):
        return (
            f"Appointment {self.appointment_id} with {self.doctor_name} on {self.date}"
        )
