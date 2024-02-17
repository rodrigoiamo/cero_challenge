from ceroai_challenge.commands.filter_appointments_command import (
    FilterAppointmentsCommand,
)
from ceroai_challenge.models.contactability import Contactability

if __name__ == "__main__":

    simple_contactability = Contactability()
    FilterAppointmentsCommand.perform(simple_contactability)
