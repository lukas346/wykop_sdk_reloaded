from enum import Enum


class RequestType:
    GET = "get"
    POST = "post"
    PUT = "put"
    DELETE = "delete"


class LinkCommentSortType(Enum):
    NEWEST = "newest"
    BEST = "best"
    OLDEST = "oldest"


class LinkCommentVoteType(Enum):
    UP = "up"
    DOWN = "down"


class LinkType(Enum):
    HOMEPAGE = "homepage"
    UPCOMING = "upcoming"


class LinkVoteDownReason(Enum):
    DUPLICATE = 1
    SPAM = 2
    UNTRUE = 3
    INAPPROPRIATE = 4
    UNSUITABLE = 5


class EntriesSortType(Enum):
    HOT = "hot"
    NEWEST = "newest"
    ACTIVE = "active"


class EntriesLastUpdateType(Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    SIX = 6
    TWELVE = 12
    TWENTY_FOUR = 24


class MediaPhotosType(Enum):
    SETTINGS = "settings"
    COMMENTS = "comments"
    LINKS = "links"


class StreamSortType(Enum):
    ALL = "all"
    BEST = "best"
