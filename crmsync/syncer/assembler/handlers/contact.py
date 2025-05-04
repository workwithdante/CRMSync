# syncer/assembler/handlers/contact.py

# Importación de las clases y módulos necesarios
from dataclasses import dataclass, field # Importa la clase dataclass y field del módulo dataclasses para la creación de clases de datos, para definir clases con atributos
from datetime import datetime, date # Importa las clases datetime y date del módulo datetime para el manejo de fechas y horas, para trabajar con fechas y horas
import re # Importa el módulo re para el uso de expresiones regulares, para realizar operaciones de búsqueda y manipulación de cadenas
from typing import Optional, List # Importa las clases Optional y List del módulo typing para la definición de tipos, para la definición de tipos de datos
from syncer.assembler.handlers.base import DocTypeHandler # Importa la clase base DocTypeHandler del módulo syncer.assembler.handlers.base, para la herencia de clases

@dataclass
class Contact(DocTypeHandler):
    """
    DocTypeHandler para Contact: contiene toda la lógica de mapeo, normalización
    y construcción de payload para la API de ERPNext.

    Args:
        customer_name (str): Nombre del cliente.
        relationship (str): Relación con el cliente.
        first_name (str): Nombre.
    """
    # Nombre del cliente
    customer_name: str
    # Relación con el cliente
    relationship: str
    # Nombre del contacto
    first_name: str
    # Segundo nombre del contacto
    middle_name: str
    # Apellido del contacto
    last_name: str
    # Cobertura del contacto
    coverage: str
    # Género del contacto
    gender: str
    # Fecha de nacimiento del contacto (opcional)
    day_of_birth: Optional[date]
    # Número de seguro social del contacto (opcional)
    social_security_number: Optional[str]
    # Estado migratorio del contacto (opcional)
    migratory_status: Optional[str]
    # Tipo de trabajo del contacto (opcional)
    job_type: Optional[str]
    # Ingresos del contacto (opcional)
    income: Optional[str]
    # Idioma del contacto (opcional)
    language: Optional[str]
    # Si el contacto fuma (opcional)
    smoke: Optional[str]
    # Si el contacto ha estado en la cárcel (opcional)
    been_in_jail: Optional[str]
    # Teléfono del contacto (opcional)
    phone: Optional[str]
    # Número de móvil del contacto (opcional)
    mobile_no: Optional[str]
    # Correo electrónico 1 del contacto (opcional)
    email1: Optional[str]
    # Correo electrónico 2 del contacto (opcional)
    email2: Optional[str]
    # ID de miembro del contacto (opcional)
    member_id: Optional[str]
    # Usuario del contacto (opcional)
    user: Optional[str]
    # Contraseña del contacto (opcional)
    password: Optional[str]
    # Tipos de documentos del contacto (lista de strings, por defecto una lista vacía)
    document_type: List[str] = field(default_factory=list)
    # Fecha límite del documento del contacto (opcional)
    document_deadline: Optional[str] = None

    def __post_init__(self):
        """
        Método de inicialización posterior.

        Este método se llama después de que se crea una instancia de la clase.
        Se encarga de normalizar los datos y sincronizarlos.
        """
        # Define el tipo de documento
        self.doctype = "Contact"
        # Mapea la relación
        self._map_relationship()
        # Normaliza la cobertura
        self._normalize_coverage()
        # Normaliza el SSN
        self._normalize_ssn()
        # Normaliza las fechas
        self._normalize_dates()
        # Normaliza el género y el idioma
        self._normalize_gender_language()
        # Normaliza los métodos de contacto
        self._normalize_contact_methods()
        # Normaliza el estado migratorio
        self._normalize_migratory_status()
        # Normaliza las preguntas
        self._normalize_questions()
        # Normaliza y sincroniza
        self.normalize_and_sync()

    @classmethod
    def from_row(cls, row, cfg: dict, customer_name: str):
        """
        Método de clase para crear una instancia de Contact desde una fila de datos.

        Args:
            row (dict): Fila de datos.
            cfg (dict): Configuración.
            customer_name (str): Nombre del cliente.

        Returns:
            Contact: Una instancia de la clase Contact.
        """
        # Retorna una instancia de la clase Contact
        return cls(
            customer_name=customer_name,
            relationship=row.get(cfg["relationship"], cfg["relationship"]),
            coverage=row.get(cfg["coverage"], ""),
            first_name=row.get(cfg["first_name"], ""),
            middle_name=row.get(cfg["middle_name"], ""),
            last_name=row.get(cfg["last_name"], ""),
            gender=row.get(cfg["gender"], ""),
            day_of_birth=row.get(cfg["day_of_birth"], None),
            social_security_number=row.get(cfg["social_security_number"], None),
            migratory_status=row.get(cfg["migratory_status"], None),
            job_type=row.get(cfg["job_type"], None),
            income=row.get(cfg["income"], "0"),
            language=row.get(cfg["language"], None),
            smoke=row.get(cfg["smoke"], None),
            been_in_jail=row.get(cfg["been_in_jail"], None),
            phone=row.get(cfg.get("phone"), None),
            mobile_no=row.get(cfg.get("mobile_no"), None),
            email1=row.get(cfg.get("email1"), None),
            email2=row.get(cfg.get("email2"), None),
            member_id=row.get(cfg.get("member_id"), None),
            user=row.get(cfg.get("user"), None),
            password=row.get(cfg.get("password"), None),
        )

    def _map_relationship(self):
        """
        Mapea la relación del contacto.

        Este método se encarga de mapear la relación del contacto a un valor estándar.
        """
        # Mapeo de relaciones
        mapping = {
            "ABUELO(A)":   "Grandparent",
            "HERMANO(A)":  "Brother or Sister (including half and step-siblings)",
            "HIJO(A)":     "Child (including adopted children)",
            "NIETO(A)":    "Grandchild",
            "PADRE/MADRE": "Parent (including adoptive parents)",
            "SOBRINO(A)":  "Nephew or Niece",
            "SUEGRO(O)":   "Mother-in-law or Father-in-law",
            "TIO(A)":      "Uncle or Aunt",
            "HIJASTRO(A)": "Stepchild",
            "CUÑADO(A)":   "Brother-in-law or Sister-in-law",
            "YERNO/NUERA": "Son-in-law or Daughter-in-law",
            "PRIMO(A)":    "First cousin",
            "OTRO":        "Other Relative (including by marriage and adoption)",
        }
        # Si la relación no es Owner o Spouse, mapea la relación a un valor estándar
        if self.relationship not in ("Owner", "Spouse"):
            self.relationship = mapping.get(self.relationship, "Other Relative")

    def _normalize_questions(self):
        """
        Normaliza las respuestas a las preguntas.

        Este método se encarga de normalizar las respuestas a las preguntas
        de fumar y haber estado en la cárcel.
        """
        # Normaliza la respuesta a la pregunta de si fuma
        self.smoke =  'No' if self.smoke != "YES" else 'Yes'
        # Normaliza la respuesta a la pregunta de si ha estado en la cárcel
        self.been_in_jail = 'No' if self.been_in_jail != "YES" else 'Yes'
        
    def _normalize_coverage(self):
        """
        Normaliza la cobertura.

        Este método se encarga de normalizar la cobertura a un valor estándar.
        """
        # Mapeo de coberturas
        mapping = {
            "OBAMACARE": "Obamacare",
            "MEDICARE":  "Medicare",
            "MEDICAID":  "Medicaid",
            "NO APLICA": "Other",
        }
        # Normaliza la cobertura a un valor estándar
        self.coverage = mapping.get(self.coverage.upper(), "Other")

    def _normalize_ssn(self):
        """
        Normaliza el número de seguro social.

        Este método se encarga de normalizar el número de seguro social,
        eliminando caracteres no numéricos y asegurándose de que tenga 9 dígitos.
        """
        # Si el número de seguro social existe
        if self.social_security_number:
            # Elimina caracteres no numéricos y rellena con ceros hasta 9 dígitos
            digits = re.sub(r"\D", "", self.social_security_number).zfill(9)
            # Si tiene 9 dígitos, lo asigna, sino lanza un error
            if len(digits) == 9:
                self.social_security_number = digits
            else:
                raise ValueError("Social Security Number must be 9 digits long.")

    def _normalize_dates(self):
        """
        Normaliza las fechas.

        Este método se encarga de normalizar las fechas al formato YYYY-MM-DD.
        """
        # Si la fecha de nacimiento es un datetime o date, la formatea
        if isinstance(self.day_of_birth, (datetime, date)):
            self.day_of_birth = self.day_of_birth.strftime("%Y-%m-%d")

    def _normalize_gender_language(self):
        """
        Normaliza el género y el idioma.

        Este método se encarga de normalizar el género y el idioma,
        capitalizando la primera letra si existen.
        """
        # Capitaliza el género si existe
        self.gender   = self.gender.capitalize() if self.gender else None
        # Capitaliza el idioma si existe
        self.language = self.language.capitalize() if self.language else None

    def _normalize_contact_methods(self):
        """
        Normaliza los métodos de contacto.

        Este método se encarga de normalizar los métodos de contacto,
        validando el formato del correo electrónico y eliminando caracteres
        no numéricos de los números de teléfono.
        """
        # Expresión regular para validar el formato del correo electrónico
        EMAIL_RX = re.compile(r"^[\w\.-]+@[\w\.-]+\.\w+$")
        # Función para validar el formato del correo electrónico
        def valid_email(e: Optional[str]) -> Optional[str]:
            if not e: return None
            e = e.strip().lower()
            return e if EMAIL_RX.match(e) else None

        # Valida y normaliza el correo electrónico 1
        self.email1 = valid_email(self.email1)
        # Valida y normaliza el correo electrónico 2
        self.email2 = valid_email(self.email2)
        # Elimina caracteres no numéricos del teléfono si existe
        self.phone     = re.sub(r"\D", "", self.phone)     if self.phone else None
        # Elimina caracteres no numéricos del móvil si existe
        self.mobile_no = re.sub(r"\D", "", self.mobile_no) if self.mobile_no else None

    def _normalize_migratory_status(self):
        """
        Normaliza el estado migratorio.

        Este método se encarga de normalizar el estado migratorio a un valor estándar.
        """
        # Mapeo de estados migratorios
        mapping = {
            "CIUDADANO":            "Passport",
            "ANTORCHA":             "Notice of Action (I-797)",
            "NOTICIA DE ACCION":    "Notice of Action (I-797)",
            "RESIDENTE":            "Resident (I-551)",
            "ASILO POLITICO":       "Refugee Travel (I-571)",
            "PERMISO DE TRABAJO":   "Employment Authorization (I-766)",
            "VISA":                 "Visa (temporary I-551)",
            "PAROL":                "Temporary (passport or I-94/I-94A)",
            "TPS":                  "Temporary (passport or I-821)",
            "PASAPORTE VIAJERO":    "Foreign Passport",
            "I-20":                 "Nonimmigrant Student Status (I-20)",
            "I-94":                 "Alien number or I-94 number",
        }
        # Si el estado migratorio existe, lo normaliza a un valor estándar
        if self.migratory_status:
            key = self.migratory_status.strip().upper()
            self.migratory_status = mapping.get(key, None)

    def get_filters(self):
        """
        Obtiene los filtros para buscar el contacto.

        Este método se encarga de obtener los filtros para buscar el contacto
        en la base de datos.
        """
        # Une el nombre, segundo nombre y apellido
        name = " ".join(filter(None, [self.first_name, self.middle_name, self.last_name]))
        # Define los filtros
        filters = [
            ["Contact", "full_name", "like", f"{name}%"],
            ["Contact", "custom_day_of_birth", "=", self.day_of_birth],
        ]
        # Si el número de seguro social existe, agrega el filtro
        if self.social_security_number:
            filters.append(["Contact", "custom_social_security_number", "=", self.social_security_number])
        # Retorna los filtros
        return filters

    def get_filters_child(self):
        """
        Obtiene los filtros para buscar los hijos del contacto.

        Este método se encarga de obtener los filtros para buscar los hijos del contacto
        en la base de datos.
        """
        return None

    def get_existing_name(self):
        """
        Obtiene el nombre existente del contacto.

        Este método se encarga de obtener el nombre existente del contacto.
        """
        # Retorna el nombre completo
        return self.full_name()

    def build_data(self):
        """
        Construye los datos para el contacto.

        Este método se encarga de construir los datos para el contacto
        que se enviarán a la API de ERPNext.
        """
        # Define los datos
        data = {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "middle_name": self.middle_name,
            "custom_day_of_birth": self.day_of_birth,
            "gender": self.gender,
            "links": [{"link_doctype": "Customer", "link_name": self.customer_name}],
        }

        # Emails
        emails = list(filter(None, [self.email1, self.email2]))
        if emails:
            data["email_ids"] = [
                {"email_id": email, "is_primary": i == 0}
                for i, email in enumerate(emails)
            ]

        # Phones
        phones = []
        if self.phone:
            phones.append({"phone": self.phone, "is_primary_phone": 1, "is_primary_mobile_no": 0})
        if self.mobile_no:
            phones.append({"phone": self.mobile_no, "is_primary_phone": 0, "is_primary_mobile_no": 1})
        if phones:
            data["phone_nos"] = phones

        return data

    def full_name(self):
        """
        Obtiene el nombre completo del contacto.

        Este método se encarga de obtener el nombre completo del contacto,
        concatenando el nombre, el apellido y el nombre del cliente.
        """
        # Retorna el nombre completo
        return " ".join(filter(None, [self.first_name, self.middle_name, self.last_name])) + f"-{self.customer_name}"
