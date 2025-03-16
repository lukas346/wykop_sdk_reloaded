class WykopApiError(Exception):
    """
    Generyczny błąd WykopApiv3
    """
    pass


class WykopApiAuthorizationError(WykopApiError):
    """
    HTTP 403 Brak autoryzacji
    """
    pass


class WykopApiNotFoundError(WykopApiError):
    """
    HTTP 404 Brak Endpointu
    """
    pass


class WykopApiLimitExceededError(WykopApiError):
    """
    HTTP 400 Limit zapytań został przekroczony
    """
    pass


class AuthError(Exception):
    pass
