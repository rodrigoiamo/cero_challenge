from abc import ABC, abstractmethod
from typing import List
from ceroai_challenge.utils import compute_delta_days_from_now
from ceroai_challenge.models.appointments import Appointment
from ceroai_challenge.enums import (
    Specialty,
    FilterRuleType,
    AppointmentType,
    AppointmentStatus,
    Policlinic,
    ContactRuleType,
)


class FilterRule(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def apply(self, appointment: Appointment) -> bool:
        pass


class FilterRuleFactory:
    @staticmethod
    def create_rule(rule_type: str, **kargs) -> FilterRule:
        if rule_type == FilterRuleType.NOT_VALID_SPECIALTY.value:
            return NotValidSpecialty(*kargs)
        elif rule_type == FilterRuleType.NOT_VALID_DOCTOR.value:
            return NotValidDoctor(*kargs)
        elif rule_type == FilterRuleType.NOT_VALID_DOCTOR_DNI.value:
            return NotValidDoctorDNI(*kargs)
        elif rule_type == FilterRuleType.VALID_APPOINTMENT_TYPE.value:
            return ValidAppointmentType(*kargs)
        elif rule_type == FilterRuleType.VALID_APPOINTMENT_TYPE_POLICLINIC.value:
            return ValidAppointmentTypePoliclinic(*kargs)
        else:
            raise ValueError(f"Rule type {rule_type} not found")


class NotValidDoctorDNI(FilterRule):

    def __init__(self, DNIs: List[str]):
        self.DNIs: List[str] = DNIs
        super().__init__()

    def apply(self, appointment: Appointment) -> bool:
        return appointment.doctor_id not in self.DNIs


class NotValidSpecialty(FilterRule):

    def __init__(self, specialties: List[str]):
        self.specialties: List[Specialty] = specialties
        super().__init__()

    def apply(self, appointment: Appointment) -> bool:
        return appointment.specialty not in self.specialties


class NotValidDoctor(FilterRule):

    def __init__(self, doctors: List[str]):
        self.doctors: List[str] = doctors
        super().__init__()

    def apply(self, appointment: Appointment) -> bool:
        return appointment.doctor_name not in self.doctors


class ValidAppointmentType(FilterRule):
    def __init__(self, appointment_types: List[str]):
        self.appointment_types: List[AppointmentType] = appointment_types
        super().__init__()

    def apply(self, appointment: Appointment) -> bool:
        return appointment.type in self.appointment_types


class ValidAppointmentTypePoliclinic(FilterRule):
    def __init__(self, appointment_status: AppointmentStatus, policlinic: Policlinic):
        self.appointment_status: AppointmentStatus = appointment_status
        self.policlinic: Policlinic = policlinic
        super().__init__()

    def apply(self, appointment: Appointment) -> bool:
        return (
            appointment.type == self.appointment_status
            and appointment.policlinic == self.policlinic
        )


class ContactRule(ABC):
    def __init__(self, overhead: int):
        self.overhead = overhead

    @abstractmethod
    def apply(self, appointment: Appointment) -> bool:
        pass

    @abstractmethod
    def _its_relevant(self, appointment: Appointment) -> bool:
        pass


class ContactRuleFactory:
    @staticmethod
    def create_rule(rule_type: str, **kargs) -> ContactRule:
        if rule_type == ContactRuleType.CONTACT_STATUS.value:
            return ContactStatusRule(**kargs)
        elif rule_type == ContactRuleType.CONTACT_DOCTOR.value:
            return ContactDoctorRule(**kargs)
        else:
            raise ValueError(f"Rule type {rule_type} not found")


class ContactStatusRule(ContactRule):
    def __init__(self, appointment_status: AppointmentStatus, overhead: int):
        self.appointment_status: AppointmentStatus = appointment_status
        super().__init__(overhead)

    def apply(self, appointment: Appointment) -> bool:
        if not self._its_relevant(appointment):
            return False
        return appointment.status == self.appointment_status

    def _its_relevant(self, appointment: Appointment) -> bool:
        days: int = compute_delta_days_from_now(appointment.date)
        return days <= self.overhead


class ContactDoctorRule(ContactRule):
    def __init__(self, doctor_name: str, overhead: int):
        self.doctor_name: str = doctor_name
        super().__init__(overhead)

    def apply(self, appointment: Appointment) -> bool:
        if not self._its_relevant(appointment):
            return False
        return appointment.doctor_name == self.doctor_name

    def _its_relevant(self, appointment: Appointment) -> bool:
        days: int = compute_delta_days_from_now(appointment.date)
        return days == self.overhead
