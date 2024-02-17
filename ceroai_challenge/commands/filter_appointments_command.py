import json

from typing import List, Dict

from ceroai_challenge.models.appointments import Appointment
from ceroai_challenge.models.rules_parser import RuleParser
from ceroai_challenge.models.rules import FilterRule, ContactRule
from ceroai_challenge.models.contactability import Contactability


class FilterAppointmentsCommand:
    """
    Represents a command to filter appointments based on rules and contactability.

    Args:
        contactability (Contactability): The contactability object used to check and update contactability status.

    Attributes:
        filter_rules (Dict[str, List[FilterRule]]): The filter rules to be applied for each organization.
        contact_rules (Dict[str, List[ContactRule]]): The contact rules to be applied for each organization.
        contactability (Contactability): The contactability object used to check and update contactability status.
        appointments (List[Appointment]): The list of appointments to be filtered.
        output_appointments (List[Appointment]): The list of filtered appointments.

    """

    @classmethod
    def perform(cls, contactability: Contactability):
        """
        Perform the filter appointments command.

        Args:
            contactability (Contactability): The contactability object used to check and update contactability status.

        Returns:
            None

        """
        return cls(contactability)._perform()

    def __init__(self, contactability: Contactability):
        """
        Initialize a new instance of FilterAppointmentsCommand.

        Args:
            contactability (Contactability): The contactability object used to check and update contactability status.

        """
        self.filter_rules: Dict[str, List[FilterRule]] = None
        self.contact_rules: Dict[str, List[ContactRule]] = None
        self.contactability = contactability
        self.appointments: List[Appointment] = None
        self.output_appointments: List[Appointment] = None

    def _perform(self):
        """
        Perform the filter appointments command.

        Returns:
            None

        """
        self.__get_rules()
        self.__get_appointments()
        self.__check_contactability()
        self.__apply_rules()
        self.__update_contactability()
        print(self.output_appointments)

    def __get_rules(self):
        """
        Get the filter and contact rules from the JSON file.

        Returns:
            None

        """
        with open("ceroai_challenge/mock_data/mock_rules.json") as f:
            json_rules = json.load(f)

        self.filter_rules, self.contact_rules = RuleParser.parse_rules(json_rules)

    def __get_appointments(self):
        """
        Get the appointments from the JSON file.

        Returns:
            None

        """
        with open("ceroai_challenge/mock_data/mock_appointments.json") as f:
            appointments = json.load(f)
        self.appointments = [
            Appointment.from_dict(appointment) for appointment in appointments
        ]

    def __check_contactability(self):
        """
        Check the contactability status of each appointment and remove contacted appointments.

        Returns:
            None

        """
        for appointment in self.appointments:
            for rule in self.contact_rules[appointment.organization_id]:
                if self.contactability.check_contacted_appointment(
                    appointment.appointment_id, rule
                ):
                    self.appointments.remove(appointment)

    def __apply_rules(self):
        """
        Apply the filter and contact rules to filter the appointments.

        Returns:
            None

        """
        self.__apply_filter_rules()
        self.__apply_contact_rules()
        self.output_appointments = self.appointments

    def __apply_filter_rules(self):
        """
        Apply the filter rules to filter the appointments.

        Returns:
            None

        """
        for appointment in self.appointments:
            for rule in self.filter_rules[appointment.organization_id]:
                if rule.apply(appointment):
                    self.appointments.remove(appointment)

    def __apply_contact_rules(self):
        """
        Apply the contact rules to filter the appointments.

        Returns:
            None

        """
        for appointment in self.appointments:
            for rule in self.contact_rules[appointment.organization_id]:
                if rule.apply(appointment):
                    self.appointments.remove(appointment)

    def __update_contactability(self):
        """
        Update the contactability status for each appointment.

        Returns:
            None

        """
        for appointment in self.output_appointments:
            for rule in self.contact_rules[appointment.organization_id]:
                self.contactability.add_contacted_appointment(
                    appointment.appointment_id, rule
                )
