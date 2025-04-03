from dataclasses import dataclass, field
from typing import Optional

from api import client
from database.engine import get_engine_new
from database.unit_of_work import UnitOfWork
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker


@dataclass
class Product:
    id: Optional[str] = field(default=None, init=False)
    planid: str
    benefitid: str

    def __post_init__(self):
        # Paso 2: Producto hijo
        child = client.doQuery(f"SELECT id FROM Products WHERE productname = '{self.benefitid}' LIMIT 1")
        if not child:
            child = client.doCreate('Products', {"productname": self.benefitid, "productcode": self.benefitid})

            # Paso 1: Producto padre (bundle)
            parent = client.doQuery(f"SELECT id FROM Products WHERE productname = '{self.planid}' LIMIT 1")
            if not parent:
                parent = client.doCreate('Products', {"productname": self.planid, "productcode": self.planid})
            else:
                parent = parent[0]  # obtener primer resultado

            # Paso 3: Vincular ambos productos (query SQL directa)
            if not get_engine_new():
                return False

            unit_of_work = UnitOfWork(lambda: sessionmaker(bind=get_engine_new())())

            parent_id = int(parent['id'].split('x')[1])
            child_id = int(child['id'].split('x')[1])

            with unit_of_work as uow:
                try:
                    uow.execute(
                        text(
                            """
                            INSERT INTO vtiger_seproductsrel (crmid, productid, setype)
                            VALUES (:crmid, :productid, 'Products')
                            ON DUPLICATE KEY UPDATE productid=productid;
                        """
                        ),
                        {'crmid': child_id, 'productid': parent_id},
                    )
                    uow.commit()
                    print(f"Producto vinculado correctamente (parent={parent_id}, child={child_id})")

                except Exception as e:
                    uow.rollback()
                    print(f"Error al vincular producto: {e}")

        else:
            child = child[0]  # obtener primer resultado

        self.id = child['id']
