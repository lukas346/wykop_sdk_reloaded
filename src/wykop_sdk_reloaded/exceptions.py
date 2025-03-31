class WykopApiError(Exception):
    """
    Generyczny błąd WykopApiv3
    """
    pass


class WykopApiLimitExceededError(WykopApiError):
    """
    HTTP 400 Limit zapytań został przekroczony
    """
    pass


class WykopApiBlockedError(WykopApiError):
    """
    HTTP 401 Endpoint został zablokowany
    """
    pass


class WykopApiAuthorizationError(WykopApiError):
    """
    HTTP 403 Brak autoryzacji - token niepoprawny albo wygasł i należy go odświeżyć
    """
    pass


class WykopApiNotFoundError(WykopApiError):
    """
    HTTP 404 Brak Endpointu
    """
    pass


class AuthError(Exception):
    pass
