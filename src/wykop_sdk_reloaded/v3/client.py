from . import _urls
from ._utils import auth_user_required
from ._request import ApiRequester
from ._auth import AuthClient
from .types import (
    LinkType,
    LinkVoteDownReason,
    LinkCommentSortType,
    LinkCommentVoteType,
    RequestType,
    EntriesSortType,
    EntriesLastUpdateType,
    MediaPhotosType,
    StreamSortType
)


class _WykopApiClientBase:
    def __init__(self, auth: AuthClient):
        self.auth = auth
        self.auth.check_authentication()

    def raw_request(self, url: str, type: RequestType, data: dict | None = None, params: dict | None = None) -> dict | None:
        """
        Umozliwia bezposrednie odpytanie Wykop API
        """
        match type:
            case RequestType.GET:
                if data:
                    raise WykopApiClient("Metoda GET nie obsługuje wysyłania danych, moze chodzilo ci o parametr params?")
                
                return ApiRequester(url=url, token=self.auth.get_jwt_token()).get(params=params)
            case RequestType.POST:
                return ApiRequester(url=url, token=self.auth.get_jwt_token()).post(data=data, params=params)
            case RequestType.PUT:
                if params:
                    raise WykopApiClient("Metoda PUT nie obsługuje wysyłania parametrów, moze chodzilo ci o parametr data?")

                return ApiRequester(url=url, token=self.auth.get_jwt_token()).put(data=data)
            case RequestType.DELETE:
                if params or data:
                    raise WykopApiClient("Metoda DELETE nie obsługuje wysyłania parametrów i danych.")
                
                return ApiRequester(url=url, token=self.auth.get_jwt_token()).delete()


class _WykopApiClientLinksMixin(_WykopApiClientBase):
    def links_list_links(
            self,
            type: LinkType,
            page: str | None = None,
            limit: int | None = None,
        ) -> dict:
        """
        Zwraca listę znalezisk
        UWAGA: Parametr page przyjmuje dla użytkowników niezalogowanych int z numerem strony, a dla zalogowanych hash strony.
        UWAGA2: Standardowa paginacja jest dostępna tylko dla użytkowników niezalogowanych. Paginacja dla użytkowników zalogowanych będzie zwracać hash next dla następnej strony i prev dla poprzedniej.
        UWAGA3: Dla parametru type=upcoming (wykopalisko) paginacja przyjmuje parametr page jako int z nr strony, zarówno dla użytkowników zalogowanych i niezalogowanych
        """
        return ApiRequester(
            url=_urls.LINKS_URL,
            token=self.auth.get_jwt_token()
        ).get(params={
            "type": type.value,
            "page": page,
            "limit": limit
        })
    
    def links_get_link(
            self,
            link_id: str
        ):
        """
        Wymagana zalogowania uzytkownika

        Szczególy znaleziska
        """
        return ApiRequester(
            url=_urls.LINKS_LINK_URL(link_id),
            token=self.auth.get_jwt_token()
        ).get()
    
    @auth_user_required
    def links_delete_link(
            self,
            link_id: str
        ):
        """
        Wymagana zalogowania uzytkownika

        Usuwanie znaleziska
        """
        return ApiRequester(
            url=_urls.LINKS_LINK_URL(link_id),
            token=self.auth.get_jwt_token()
        ).delete()
    
    @auth_user_required
    def links_update_link(
        self,
        link_id: str,
        title: str,
        description: str,
        tags: list[str],
        adult: bool,
        photo: str | None = None
    ):
        """
        Wymaga zalogowania uzytkownika.

        Można modyfikować tylko własne znaleziska. 
        Autor może modyfikować wpis 15 minut od daty dodania. Link nie możne się znajdować na stronie głwnej. 
        UWAGA: Gdy znalezisko ma ustalone zdjęcie, a w edycji atrybut "photo" nie zostanie przesłany lub 
        będzie przesłany jako null - zdjęcie zostanie usunięte.

        params photo: Załącznik użytkownika. W celu dodania należy podać "key" pliku z media/photo. 
        Akceptowane są tylko pliki przesłane jako typ links.
        params tags: Tagi. Można wysłać do 6 tagów (bez '#').
        """
        return ApiRequester(
            url=_urls.LINKS_LINK_URL(link_id),
            token=self.auth.get_jwt_token()
        ).post({
            "title": title,
            "description": description,
            "tags": tags,
            "adult": adult,
            "photo": photo
        })
    
    @auth_user_required
    def links_vote_up_link(
            self,
            link_id: str
        ):
        """
        Wymagana zalogowania uzytkownika

        Wykopanie znaleziska
        """
        return ApiRequester(
            url=_urls.LINKS_VOTE_UP_URL(link_id),
            token=self.auth.get_jwt_token()
        ).post()
    
    @auth_user_required
    def links_vote_down_link(
            self,
            link_id: str,
            reason: LinkVoteDownReason
        ):
        """
        Wymaga zalogowania uzytkownika

        Zakopanie znaleziska
        """
        return ApiRequester(
            url=_urls.LINKS_VOTE_DOWN_URL(link_id, reason.value),
            token=self.auth.get_jwt_token()
        ).post()
    
    @auth_user_required
    def links_vote_revoke_link(
            self,
            link_id: str
        ):
        """
        Wymaga zalogowania uzytkownika

        Cofnięcie wykopania lub zakopania znaleziska
        """
        return ApiRequester(
            url=_urls.LINKS_VOTES_URL(link_id),
            token=self.auth.get_jwt_token()
        ).delete()


