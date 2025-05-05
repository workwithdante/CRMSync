from syncer.assembler.core.pipeline import Pipeline
from syncer.assembler.factories.address import AddressFactory
from syncer.assembler.factories.bank_account import BankAccountFactory
from syncer.assembler.factories.contact import ContactFactory
from syncer.assembler.factories.customer import CustomerFactory
from syncer.assembler.factories.item import ItemFactory
from syncer.assembler.factories.salesorder import SalesOrderFactory
from syncer.assembler.linkers.address import AddressLinker
from syncer.assembler.linkers.contact import ContactLinker
from syncer.assembler.linkers.document import DocumentLinker
from syncer.assembler.resolvers.simple_name import SimpleNameResolver
from tqdm import tqdm

class PolicyAssembler:
    """
    Ensamblador de pólizas.

    Esta clase se encarga de ensamblar las pólizas para un contacto,
    coordinando la creación de objetos y el establecimiento de relaciones
    entre ellos.
    """
    def __init__(self, config, parser_bank):
        """
        Constructor de la clase PolicyAssembler.

        Inicializa el ensamblador con la configuración y los resolvedores necesarios.

        Args:
            config (dict): Configuración de la aplicación.
            parser_bank (ParserBank): Parser para nombres de bancos.
        """
        self.config = config
        # Un único parser para personas:
        self.parser_person  = SimpleNameResolver(valid_names=[])
        # Un único parser para bancos (lo tenías):
        self.parser_bank    = parser_bank
        # instanciar resolvers y steps
        self.customer_factory   = CustomerFactory(config.customer_mapping)
        self.bank_account_factory = BankAccountFactory(config.bank_account_mapping, parser_bank)
        self.address_factory    = AddressFactory(config.address_mapping[0])
        self.contact_factory    = ContactFactory(config.contact_mapping)
        self.item_factory       = ItemFactory(config.item_mapping)
        self.sales_order_factory  = SalesOrderFactory()
        self.document_linker    = DocumentLinker(self.parser_person)
        self.contact_linker     = ContactLinker(self.parser_person)
        #self.address_linker     = AddressLinker()

        self.pipeline = Pipeline([
            self.customer_factory,
            self.bank_account_factory,
            self.address_factory,
            self.contact_factory,
            self.item_factory,
            self.document_linker,
            self.sales_order_factory,
            self.contact_linker,
            #self.address_linker,
        ])

    def assemble(self, contact_id: str, rows):
        """
        Ensambla las pólizas para un contacto.

        Este método toma un ID de contacto y una lista de filas de datos,
        y ejecuta el pipeline para crear y relacionar los objetos correspondientes.

        Args:
            contact_id (str): ID del contacto.
            rows (list): Lista de filas de datos.
        """
        base_ctx = {
            "config": self.config,
            # exponer caches
            "contact_cache": self.contact_factory.cache,
            "address_cache": self.address_factory.cache,
        }
        for _, row in rows.iterrows():
            ctx = base_ctx.copy()
            ctx.update({"row": row, "rows": rows})
            self.pipeline.run(ctx)
        tqdm.write(
            f"Policy assembled for contact {contact_id}: "
            f"{len(rows)} orders, "
            f"{len(self.contact_factory.cache)} contacts, "
            f"{len(self.address_factory.cache)} addresses created"
        )
