
class EmailAlreadyExistsError(Exception):
    """Exception raised when attempting to register with an email that already exists."""
    pass

class NoFieldToPatchError(Exception):
    """Exception levantada quando alguem tenta dar patch no banco de dados com os campos desejados vazios."""
    pass

class InvalidMonthFormatError(Exception):
    """Exception levantada quando alguém insere o mês no formato errado. Formato esperado: YYYY-mm"""
    pass
