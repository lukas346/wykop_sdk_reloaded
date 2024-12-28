from enum import Enum


class RequestType:
    """
    Typ żądania HTTP
    """
    GET = "get"
    POST = "post"
    PUT = "put"
    DELETE = "delete"


class LinkCommentSortType(Enum):
    """
    Sposoby sortowania komentarzy pod znaleziskiem
    """
    NEWEST = "newest"
    BEST = "best"
    OLDEST = "oldest"


class LinkCommentVoteType(Enum):
    """
    Typ oceny komentarza pod znaleziskiem
    """
    UP = "up"
    DOWN = "down"


class LinkType(Enum):
    """
    Typ znaliska (strona główna bądź wykopalisko)
    """
    HOMEPAGE = "homepage"
    UPCOMING = "upcoming"


class LinkVoteDownReason(Enum):
    """
    Powód zakopania znaleziska
    """
    DUPLICATE = 1
    SPAM = 2
    UNTRUE = 3
    INAPPROPRIATE = 4
    UNSUITABLE = 5


class EntriesSortType(Enum):
    """
    Sposób sortowania wpisów
    """
    HOT = "hot"
    NEWEST = "newest"
    ACTIVE = "active"


class EntriesLastUpdateType(Enum):
    """
    (Działa tylko dla gorących wpisów) Określony przedział czasowy dla gorących wpisów
    """
    ONE = 1
    TWO = 2
    THREE = 3
    SIX = 6
    TWELVE = 12
    TWENTY_FOUR = 24


class MediaPhotosType(Enum):
    """
    Przeznaczenie wysłanego zdjęcia
    """
    SETTINGS = "settings"
    COMMENTS = "comments"
    LINKS = "links"


class StreamSortType(Enum):
    """
    Typ obiektów
    """
    ALL = "all"
    BEST = "best"
