from ..exceptions import AuthError

from . import _urls
from ._request import ApiRequester


class AuthClient:
    def __init__(self):
        self.key = None
        self.secret = None
        self.jwt_app_token = None
        self.jwt_user_token = None
        self.jwt_refresh_user_token = None

    def __generate_jwt_app_token(self) -> str:
        return ApiRequester(url=_urls.AUTH_URL, token=None).post(
            data={"key": self.key, "secret": self.secret}
        )["data"]["token"]
    
    def check_authentication(self):
        if not self.jwt_app_token and not self.jwt_user_token:
            raise AuthError("Wymagane zalogowanie. Wywołaj AuthClient.authenticate_app() albo AuthClient.authenticate_user()")
        
    def check_user_authentication(self):
        if not self.jwt_user_token or not self.jwt_refresh_user_token:
            raise AuthError("Wymagane zalogowanie uzytkownika. Wywołaj AuthClient.authenticate_user()")
    
    def wykop_connect(self):
        """
        Zwraca link laczacy aplikacje z kontem. Metoda wymagania do uzyskania danych logowania uzytkownika
        """
        print(ApiRequester(url=_urls.CONNECT_URL, token=self.jwt_app_token).get()["data"]["connect_url"])

    def authenticate_app(self, key: str, secret: str):
        self.key = key
        self.secret = secret

        self.jwt_app_token = self.__generate_jwt_app_token()

    def authenticate_user(self, token: str, refresh_token: str):
        self.jwt_user_token = token
        self.jwt_refresh_user_token = refresh_token

    def refresh_user_token(self) -> dict:
        self.check_user_authentication()

        response = ApiRequester(url=_urls.REFRESH_TOKEN_URL, token=None).post(
            data={"refresh_token": self.jwt_refresh_user_token}
        )["data"]

        self.jwt_user_token = response["token"]
        self.jwt_refresh_user_token = response["refresh_token"]

        return response

    def get_jwt_token(self):
        """
        Wybiera bardziej sprawczy token
        """
        return self.jwt_user_token or self.jwt_app_token