class _WykopApiClientLinkCommentsMixin(_WykopApiClientBase):
    def link_comments_list_comments(
        self,
        link_id: str,
        sort: LinkCommentSortType = LinkCommentSortType.NEWEST,
        page: str | None = None,
        limit: int | None = None,
    ) -> dict:
        """
        Komentarze do znaleziska
        """
        return ApiRequester(
            url=_urls.LINK_COMMENTS_URL(link_id),
            token=self.auth.get_jwt_token()
        ).get(params={
            "sort": sort.value,
            "page": page,
            "limit": limit
        })
    
    @auth_user_required
    def link_comments_create_comment(
            self,
            link_id: str,
            content: str | None = None,
            photo: str | None = None,
            embed: str | None = None,
            adult: bool | None = None,

        ) -> dict:
        """
        Wymaga zalogowania uzytkownika.

        Dodawanie nowego komentarza do wykopaliska
        """
        return ApiRequester(
            url=_urls.LINK_COMMENTS_URL(link_id),
            token=self.auth.get_jwt_token()
        ).post(data={
            "content": content,
            "photo": photo,
            "embed": embed,
            "adult": adult
        })
    
    @auth_user_required
    def link_comments_create_comment_to_comment(
            self,
            link_id: str,
            comment_id: str,
            content: str | None = None,
            photo: str | None = None,
            embed: str | None = None,
            adult: bool | None = None,

        ) -> dict:
        """
        Wymaga zalogowania uzytkownika.

        Dodawanie nowego podkomentarza do istniejącego komentarza
        """
        return ApiRequester(
            url=_urls.LINK_COMMENTS_COMMENT_URL(link_id, comment_id),
            token=self.auth.get_jwt_token()
        ).post(data={
            "content": content,
            "photo": photo,
            "embed": embed,
            "adult": adult
        })
    
    @auth_user_required
    def link_comments_update_comment(
            self,
            link_id: str,
            comment_id: str,
            content: str | None = None,
            photo: str | None = None,
            embed: str | None = None,
            adult: bool | None = None,

        ) -> dict:
        """
        Wymaga zalogowania uzytkownika.

        Edycja komentarza do wykopaliska
        """
        return ApiRequester(
            url=_urls.LINK_COMMENTS_COMMENT_URL(link_id, comment_id),
            token=self.auth.get_jwt_token()
        ).put(data={
            "content": content,
            "photo": photo,
            "embed": embed,
            "adult": adult
        })
    
    @auth_user_required
    def link_comments_delete_comment(
            self,
            link_id: str,
            comment_id: str
        ):
        """
        Wymaga zalogowania uzytkownika.

        Usuwanie komentarza do wykopaliska
        """
        return ApiRequester(
            url=_urls.LINK_COMMENTS_COMMENT_URL(link_id, comment_id),
            token=self.auth.get_jwt_token()
        ).delete()
    
    @auth_user_required
    def link_comments_vote_comment(
            self,
            link_id: str,
            comment_id: str,
            type: LinkCommentVoteType,
        ):
        """
        Wymaga zalogowania uzytkownika.

        Glosowanie na komentarz do wykopaliska
        """
        return ApiRequester(
            url=_urls.LINK_COMMENTS_COMMENT_VOTE_URL(link_id, comment_id, type.value),
            token=self.auth.get_jwt_token()
        ).post()
   
    @auth_user_required
    def link_comments_vote_revoke_comment(
            self,
            link_id: str,
            comment_id: str,
        ):
        """
        Wymaga zalogowania uzytkownika.

        Cofanie oceny komentarza do wykopaliska
        """
        return ApiRequester(
            url=_urls.LINK_COMMENTS_COMMENT_VOTE_REVOKE_URL(link_id, comment_id),
            token=self.auth.get_jwt_token()
        ).delete()


