
from syncer.assembler.core.step import PipelineStep # Importa la clase PipelineStep del módulo syncer.assembler.core.step
from syncer.assembler.handlers.bank_account import BankAccount # Importa la clase BankAccount del módulo syncer.assembler.handlers.bank_account
import numpy as np

class BankAccountFactory(PipelineStep):
    """
    Fábrica de cuentas bancarias.

    Esta clase se encarga de crear instancias de la clase BankAccount.
    """
    def __init__(self, mappings, parser_bank):
        """
        Constructor de la clase BankAccountFactory.

        Args:
            mappings (dict): Mapeo de campos.
            parser_bank (ParserBank): Parser para bancos.
        """
        # Mapeo de campos
        self.mappings = mappings
        # Parser para bancos
        self.parser_bank = parser_bank
        # Cache de cuentas bancarias
        self.cache: dict = {}

    def execute(self, context: dict) -> None:
        """
        Ejecuta el paso del pipeline.

        Args:
            context (dict): Contexto del pipeline.
        """
        # Obtiene la fila de datos del contexto
        row = context["row"]
        # Obtiene el cliente del contexto
        customer = context["customer"]
        # Obtiene el primer mapeo de la lista
        m = self.mappings[0]
        # Obtiene el nombre del banco de la fila
        raw_bank = row.get(m["bank_account"]) or ''
        # Obtiene el número de cuenta de la fila
        raw_no   = row.get(m["bank_account_no"]) or ''
        # Si el nombre del banco y el número de cuenta existen
        if raw_bank and len(raw_no) > 3:
            # Procesa el nombre del banco con el parser
            chunk = self.parser_bank.process_text(raw_bank)[0]
            # Obtiene el nombre del banco del resultado del parser
            bank_name = chunk["matched"]
            # Define el tipo de cuenta como "Bank"
            account_type = "Bank"
            # Obtiene los últimos 4 dígitos del número de cuenta
            account_number = raw_no[-4:]
        # Si no, intenta obtener la información de la tarjeta de crédito
        else:
            # Mapeo de tarjetas de crédito
            cards = {"VISA":"Visa Inc","MASTERCARD":"Mastercard Incorporated",
                     "AMERICAN EXPRESS":"American Express Company",
                     "DISCOVERY":"Discover Financial Services"}
            # Obtiene el tipo de cuenta de la fila
            card_acc = row.get(m["card_account"])
            # Define el tipo de cuenta como "Credit Card" o "Debit Card"
            account_type = "Credit Card" if row.get(m["card_type"]) == "Crédito" else "Debit Card"
            # Obtiene el nombre del banco del mapeo de tarjetas
            bank_name = cards.get(card_acc)
            # Obtiene los últimos 4 dígitos del número de tarjeta
            account_number = row.get(m["card_number"])[-4:]
        # Define la clave para el cache
        key = (account_type, bank_name, account_number)
        # Si todos los campos de la clave existen y al menos uno no está vacío
        if all(key) and any(isinstance(s, str) and s.strip() for s in key):
            # Si la clave no está en el cache
            if key not in self.cache:
                # Crea una nueva instancia de BankAccount
                ba = BankAccount.from_row(
                    row, *self.mappings,
                    customer_name=customer.name,
                    account_type=account_type,
                    bank_name=bank_name
                )
                # Agrega la cuenta bancaria al cache
                self.cache[key] = ba
                # Obtiene el código postal de la fila
                p = row.get(m["pincode"])
                # Si el código postal existe, agrega un enlace pendiente
                if p and not np.isnan(p):
                    context.setdefault("pending_links",[]).append(
                        ("Address", str(int(p)), "Bank Account", ba.name)
                    )
                # Obtiene el propietario de la fila
                owner = row.get(m["owner"])
                # Si el propietario existe, agrega un enlace pendiente
                if owner:
                    context.setdefault("pending_links",[]).append(
                        ("Contact", owner, "Bank Account", ba.name)
                    )
        # Agrega la cuenta bancaria al contexto
        context["bank_account"] = self.cache.get(key)
