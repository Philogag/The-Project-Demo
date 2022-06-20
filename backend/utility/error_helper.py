class BusinessError(Exception):
    message: str

    @classmethod
    def __message__(cls):
        """The default message."""
        return ""

    def __init__(self, message: str = None):
        super().__init__(message if message else self.__message__())
        if message is not None:
            self.message = message


class ClassConfigNotSetError(BusinessError):
    def __init__(self, cls, var_name):
        super().__init__(
            f"{cls.__name__} dose not set {var_name} yet."
        )


class DoesNotSupportUpdatingBySql(BusinessError):
    @classmethod
    def __message__(cls):
        return "Can not update sql data."


class EntityNotFoundError(BusinessError):
    def __init__(self, cls, entity_id, version):
        super().__init__(
            f"{cls.__name__} has no entity of id:{entity_id} at version:{version}"
        )


class InvalidHistoryDataError(BusinessError):
    def __message__(self):
        return "Invalid data version, please refresh."


class InvalidSqlAlchemyClassAttrError(BusinessError):
    def __init__(self, cls, attr):
        super().__init__(f"{cls.__name__} has no attr named {attr}.")


class InvalidSqlAlchemyClassColumnError(BusinessError):
    def __init__(self, cls, column_name):
        super().__init__(f"{cls.__name__} has no valid column named {column_name}.")


class InvalidSqlAlchemyClassError(BusinessError):
    def __init__(self, cls):
        super().__init__(f"Cannot found {cls.__name__}.")


class InvalidSqlAlchemyClassWithIdError(BusinessError):
    def __init__(self, cls):
        super().__init__(f"Cannot found {cls.__name__} with id.")


class InvalidClassAttrError(BusinessError):
    def __init__(self, cls, attr):
        super().__init__(f"{cls.__name__} has no attr named {attr}.")


class NoPermissionError(BusinessError):
    def __init__(self, route):
        super().__init__(f"没有权限: {route}")