class _WykopApiClientLinkDraftMixin(_WykopApiClientBase):
    @auth_user_required
    def links_draft_list_drafts(self):
        """
        Wymaga zalogowania uzytkownika.

        Lista wersji roboczych linków zalogowanego użytkownika
        Wersje robocze są kasowane po upływie 24h.
        """
        return ApiRequester(
            url=_urls.LINK_DRAFTS_URL,
            token=self.auth.get_jwt_token()
        ).get()
    
    @auth_user_required
    def links_draft_create_draft_step_one(self, url: str):
        """
        Wymaga zalogowania uzytkownika.

        Dodawanie nowego linku w wersji roboczej krok pierwszy
        """
        return ApiRequester(
            url=_urls.LINK_DRAFTS_URL,
            token=self.auth.get_jwt_token()
        ).post({"url": url})
    
    @auth_user_required
    def links_draft_create_draft_step_two(
        self,
        key: str,
        title: str,
        description: str,
        tags: list[str],
        adult: bool,
        photo: str | None = None
    ):
        """
        Wymaga zalogowania uzytkownika.

        Dodawanie nowego linku w wersji roboczej krok drugi - publikacja.

        params photo: Załącznik użytkownika. W celu dodania należy podać "key" pliku z media/photo. 
        Akceptowane są tylko pliki przesłane jako typ links.
        params tags: Tagi. Można wysłać do 6 tagów (bez '#').
        """
        return ApiRequester(
            url=_urls.LINK_DRAFTS_DRAFT_URL(key),
            token=self.auth.get_jwt_token()
        ).post({
            "title": title,
            "description": description,
            "tags": tags,
            "adult": adult,
            "photo": photo,
            "selected_image": 1
        })
    
    @auth_user_required
    def links_draft_update_draft(
        self,
        key: str,
        title: str | None = None,
        description: str | None = None,
        tags: list[str] | None = None,
        adult: bool | None = None,
        photo: str | None = None
    ):
        """
        Wymaga zalogowania uzytkownika.

        Aktualizacja linku w wersji roboczej

        params photo: Załącznik użytkownika. W celu dodania należy podać "key" pliku z media/photo. 
        Akceptowane są tylko pliki przesłane jako typ links.
        params tags: Tagi. Można wysłać do 6 tagów (bez '#').
        """
        return ApiRequester(
            url=_urls.LINK_DRAFTS_DRAFT_URL(key),
            token=self.auth.get_jwt_token()
        ).put({
            "title": title,
            "description": description,
            "tags": tags,
            "adult": adult,
            "photo": photo,
            "selected_image": 1
        })

    @auth_user_required
    def links_draft_get_draft(self, key: str):
        """
        Wymaga zalogowania uzytkownika.

        Zwraca wersję robocza linku
        """
        return ApiRequester(
            url=_urls.LINK_DRAFTS_DRAFT_URL(key),
            token=self.auth.get_jwt_token()
        ).get()

    @auth_user_required
    def links_draft_delete_draft(self, key: str):
        """
        Wymaga zalogowania uzytkownika.

        Usuwa wersję robocza linku
        """
        return ApiRequester(
            url=_urls.LINK_DRAFTS_DRAFT_URL(key),
            token=self.auth.get_jwt_token()
        ).delete()


class _WykopApiClientTagsMixin(_WykopApiClientBase):
    def tags_get_popular_tags(self) -> dict:
        """
        Zwraca listę popularnych tagów.
        """
        return ApiRequester(
            url=_urls.TAGS_POPULAR_URL,
            token=self.auth.get_jwt_token()
        ).get()
    
    def tags_get_popular_user_tags(self) -> dict:
        """
        Kolekcja popularnych tagów autorskich (max do 10 wyników)
        """
        return ApiRequester(
            url=_urls.TAGS_POPULAR_USER_URL,
            token=self.auth.get_jwt_token()
        ).get()
        
    def tags_get_related_tag(self, tag: str) -> dict:
        """
        Kolekcja powiązanych tagów (max do 10 wyników)
        """
        return ApiRequester(
            url=_urls.TAGS_RELATED_TAG_URL(tag),
            token=self.auth.get_jwt_token()
        ).get()
    
    def tags_get_detail_of_tag(self, tag: str) -> dict:
        """
        Szczegóły tagu
        """
        return ApiRequester(
            url=_urls.TAGS_DETAIL_TAG_URL(tag),
            token=self.auth.get_jwt_token()
        ).get()
    
    @auth_user_required
    def tags_edit_tag(self, tag: str, photo: str, description: str) -> str:
        """
        Wymaga zalogowania uzytkownika.

        Właściciel tagu może modyfikować tło (base64 str) oraz opis tagu.
        """
        return ApiRequester(
            url=_urls.TAGS_DETAIL_TAG_URL(tag),
            token=self.auth.get_jwt_token()
        ).put({
            "photo": photo,
            "description": description
        })
    
    def tags_get_stream_of_tag(
            self,
            tag: str,
            sort: StreamSortType = StreamSortType.ALL,
            page: str | None = None,
            limit: int | None = None,
            year: int | None = None,
            month: int | None = None
        ) -> dict:
        """
        Zwraca pełną liste wpisów i znalezisk z konkretnego tagu UWAGA: 
        Parametr page przyjmuje dla użytkowników niezalogowanych int z numerem strony, a dla zalogowanych hash strony. 
        UWAGA2: Standardowa paginacja jest dostępna tylko dla użytkowników niezalogowanych. 
        Paginacja dla użytkowników zalogowanych będzie zwracać hash next dla następnej strony i prev dla poprzedniej.
        """
        return ApiRequester(
            url=_urls.TAGS_STREAM_TAG_URL(tag),
            token=self.auth.get_jwt_token()
        ).get(params={
            "sort": sort.value,
            "page": page,
            "limit": limit,
            "year": year,
            "month": month
        })
    
    def tags_get_tag_owners(
            self,
            tag: str,
        ) -> dict:
        """
        Kolekcja autorów tagu (short profile)
        """
        return ApiRequester(
            url=_urls.TAGS_TAG_OWNERS_URL(tag),
            token=self.auth.get_jwt_token()
        ).get()


