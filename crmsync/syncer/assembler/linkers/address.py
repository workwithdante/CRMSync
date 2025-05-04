# syncer/assembler/linkers/address_linker.py

# syncer/assembler/linkers/address_linker.py

from syncer.assembler.core.step import PipelineStep # Importa la clase PipelineStep del módulo syncer.assembler.core.step
from api import client # Importa el módulo client de la API

class AddressLinker(PipelineStep):
    """
    Vinculador de direcciones.

    Toma las tuplas pending_links con doctype=="Address" y vincula
    la cuenta bancaria a la Address cuyo `code` coincide con el pincode.
    """
    def execute(self, context: dict) -> None:
        """
        Ejecuta el paso del pipeline.

        Args:
            context (dict): Contexto del pipeline.
        """
        # Obtiene el cache de direcciones del contexto
        addr_cache = context.get("address_cache", {})
        # Obtiene los enlaces pendientes del contexto
        pending    = context.get("pending_links", [])

        # Inicializa la lista de enlaces restantes
        leftovers = []
        # Itera sobre los enlaces pendientes
        for doctype, raw, link_doctype, link_name in pending:
            # Solo procesamos los enlaces de tipo "Address"
            if doctype != "Address" or not raw:
                leftovers.append((doctype, raw, link_doctype, link_name))
                continue

            # Obtiene el código postal del enlace
            pincode = str(raw).strip()
            # Busca la Address en cache por su atributo `code`
            addr = next(
                (a for a in addr_cache.values() if getattr(a, "code", None) == pincode),
                None
            )
            # Si la dirección existe
            if addr:
                # Actualiza los enlaces de la dirección
                client.doUpdateLinks(
                    "Address",
                    addr.name,
                    [{"link_doctype": link_doctype, "link_name": link_name}],
                )
            # Si no la encontramos, la dejamos para intentar más tarde
            else:
                leftovers.append((doctype, raw, link_doctype, link_name))

        # Reemplaza pending_links por los que aún faltan
        context["pending_links"] = leftovers
