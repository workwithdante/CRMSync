# syncer/assembler/linkers/contact_linker.py

# syncer/assembler/linkers/contact_linker.py

from syncer.assembler.core.step import PipelineStep # Importa la clase PipelineStep del módulo syncer.assembler.core.step
from api import client # Importa el módulo client de la API
from syncer.assembler.resolvers.simple_name import SimpleNameResolver # Importa la clase SimpleNameResolver del módulo syncer.assembler.resolvers.simple_name

class ContactLinker(PipelineStep):
    """
    Vinculador de contactos.

    Toma las tuplas pending_links con doctype=="Contact" y vincula
    la cuenta bancaria al Contact correspondiente.
    """
    def __init__(self, person_resolver: SimpleNameResolver):
        """
        Constructor de la clase ContactLinker.

        Args:
            person_resolver (SimpleNameResolver): Resolvedor de nombres de personas.
        """
        # Resolvedor de nombres de personas
        self.resolver = person_resolver

    def execute(self, context: dict) -> None:
        """
        Ejecuta el paso del pipeline.

        Args:
            context (dict): Contexto del pipeline.
        """
        # Obtiene la lista de contactos del contexto
        contacts = context.get("contacts", [])
        # Obtiene el cache de contactos del contexto
        cache    = context.get("contact_cache", {})
        # Obtiene los enlaces pendientes del contexto
        pending  = context.get("pending_links", [])

        # 1) Actualizar valid_names de personas
        names = [c.name.split("-", 1)[0] for c in cache.values()]
        self.resolver.valid_names = names
        self.resolver.first_names = [n.split()[0] for n in names]
        self.resolver.first_names_lower = [fn.lower() for fn in self.resolver.first_names]
        self.resolver.first_name_map_lower = {
            fn.lower(): full for fn, full in zip(self.resolver.first_names, names)
        }

        # 2) Procesar solo los enlaces de tipo "Contact"
        leftovers = []
        # Itera sobre los enlaces pendientes
        for doctype, raw, link_doctype, link_name in pending:
            # Si el tipo de documento no es "Contact" o el raw no existe
            if doctype != "Contact" or not raw:
                # Agrega el enlace a la lista de enlaces restantes
                leftovers.append((doctype, raw, link_doctype, link_name))
                continue

            # Procesa el texto con el resolvedor
            matched = self.resolver.process_text(raw)[0]["matched"]
            # Busca el contacto en la lista de contactos
            contact = next((c for c in contacts if c.name.startswith(matched)), None)
            # Si el contacto existe
            if contact:
                # Actualiza los enlaces del contacto
                client.doUpdateLinks(
                    "Contact",
                    contact.name,
                    [{"link_doctype": link_doctype, "link_name": link_name}],
                )
            # Si no encuentra match, lo dejamos para reintentar más tarde
            else:
                leftovers.append((doctype, raw, link_doctype, link_name))

        # 3) Sustituir pending_links por los que aún no se resolvieron
        context["pending_links"] = leftovers