class _WykopApiClientArticleMixin(_WykopApiClientBase):
    def articles_list_articles_by_tag(
            self,
            tag: str,
            sort: StreamSortType = StreamSortType.ALL,
            page: str | None = None,
            limit: int | None = None,
            year: int | None = None,
            month: int | None = None
        ) -> dict:
        """
        Zwraca pełną liste artykułów konkretnego tagu 
        UWAGA: Parametr page przyjmuje dla użytkowników niezalogowanych int z numerem strony, a dla zalogowanych hash strony. 
        UWAGA2: Standardowa paginacja jest dostępna tylko dla użytkowników niezalogowanych. 
        Paginacja dla użytkowników zalogowanych będzie zwracać hash next dla następnej strony i prev dla poprzedniej.
        """
        return ApiRequester(
            url=_urls.TAGS_STREAM_TAG_URL(tag),
            token=self.auth.get_jwt_token()
        ).get(params={
            "type": "article",
            "sort": sort.value,
            "page": page,
            "limit": limit,
            "year": year,
            "month": month
        })
    
    def articles_get_article(
        self,
        article_id: str
    ) -> dict:
        """
        Pobranie informacji o artykule
        """
        return ApiRequester(
            url=_urls.ARTICLES_ARTICLE_URL(article_id),
            token=self.auth.get_jwt_token()
        ).get()


class _WykopApiClientEntriesMixin(_WykopApiClientBase):
    @auth_user_required
    def entries_create_entry(
            self,
            content: str | None = None,
            photo: str | None = None,
            embed: str | None = None,
            adult: bool | None = None,

        ) -> dict:
        """
        Wymaga zalogowania uzytkownika.

        Dodawanie nowego wpisu na mikroblogu
        """
        return ApiRequester(
            url=_urls.ENTRIES_URL,
            token=self.auth.get_jwt_token()
        ).post(data={
            "content": content,
            "photo": photo,
            "embed": embed,
            "adult": adult
        })
    
    def entries_list_entries(
        self,
        sort: EntriesSortType = EntriesSortType.HOT,
        last_update: EntriesLastUpdateType = EntriesLastUpdateType.TWELVE,
        page: str | None = None,
        limit: int | None = None,
    ) -> dict:
        """
        Zwraca wpisy z mikrobloga. 
        UWAGA: Parametr page przyjmuje dla użytkowników niezalogowanych int z numerem strony, a dla zalogowanych hash strony. 
        UWAGA2: Standardowa paginacja jest dostępna tylko dla użytkowników niezalogowanych. 
        Paginacja dla użytkowników zalogowanych będzie zwracać hash next dla następnej strony i prev dla poprzedniej.
        """
        return ApiRequester(
            url=_urls.ENTRIES_URL,
            token=self.auth.get_jwt_token()
        ).get(params={
            "sort": sort.value,
            "last_update": last_update.value,
            "page": page,
            "limit": limit
        })
    
    def entries_list_entries_by_tag(
            self,
            tag: str,
            sort: StreamSortType = StreamSortType.ALL,
            page: str | None = None,
            limit: int | None = None,
            year: int | None = None,
            month: int | None = None
        ) -> dict:
        """
        Zwraca pełną liste wpisów konkretnego tagu 
        UWAGA: Parametr page przyjmuje dla użytkowników niezalogowanych int z numerem strony, a dla zalogowanych hash strony. 
        UWAGA2: Standardowa paginacja jest dostępna tylko dla użytkowników niezalogowanych. 
        Paginacja dla użytkowników zalogowanych będzie zwracać hash next dla następnej strony i prev dla poprzedniej.
        """
        return ApiRequester(
            url=_urls.TAGS_STREAM_TAG_URL(tag),
            token=self.auth.get_jwt_token()
        ).get(params={
            "type": "entry",
            "sort": sort.value,
            "page": page,
            "limit": limit,
            "year": year,
            "month": month
        })
    
    def entries_get_entry(
        self,
        entry_id: str
    ) -> dict:
        """
        Pobranie wpisu z mikrobloga
        """
        return ApiRequester(
            url=_urls.ENTRIES_ENTRY_URL(entry_id),
            token=self.auth.get_jwt_token()
        ).get()
    
    @auth_user_required
    def entries_update_entry(
        self,
        entry_id: str,
        content: str | None = None,
        photo: str | None = None,
        embed: str | None = None,
        adult: bool | None = None,
    ) -> dict:
        """
        Wymaga zalogowania uzytkownika.

        Edycja wpisu z mikrobloga
        """
        return ApiRequester(
            url=_urls.ENTRIES_ENTRY_URL(entry_id),
            token=self.auth.get_jwt_token()
        ).put({
            "content": content,
            "photo": photo,
            "embed": embed,
            "adult": adult
        })
    
    @auth_user_required
    def entries_delete_entry(
        self,
        entry_id: str
    ) -> dict:
        """
        Wymaga zalogowania uzytkownika.

        Usuwanie wpisu z mikrobloga
        """
        return ApiRequester(
            url=_urls.ENTRIES_ENTRY_URL(entry_id),
            token=self.auth.get_jwt_token()
        ).delete()
    
    @auth_user_required
    def entries_vote_up_entry(
        self,
        entry_id: str
    ) -> dict:
        """
        Wymaga zalogowania uzytkownika.

        Głosowanie na wpis z mikrobloga
        """
        return ApiRequester(
            url=_urls.ENTRIES_ENTRY_VOTES_URL(entry_id),
            token=self.auth.get_jwt_token()
        ).post()
    
    @auth_user_required
    def entries_vote_revoke_entry(
        self,
        entry_id: str
    ) -> dict:
        """
        Wymaga zalogowania uzytkownika.

        Cofnięcie głosu na wpis z mikrobloga
        """
        return ApiRequester(
            url=_urls.ENTRIES_ENTRY_VOTES_URL(entry_id),
            token=self.auth.get_jwt_token()
        ).delete()


