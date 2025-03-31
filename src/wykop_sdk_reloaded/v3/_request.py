import requests

from ..exceptions import WykopApiError, WykopApiAuthorizationError, WykopApiNotFoundError, WykopApiLimitExceededError, WykopApiBlockedError


def handle_errors(response: requests.Response):
    match response.status_code:
        case 404:
            raise WykopApiNotFoundError(response.json()["error"])
        case 400:
            raise WykopApiLimitExceededError(response.json()["error"])
        case 401:
            raise WykopApiBlockedError(response.json()["error"])
        case 403:
            raise WykopApiAuthorizationError(response.json()["error"])
        
    if response.status_code >= 300:
        raise WykopApiError(response.json()["error"])


class ApiRequester:
    def __init__(self, url: str, token: str | None):
        self.url = url
        self.header = {
            "Authorization": f"Bearer {token}"
        } if token else {}

    def get(self, params: dict | None = None) -> dict:
        if params:
            params = {k: v for k, v in params.items() if v} 
        
        response = requests.get(self.url, params, headers=self.header)

        handle_errors(response)
        
        return response.json()
    
    def post(self, data: dict | None = None, params: dict | None = None, files: dict | None = None) -> dict | None:
        if data:
            data = {k: v for k, v in data.items() if v}
        if params:
            params = {k: v for k, v in params.items() if v}
        if files:
            files = {k: v for k, v in files.items() if v}
        
        response = requests.post(
            self.url,
            params=params,
            json={"data": data} if data else None,
            files=files if files else None,
            headers=self.header
        )

        handle_errors(response)
        
        return response.json() if response.text else None
    

    def put(self, data: dict | None = None) -> dict | None:
        response = requests.put(
            self.url,
            json={"data": data} if data else None,
            headers=self.header
        )

        handle_errors(response)
        
        return response.json() if response.text else None
    
    def delete(self):
        response = requests.delete(self.url, headers=self.header)

        handle_errors(response)
