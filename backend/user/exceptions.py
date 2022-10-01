class InvalidPassword(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__("Wrong Password")

class InvalidUser(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__("Invalid User")

class ServerError(Exception):
    def __init__(self, error: Exception = None, *args: object) -> None:
        if(error):
            super().__init__(error.message, *args)
        else:
            super().__init__(*args)