class _WykopApiClientEntryCommentsMixin(_WykopApiClientBase):
    def entry_comments_list_comments(
        self,
        entry_id: str,
        page: str | None = None,
        limit: int | None = None,
    ) -> dict:
        """
        Komentarze do wpisu z mikrobloga
        """
        return ApiRequester(
            url=_urls.ENTRY_COMMENTS_URL(entry_id),
            token=self.auth.get_jwt_token()
        ).get(params={
            "page": page,
            "limit": limit
        })
    
    @auth_user_required
    def entry_comments_create_comment(
            self,
            entry_id: str,
            content: str | None = None,
            photo: str | None = None,
            embed: str | None = None,
            adult: bool | None = None,

        ) -> dict:
        """
        Wymaga zalogowania uzytkownika.

        Dodawanie nowego komentarza do wpisu na mikroblogu
        """
        return ApiRequester(
            url=_urls.ENTRY_COMMENTS_URL(entry_id),
            token=self.auth.get_jwt_token()
        ).post(data={
            "content": content,
            "photo": photo,
            "embed": embed,
            "adult": adult
        })

    @auth_user_required
    def entry_comments_update_comment(
            self,
            entry_id: str,
            comment_id: str,
            content: str | None = None,
            photo: str | None = None,
            embed: str | None = None,
            adult: bool | None = None,

        ) -> dict:
        """
        Wymaga zalogowania uzytkownika.

        Edycja komentarza do wpisu na mikroblogu
        """
        return ApiRequester(
            url=_urls.ENTRY_COMMENTS_COMMENT_URL(entry_id, comment_id),
            token=self.auth.get_jwt_token()
        ).put(data={
            "content": content,
            "photo": photo,
            "embed": embed,
            "adult": adult
        })
    
    @auth_user_required
    def entry_comments_delete_comment(
        self,
        entry_id: str,
        comment_id: str
    ) -> dict:
        """
        Wymaga zalogowania uzytkownika.

        Usuwanie komentarza do wpisu z mikrobloga
        """
        return ApiRequester(
            url=_urls.ENTRY_COMMENTS_COMMENT_URL(entry_id, comment_id),
            token=self.auth.get_jwt_token()
        ).delete()
    
    @auth_user_required
    def entry_comments_vote_up_comment(
        self,
        entry_id: str,
        comment_id: str
    ) -> dict:
        """
        Wymaga zalogowania uzytkownika.

        Głosowanie na komentarz do wpisu z mikrobloga
        """
        return ApiRequester(
            url=_urls.ENTRY_COMMENTS_VOTES_URL(entry_id, comment_id),
            token=self.auth.get_jwt_token()
        ).post()
    
    @auth_user_required
    def entry_comments_vote_revoke_comment(
        self,
        entry_id: str,
        comment_id: str
    ) -> dict:
        """
        Wymaga zalogowania uzytkownika.

        Cofanie głosu na komentarz do wpisu z mikrobloga
        """
        return ApiRequester(
            url=_urls.ENTRY_COMMENTS_VOTES_URL(entry_id, comment_id),
            token=self.auth.get_jwt_token()
        ).delete()


