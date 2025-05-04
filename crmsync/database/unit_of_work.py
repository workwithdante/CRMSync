# Unit of Work pattern implementation for database transactions
class UnitOfWork:
    """
    Implementación del patrón Unit of Work para las transacciones de la base de datos.
    """
    def __init__(self, session_factory):
        """
        Inicializa una nueva instancia de UnitOfWork.

        Args:
            session_factory: Función de fábrica para crear nuevas sesiones.
        """
        # Store factory function to create new sessions
        self.session_factory = session_factory

    def __enter__(self):
        """
        Crea una nueva sesión al entrar en el contexto.
        """
        # Create new session when entering context
        self.session = self.session_factory()
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Maneja la finalización de la transacción.
        """
        # Handle transaction completion
        if exc_type is not None:
            # Rollback on exception
            self.session.rollback()
        else:
            # Commit if successful
            self.session.commit()
        # Always close the session
        self.session.close()
