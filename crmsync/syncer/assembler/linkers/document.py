# syncer/assembler/linkers/document_linker.py

# syncer/assembler/linkers/document_linker.py

from syncer.assembler.core.step import PipelineStep # Importa la clase PipelineStep del módulo syncer.assembler.core.step
from syncer.assembler.resolvers.simple_name import SimpleNameResolver # Importa la clase SimpleNameResolver del módulo syncer.assembler.resolvers.simple_name

class DocumentLinker(PipelineStep):
    """
    Vinculador de documentos.

    Resuelve documentos asociados a Contact instances.
    No toca pending_links; añade tipos y deadlines directamente a los objetos.
    """
    def __init__(self, person_resolver: SimpleNameResolver):
        """
        Constructor de la clase DocumentLinker.

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
        # Obtiene la fila de datos del contexto
        row      = context["row"]
        # Obtiene la lista de contactos del contexto
        contacts = context.get("contacts", [])
        # Obtiene el cache de contactos del contexto
        cache    = context.get("contact_cache", {})
        # Obtiene el cliente del contexto
        customer = context["customer"]

        # 1) Actualizar valid_names para que incluyan TODOS los contactos creados
        names = [c.name.split("-", 1)[0] for c in cache.values()]
        self.resolver.valid_names = names or [customer.name]
        # reconstruir índices internos
        self.resolver.first_names = [n.split()[0] for n in self.resolver.valid_names]
        self.resolver.first_names_lower = [fn.lower() for fn in self.resolver.first_names]
        self.resolver.first_name_map_lower = {
            fn.lower(): full for fn, full in zip(self.resolver.first_names, self.resolver.valid_names)
        }

        # 2) Extraer documentos de la fila
        docs = {
            row.get(f"document_person_{i}"): row.get(f"document_name_{i}")
            for i in range(1, 6)
            if row.get(f"document_name_{i}")
        }
        # 3) Resolver y asignar
        for raw_person, doc_type in docs.items():
            # Si la persona no existe, continua con la siguiente iteración
            if not raw_person:
                continue
            # Procesa el texto con el resolvedor
            matched = self.resolver.process_text(raw_person)[0]["matched"]
            # Busca el contacto en la lista de contactos
            target  = next((c for c in contacts if c.name.startswith(matched)), None)
            # Si el contacto existe
            if target:
                # Agrega el tipo de documento a la lista de tipos de documentos del contacto
                target.document_type.append(doc_type)
                # Asigna la fecha límite del documento al contacto
                target.document_deadline = row.get("document_deadline")