class _WykopApiClientNotificationsMixin(_WykopApiClientBase):
    @auth_user_required
    def notifinations_status(self) -> dict:
        """
        Wymaga zalogowania uzytkownika.

        Sprawdzenie czy zalogowany użytkownik posiada nowe powiadomienia
        """
        return ApiRequester(
            url=_urls.NOTIFICATIONS_STATUS_URL,
            token=self.auth.get_jwt_token()
        ).get()

    @auth_user_required
    def notifinations_list_entries(self) -> dict:
        """
        Wymaga zalogowania uzytkownika.

        Pobranie notyfikacji
        """
        return ApiRequester(
            url=_urls.NOTIFICATIONS_ENTRIES_URL,
            token=self.auth.get_jwt_token()
        ).get()

    @auth_user_required
    def notifinations_mark_all_entries_readed(self):
        """
        Wymaga zalogowania uzytkownika.

        Oznaczenie powiadomień użytkownika jako przeczytane
        """
        return ApiRequester(
            url=_urls.NOTIFICATIONS_ENTRIES_ALL_URL,
            token=self.auth.get_jwt_token()
        ).put()
    
    @auth_user_required
    def notifinations_delete_all_entries(self):
        """
        Wymaga zalogowania uzytkownika.

        Usunięcie wszystkich powiadomień użytkownika
        """
        return ApiRequester(
            url=_urls.NOTIFICATIONS_ENTRIES_ALL_URL,
            token=self.auth.get_jwt_token()
        ).delete()

    @auth_user_required
    def notifinations_get_entry(self, entry_id: str) -> dict:
        """
        Wymaga zalogowania uzytkownika.

        Pobranie jednej notyfikacji dla zalogowanego użytkownika
        """
        return ApiRequester(
            url=_urls.NOTIFICATIONS_ENTRY_URL(entry_id),
            token=self.auth.get_jwt_token()
        ).get()

    @auth_user_required
    def notifinations_mark_entry_readed(self, entry_id: str):
        """
        Wymaga zalogowania uzytkownika.

        Ustawienie powiadomienia jako przeczytane
        """
        return ApiRequester(
            url=_urls.NOTIFICATIONS_ENTRY_URL(entry_id),
            token=self.auth.get_jwt_token()
        ).put()

    @auth_user_required
    def notifinations_delete_entry(self, entry_id: str):
        """
        Wymaga zalogowania uzytkownika.

        Usunięcie powiadomienia
        """
        return ApiRequester(
            url=_urls.NOTIFICATIONS_ENTRY_URL(entry_id),
            token=self.auth.get_jwt_token()
        ).delete()
    
    @auth_user_required
    def notifinations_list_pms(self) -> dict:
        """
        Wymaga zalogowania uzytkownika.

        Pobranie listy notyfikacji o prywatnych wiadomościach użytkownika
        """
        return ApiRequester(
            url=_urls.NOTIFICATIONS_PMS_URL,
            token=self.auth.get_jwt_token()
        ).get()

    @auth_user_required
    def notifinations_mark_all_pms_readed(self):
        """
        Wymaga zalogowania uzytkownika.

        Ustawienie wszystkich powiadomień z prywatnych wiadomości jako przeczytane
        """
        return ApiRequester(
            url=_urls.NOTIFICATIONS_PMS_ALL_URL,
            token=self.auth.get_jwt_token()
        ).put()
    
    @auth_user_required
    def notifinations_delete_all_pms(self):
        """
        Wymaga zalogowania uzytkownika.

        Usunięcie wszystkich powiadomień z prywatnych wiadomości
        """
        return ApiRequester(
            url=_urls.NOTIFICATIONS_PMS_ALL_URL,
            token=self.auth.get_jwt_token()
        ).delete()

    @auth_user_required
    def notifinations_get_pm(self, pm_id: str) -> dict:
        """
        Wymaga zalogowania uzytkownika.

        Pobranie pw dla zalogowanego użytkownika
        """
        return ApiRequester(
            url=_urls.NOTIFICATIONS_PM_URL(pm_id),
            token=self.auth.get_jwt_token()
        ).get()

    @auth_user_required
    def notifinations_mark_pm_readed(self, pm_id: str):
        """
        Wymaga zalogowania uzytkownika.

        Ustawienie pw jako przeczytanej
        """
        return ApiRequester(
            url=_urls.NOTIFICATIONS_PM_URL(pm_id),
            token=self.auth.get_jwt_token()
        ).put()

    @auth_user_required
    def notifinations_delete_pm(self, pm_id: str):
        """
        Wymaga zalogowania uzytkownika.

        Usunięcie pw
        """
        return ApiRequester(
            url=_urls.NOTIFICATIONS_PM_URL(pm_id),
            token=self.auth.get_jwt_token()
        ).delete()


class _WykopApiClientMediaPhotosMixin(_WykopApiClientBase):
    @auth_user_required
    def photos_upload_url(self, url: str, type: MediaPhotosType) -> dict:
        """
        Wymaga zalogowania uzytkownika.

        Wgrywanie wskazanego pliku przez URL na serwer
        Dozwolone jest wgrywanie multimedialnych plików o następujących 
        mimetype: 'image/jpeg', 'image/jpg', 'image/pjpeg', 'image/gif', 'image/png', 'image/x-png'. 
        Maksymalny rozmiar pliku to 10 MB.
        """
        return ApiRequester(
            url=_urls.MEDIA_PHOTOS_UPLOAD_URL,
            token=self.auth.get_jwt_token()
        ).post(data={"url": url}, params={"type": type.value})
    
    @auth_user_required
    def photos_upload_file(self, picf: str, type: MediaPhotosType) -> dict:
        """
        Wymaga zalogowania uzytkownika.

        Wgrywanie wskazanego pliku przez URL na serwer
        Dozwolone jest wgrywanie multimedialnych plików o następujących 
        mimetype: 'image/jpeg', 'image/jpg', 'image/pjpeg', 'image/gif', 'image/png', 'image/x-png'. 
        Maksymalny rozmiar pliku to 10 MB.
        """
        return ApiRequester(
            url=_urls.MEDIA_PHOTOS_UPLOAD_FILE,
            token=self.auth.get_jwt_token()
            ).post(files={"file": open(picf,"rb")}, params={"type": type.value})


    @auth_user_required
    def photos_delete_photo(self, key: str) -> dict:
        """
        Wymaga zalogowania uzytkownika.

        Właściciel pliku posiada możliwość jego usunięcia z serwera.
        """
        return ApiRequester(
            url=_urls.MEDIA_PHOTOS_GET_PHOTO_URL(key),
            token=self.auth.get_jwt_token()
        ).delete()


