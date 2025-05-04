# syncer/assembler/factories/contact_factory.py

# syncer/assembler/factories/contact_factory.py

from syncer.assembler.core.step import PipelineStep # Importa la clase PipelineStep del módulo syncer.assembler.core.step
from syncer.assembler.handlers.contact import Contact # Importa la clase Contact del módulo syncer.assembler.handlers.contact

class ContactFactory(PipelineStep):
    """
    PipelineStep que crea y cachea instancias de Contact a partir de cada fila (row).
    No contiene ninguna lógica de normalización ni mapeo: eso lo hace Contact.
    """
    def __init__(self, mappings):
        """
        Constructor de la clase ContactFactory.

        Args:
            mappings (dict): Mapeo de campos.
        """
        # Mapeo de campos
        self.mappings = mappings
        # Cache de contactos
        self.cache: dict[tuple[str,str,str], Contact] = {}

    def execute(self, context: dict) -> None:
        """
        Ejecuta el paso del pipeline.

        Args:
            context (dict): Contexto del pipeline.
        """
        # Obtiene la fila de datos del contexto
        row      = context["row"]
        # Obtiene el cliente del contexto
        customer = context["customer"]
        # Inicializa la lista de contactos
        contacts: list[Contact] = []

        # Itera sobre los mapeos
        for cfg in self.mappings:
            # Obtiene el nombre y apellido del contacto de la fila
            fn = (row.get(cfg["first_name"]) or "").strip()
            ln = (row.get(cfg["last_name"])  or "").strip()
            # Obtiene la fecha de nacimiento del contacto de la fila
            dob = row.get(cfg["day_of_birth"])
            # Si no hay nombre ni apellido, continua con la siguiente iteración
            if not (fn or ln):
                continue

            # Define la clave para el cache
            key = (fn, ln, dob)
            # Si la clave no está en el cache
            if key not in self.cache:
                # Deja que Contact.from_row reciba los valores crudos
                contact = Contact.from_row(row, cfg, customer_name=customer.name)
                # Agrega el contacto al cache
                self.cache[key] = contact

            # Agrega el contacto a la lista de contactos
            contacts.append(self.cache[key])

        # Agrega la lista de contactos al contexto
        context["contacts"]      = contacts
        # Agrega el cache de contactos al contexto
        context["contact_cache"] = self.cache
