from dataclasses import dataclass, field
from ceroai_challenge.models.rules import ContactRule
from typing import List
from datetime import datetime


@dataclass
class ContactedAppointment:
    appointment_id: str
    contact_rule: ContactRule
    date: datetime = field(default_factory=datetime.now)


class Contactability:
    def __init__(self):
        self.contacted_appointments: List[ContactedAppointment] = []

    def add_contacted_appointment(
        self, appointment_id: int, contact_rule: ContactRule
    ) -> None:
        contacted_appointment = ContactedAppointment(
            appointment_id=appointment_id, contact_rule=contact_rule
        )
        self.contacted_appointments.append(contacted_appointment)

    def check_contacted_appointment(
        self, appointment_id: int, contact_rule: ContactRule
    ) -> bool:
        for contacted_appointment in self.contacted_appointments:
            if (
                contacted_appointment.appointment_id == appointment_id
                and contacted_appointment.contact_rule == contact_rule
            ):
                return True
        return False
