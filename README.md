# Wykop SDK Reloaded

[![PyPI version](https://badge.fury.io/py/wykop-sdk-reloaded.svg)](https://badge.fury.io/py/wykop-sdk-reloaded)

![](https://wykop.pl/cdn/c3201142/comment_ngdZRBR0tJ8YW99kIj66o0KiHeFrapCO.jpg)

SDK umozliwijące komunikację z API (v3) wykopu na podstawie [oficjalnej dokumentacji](https://doc.wykop.pl/#/).

## Dokumentacja

[Link do dokumentacji ](https://lukas346.github.io/wykop_sdk_reloaded/)

Jeśli brakuje akcji w sdk mozna bezposrednio wyslac request do wykop api dzięki metodzie `raw_request`.
```python
api.raw_request("https://wykop.pl/api/v3/tags/popular", RequestType.GET, data=None)
```

## Instalacja

```bash
pip install wykop_sdk_reloaded
```

## Przykładowe uzycie

```python
from wykop_sdk_reloaded.v3.client import AuthClient, WykopApiClient

auth = AuthClient()
auth.authenticate_user("<USER_JWT_TOKEN>", "<USER_REFRESH_TOKEN>")
auth.refresh_user_token()

api = WykopApiClient(auth)

# tworzy wpis na mikroblogu
api.entries_create_entry("michal bialek sami wiecie co #wykop")
# pobiera listę wpisów z mikrobloga
api.entries_list_entries()
```

```python
from wykop_sdk_reloaded.v3.client import AuthClient, WykopApiClient

auth = AuthClient()
"""
autoryzując się w ten sposob masz tylko dostep do operacji odczytu.
Reszta wymaga WykopApiClient.authenticate_user()
""" 
auth.authenticate_app("<APP_KEY>", "<APP_SECRET>")

api = WykopApiClient(auth)

# pobiera listę wpisów z mikrobloga
api.entries_list_entries()
```

W razie wątpliwości przeczytaj README do końca i rzuć okiem na [testy](https://github.com/lukas346/wykop_sdk_reloaded/blob/main/tests/test_client.py).

## Autoryzacja przez Wykop API

### Utworzenie aplikacji 

By móc korzystać z api wykopu potrzebujecie utworzyć aplikację na stronie [dev.wykop.pl](https://dev.wykop.pl).


Klikacie w przycisk "utwórz aplikację". Zaznaczacie uprawnienia wedle uznania.

![](https://i.ibb.co/Yb1C27t/Zrzut-ekranu-2024-03-7-o-12-45-54.png)

Akceptujecie regulamin i klikacie "dodaj aplikację".

Na liście powinna ukazać wam się świezo dodana pozycja:

![](https://i.ibb.co/M11m064/Zrzut-ekranu-2024-03-7-o-12-48-48.png)

Kopiujecie klucz API oraz Sekret i wklejacie go do tego fragmentu kodu:
```python
auth = AuthClient()
auth.authenticate_app("<APP_KEY>", "<APP_SECRET>")
```

Dzięki temu mozecie wykonywać ządania przez SDK. **Uwaga, by móc tworzyć, edytować, usuwać, głosować i mieć dostęp do powiadomień musicie się dodatkowo zalogować. Ten etap wystarczy do pobierania danych i w sumie nic poza tym.**

### Zalogowanie uzytkownikiem

By móc tworzyć, edytować, usuwać, głosować i mieć dostęp do powiadomień musicie się dodatkowo zalogować. Oto instrukcja jak to zrobić.


Gdy juz macie dane aplikacji wywołujecie metodę `.wykop_connect()` klasy `AuthClient` która zwraca Wam link pod który musicie się udać.
```python
from wykop_sdk_reloaded.v3.client import AuthClient

auth = AuthClient()
auth.authenticate_app("<APP_KEY>", "<APP_SECRET>")

# zwraca link do wykopu na który musicie wejsc
auth.wykop_connect()
``` 

Link powinien wyglądać tak: `https://wykop.pl/connect/10d711dfc86f361b6a3349dd1b71c19132f88cc1`

Po wejściu powinno wam wyskoczyć okienko łączące wasze konto z aplikacją. Wybierzcie jakie uprawnienia powinien mieć wasz uzytkownik api a następnie kliknijcie "połącz z aplikacją".

![](https://i.ibb.co/1LG7HQL/Zrzut-ekranu-2024-03-7-o-13-03-56.png)

Po kliknięciu zostajecie przekierowani na stronę zdefiniowaną przy tworzeniu aplikacji w polu "Podaj adres zwrotny dla WykopConnect". 

U mnie będzie to: `http://api/?token=eyJ041424iJ3QiLCJhbGciOiJIUzI1NiJ9.bG9yZW0gaXBzdW1sb3JlbSBpcHN1bWxvcmVtIGlwc3VtbG9yZW0gaXBzdW1sb3JlbSBpcHN1bWxvcmVtIGlwc3VtbG9yZW0gaXBzdW0=&rtoken=3e39e42414248c4c79ee221ef8f10af55252db20139eb5c2617a188115f7c2758`

Wyciągacie z URLa token i rtoken, zapisujecie gdzieś sobie na przykład w pliku `.env` waszej aplikacji i teraz w końcu mozecie korzystac z pelni mozliwosci wykopowego api.

```python
from wykop_sdk_reloaded.v3.client import AuthClient, WykopApiClient

auth = AuthClient()
# USER_JWT_TOKEN to token, a USER_REFRESH_TOKEN to rtoken z urla
auth.authenticate_user("<USER_JWT_TOKEN>", "<USER_REFRESH_TOKEN>")

api = WykopApiClient(auth)

# tworzy wpis na mikroblogu
api.entries_create_entry("michal bialek sami wiecie co #wykop")
```

Michal Białek jak zwykle przekombinował ale co mozna poradzic.

## Decyzje projektowe
### As explicit as possible
Unikam automagicznych funkcjonalności dlatego na przykład nie ma automatycznego odświezania tokenu uzytkownika API. Osoba korzystająca z SDK musi to zrobić manualnie. Najbardziej leniwy sposób to robienie tego za kazdym razem przy inicjacji obiektu wtedy macie gwarancję, ze uzywacie aktualnego tokenu:
```python
from wykop_sdk_reloaded.v3.client import AuthClient

auth = AuthClient()
auth.authenticate_user("<USER_JWT_TOKEN>", "<USER_REFRESH_TOKEN>")
auth.refresh_user_token()
```

Tokeny mają ustawiony krotki okres waznosci więc podejrzewam, ze to jest najbardziej praktyczna opcja.

### SDK blisko Wykop API
Postanowiłem zwracać praktycznie surowe dane z api wykopu zamiast zdeserializowanych list obiektów. Ma to jedną duzą zaletę - znaczie ułatwiania utrzymywanie biblioteki przy jednoczesnej duzej elastyczności w przetwarzaniu odpowiedzi przez uzytkowników SDK. Jeśli struktura odpowiedzi się zmieni to znaczy, ze wykop zmienił swoje API i wystarczy, ze dokonacie zmian w kodzie zamiast czekania na nową wersję SDK.

Wiele bibliotek ma tendencje do zbyt duzej abstrakcji co powoduje, ze nie są wstanie nadązyć za zmianami w API a przez to stają się niepraktyczne dla programistów którzy są zmuszeni do napisania własnego wrappera.

Jeśli brakuje Wam implementacji jakiegoś endpointu albo obecna jest niepełna to oczywiście utwórzcie ticket ale pamiętajcie, ze mozecie zawsze uzywać `WykopApiClient.raw_request()`. Pomysł został zaczerpnięty z ORMów, które mają metodę awaryjną do wykonywania napisanego przez programistę SQLa.

### Dlaczego polski
Z wykopu korzystają polacy (ewentualnie ruskie i ukraińskie trolle). Język angielski w komentarzach nie ma sensu dla polskojęzycznego odbiorcy. Nazwy obiektów i metod są po angielsku tylko dlatego, ze wymagają tego dobre praktyki programistyczne.

## Etyka
Nie napisałem tego SDK by jakieś trolle i boty spamowały na wykopie. Niestety nie jestem wstanie tego skontrolować więc zotaje sprawiedliwość boska tak zwana pośmiertna. SDK zostało stworzone do pomocy fajnym projektom, jak na przykład [WykopGPT](https://wykop-gpt.lol). 

## Kontakt

SDK nie jest kompletne, jeśli będzie Wam czegoś brakowało to dodajcie swoje Issue albo PR, które są oczywiście mile widziane.