class _WykopApiClientMediaEmedMixin(_WykopApiClientBase):
    @auth_user_required
    def embed_upload_url(self, url: str) -> dict:
        """
        Wymaga zalogowania uzytkownika.

        Wgrywanie podglądu embed przez URL na serwer
        """
        return ApiRequester(
            url=_urls.MEDIA_EMBED_UPLOAD_URL,
            token=self.auth.get_jwt_token()
        ).post({"url": url})


class _WykopApiClientProfileMixin(_WykopApiClientBase):
    @auth_user_required
    def profiles_get_my_profile(self) -> dict:
        """
        Pobranie danych publicznych i prywatnych zalogowanego użytkownika.
        """
        return ApiRequester(
            url=_urls.PROFILES_OWN_PROFILE_URL,
            token=self.auth.get_jwt_token()
        ).get()

    @auth_user_required
    def profiles_get_my_profile_short(self) -> dict:
        """
        Pobranie danych publicznych zalogowanego użytkownika - wersja skrócona.
        """
        return ApiRequester(
            url=_urls.PROFILES_OWN_SHORT_PROFILE_URL,
            token=self.auth.get_jwt_token()
        ).get()

    def profiles_get_profile(self, username: str) -> dict:
        """
        Pobranie danych publicznych danego użytkownika.
        """
        return ApiRequester(
            url=_urls.PROFILES_PROFILE_URL(username),
            token=self.auth.get_jwt_token()
        ).get()

    def profiles_get_profile_short(self, username: str) -> dict:
        """
        Pobranie danych publicznych danego użytkownika - wersja skrócona.
        """
        return ApiRequester(
            url=_urls.PROFILES_PROFILE_SHORT_URL(username),
            token=self.auth.get_jwt_token()
        ).get()

    def profiles_get_profile_actions(self, username: str) -> dict:
        """
        Lista akcji (wpisy i znaleziska) autorstwa danego użytkownika
        """
        return ApiRequester(
            url=_urls.PROFILES_PROFILE_ACTIONS_URL(username),
            token=self.auth.get_jwt_token()
        ).get()

    def profiles_get_profile_entries_added(self, username: str, page: str | None = None, limit: int | None = None) -> dict:
        """
        Lista wpisów autorstwa danego użytkownika
        """
        return ApiRequester(
            url=_urls.PROFILES_PROFILE_ENTRIES_ADDED_URL(username),
            token=self.auth.get_jwt_token()
        ).get({"page": page, "limit": limit})

    def profiles_get_profile_entries_voted(self, username: str, page: str | None = None, limit: int | None = None) -> dict:
        """
        Lista plusowanych wpisów przez użytkownika
        """
        return ApiRequester(
            url=_urls.PROFILES_PROFILE_ENTRIES_VOTED_URL(username),
            token=self.auth.get_jwt_token()
        ).get({"page": page, "limit": limit})

    def profiles_get_profile_entries_commented(self, username: str, page: str | None = None, limit: int | None = None) -> dict:
        """
        Lista komentarzy autorstwa danego użytkownika wraz z wpisem
        """
        return ApiRequester(
            url=_urls.PROFILES_PROFILE_ENTRIES_COMMENTED_URL(username),
            token=self.auth.get_jwt_token()
        ).get({"page": page, "limit": limit})

    def profiles_get_profile_links_added(
            self,
            username: str,
            page: str | None = None,
            limit: int | None = None
        ) -> dict:
        """
        Lista znalezisk autorstwa danego użytkownika
        """
        return ApiRequester(
            url=_urls.PROFILES_PROFILE_LINKS_ADDED_URL(username),
            token=self.auth.get_jwt_token()
        ).get({"page": page, "limit": limit})
    
    def profiles_get_profile_links_published(self, username: str, page: str | None = None, limit: int | None = None) -> dict:
        """
        Lista znalezisk autorstwa danego użytkownika, które trafiły na stronę główną
        """
        return ApiRequester(
            url=_urls.PROFILES_PROFILE_LINKS_PUBLISHED_URL(username),
            token=self.auth.get_jwt_token()
        ).get({"page": page, "limit": limit})

    def profiles_get_profile_links_up(self, username: str, page: str | None = None, limit: int | None = None) -> dict:
        """
        Lista znalezisk wykopanych przez danego użytkownika
        """
        return ApiRequester(
            url=_urls.PROFILES_PROFILE_LINKS_UP_URL(username),
            token=self.auth.get_jwt_token()
        ).get({"page": page, "limit": limit})

    @auth_user_required
    def profiles_get_profile_links_down(self, username: str, page: str | None = None, limit: int | None = None) -> dict:
        """
        Lista znalezisk zakopanych przez zalogowanego użytkownika
        """
        return ApiRequester(
            url=_urls.PROFILES_PROFILE_LINKS_DOWN_URL(username),
            token=self.auth.get_jwt_token()
        ).get({"page": page, "limit": limit})

    def profiles_get_profile_links_commented(self, username: str, page: str | None = None, limit: int | None = None) -> dict:
        """
        Lista komentarzy autorstwa danego użytkownika wraz ze znaleziskiem
        """
        return ApiRequester(
            url=_urls.PROFILES_PROFILE_LINKS_COMMENTED_URL(username),
            token=self.auth.get_jwt_token()
        ).get({"page": page, "limit": limit})

    def profiles_get_profile_links_related(self, username: str, page: str | None = None, limit: int | None = None) -> dict:
        """
        Lista linków powiązanych autorstwa danego użytkownika wraz ze znaleziskiem
        """
        return ApiRequester(
            url=_urls.PROFILES_PROFILE_LINKS_RELATED_URL(username),
            token=self.auth.get_jwt_token()
        ).get({"page": page, "limit": limit})

    def profiles_get_profile_badges(self, username: str) -> dict:
        """
        Pobiera listę osiągnięć użytkownika
        """
        return ApiRequester(
            url=_urls.PROFILES_PROFILE_BADGES_URL(username),
            token=self.auth.get_jwt_token()
        ).get()

    def profiles_get_profile_tags(self, username: str) -> dict:
        """
        Lista tagów autorskich użytkownika
        """
        return ApiRequester(
            url=_urls.PROFILES_PROFILE_TAGS_URL(username),
            token=self.auth.get_jwt_token()
        ).get()

    def profiles_get_profile_observed_tags(self, username: str) -> dict:
        """
        Pobranie obserwowanych tagów użytkownika
        """
        return ApiRequester(
            url=_urls.PROFILES_PROFILE_OBSERVED_TAGS_URL(username),
            token=self.auth.get_jwt_token()
        ).get()

    def profiles_get_profile_users_following(self, username: str) -> dict:
        """
        Lista osób obserwowanych przez danego użytkownika
        """
        return ApiRequester(
            url=_urls.PROFILES_PROFILE_OBSERVED_FOLLOWING_URL(username),
            token=self.auth.get_jwt_token()
        ).get()

    def profiles_get_profile_users_followers(self, username: str) -> dict:
        """
        Lista osób obserwujących danego użytkownika
        """
        return ApiRequester(
            url=_urls.PROFILES_PROFILE_OBSERVED_FOLLOWERS_URL(username),
            token=self.auth.get_jwt_token()
        ).get()

