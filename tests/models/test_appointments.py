import unittest
from datetime import datetime
from ceroai_challenge.models.appointments import (
    Appointment,
    Specialty,
    Policlinic,
    AppointmentType,
    AppointmentStatus,
)


class TestAppointment(unittest.TestCase):
    def test_from_dict(self):
        data = {
            "appointment_id": 1,
            "organization_id": "org123",
            "date": "2022-01-01T10:00:00",
            "patient_id": "patient123",
            "doctor_name": "Dr. John Doe",
            "doctor_id": "doctor123",
            "specialty": "CARDIOLOGY",
            "policlinic": "HOSPITAL",
            "type": "CONTROL",
            "status": "CONFIRMED",
        }
        appointment = Appointment.from_dict(data)
        self.assertEqual(appointment.appointment_id, 1)
        self.assertEqual(appointment.organization_id, "org123")
        self.assertEqual(appointment.date, datetime(2022, 1, 1, 10, 0, 0))
        self.assertEqual(appointment.patient_id, "patient123")
        self.assertEqual(appointment.doctor_name, "Dr. John Doe")
        self.assertEqual(appointment.doctor_id, "doctor123")
        self.assertEqual(appointment.specialty, Specialty.CARDIOLOGY)
        self.assertEqual(appointment.policlinic, Policlinic.HOSPITAL)
        self.assertEqual(appointment.type, AppointmentType.CONTROL)
        self.assertEqual(appointment.status, AppointmentStatus.CONFIRMED)

    def test_str_representation(self):
        appointment = Appointment(
            appointment_id=1,
            organization_id="org123",
            date=datetime(2022, 1, 1, 10, 0, 0),
            patient_id="patient123",
            doctor_name="Dr. John Doe",
            doctor_id="doctor123",
            specialty=Specialty.CARDIOLOGY,
            policlinic=Policlinic.HOSPITAL,
            type=AppointmentType.CONTROL,
            status=AppointmentStatus.CONFIRMED,
        )
        expected_str = "Appointment 1 with Dr. John Doe on 2022-01-01 10:00:00"
        self.assertEqual(str(appointment), expected_str)

    def test_repr_representation(self):
        appointment = Appointment(
            appointment_id=1,
            organization_id="org123",
            date=datetime(2022, 1, 1, 10, 0, 0),
            patient_id="patient123",
            doctor_name="Dr. John Doe",
            doctor_id="doctor123",
            specialty=Specialty.CARDIOLOGY,
            policlinic=Policlinic.HOSPITAL,
            type=AppointmentType.CONTROL,
            status=AppointmentStatus.CONFIRMED,
        )
        expected_repr = "Appointment 1 with Dr. John Doe on 2022-01-01 10:00:00"
        self.assertEqual(repr(appointment), expected_repr)


if __name__ == "__main__":
    unittest.main()