class _WykopApiClientPMMixin(_WykopApiClientBase):
    @auth_user_required
    def pms_mark_all_pms_readed(self):
        """
        Oznacza wszystkie otrzymane wiadomości jako odczytanie.

        Wymaga zalogowania uzytkownika.
        """
        return ApiRequester(
            url=_urls.PMS_READ_ALL_URL,
            token=self.auth.get_jwt_token()
        ).put()
    
    @auth_user_required
    def pms_list_conversations(self, username: str | None = None):
        """
        Lista konwersacji

        params username: nazwa użytkownika (min. 3 znaki)

        Wymaga zalogowania uzytkownika.
        """
        return ApiRequester(
            url=_urls.PMS_CONVERSATIONS_URL,
            token=self.auth.get_jwt_token()
        ).get({"query": username})

    @auth_user_required
    def pms_create_pm(
        self, 
        username: str,
        content: str,
        photo: str | None = None,
        embed: str | None = None):
        """
        Dodawanie nowej wiadomości

        Wymaga zalogowania uzytkownika.
        """
        return ApiRequester(
            url=_urls.PMS_CONVERSATION_URL(username),
            token=self.auth.get_jwt_token()
        ).post({"content": content, "photo": photo, "embed": embed})

    @auth_user_required
    def pms_get_conversation(
        self,
        username: str,
        prev_message: str | None = None,
        next_message: str | None = None
    ):
        """
        Lista wiadomości z użytkownikiem

        params prev_message: identyfikator (key) najstarszej widocznej wiadomości. Po jego podaniu zostaną doczytane starsze wiadomości.
        params next_message: identyfikator (key) najnowszej widocznej wiadomości. Po jego podaniu zostaną doczytane nowsze wiadomości.

        Wymaga zalogowania uzytkownika.
        """
        return ApiRequester(
            url=_urls.PMS_CONVERSATION_URL(username),
            token=self.auth.get_jwt_token()
        ).get({"prev_message": prev_message, "next_message": next_message})

    @auth_user_required
    def pms_delete_conversation(
        self,
        username: str
    ):
        """
        Usuwa konwersację. Znika tylko po stronie osoby wykonującej akcję.

        Wymaga zalogowania uzytkownika.
        """
        return ApiRequester(
            url=_urls.PMS_CONVERSATION_URL(username),
            token=self.auth.get_jwt_token()
        ).delete()


class WykopApiClient(
    _WykopApiClientLinksMixin,
    _WykopApiClientLinkCommentsMixin,
    _WykopApiClientLinkDraftMixin,
    _WykopApiClientArticleMixin,
    _WykopApiClientTagsMixin,
    _WykopApiClientEntriesMixin,
    _WykopApiClientEntryCommentsMixin,
    _WykopApiClientNotificationsMixin,
    _WykopApiClientMediaPhotosMixin,
    _WykopApiClientMediaEmedMixin,
    _WykopApiClientProfileMixin,
    _WykopApiClientPMMixin
):
    pass
