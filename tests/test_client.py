from pprint import pprint as print
from unittest import TestCase
import os

from src.wykop_sdk_reloaded.v3.client import AuthClient, WykopApiClient
from src.wykop_sdk_reloaded.v3.types import LinkType, LinkVoteDownReason, LinkCommentVoteType, RequestType, EntriesSortType, MediaPhotosType
from src.wykop_sdk_reloaded.exceptions import AuthError


env = os.getenv


class TestReadOnlyWykopApiV3Client(TestCase):
    def setUp(self):
        auth = AuthClient()
        auth.authenticate_app(env("WYKOP_APP_KEY"), env("WYKOP_APP_SECRET"))

        self.api = WykopApiClient(auth)    

    def test_read_only_operations(self):
        tag = "wykop"
        
        self.api.tags_get_detail_of_tag(tag)
        self.api.tags_get_popular_tags()
        self.api.tags_get_popular_user_tags()
        self.api.tags_get_related_tag(tag)
        self.api.tags_get_stream_of_tag(tag)
        self.api.tags_get_tag_owners(tag)
        self.api.entries_list_entries()

    def test_not_permitted(self):
        with self.assertRaises(AuthError):
            self.api.notifinations_list_entries()
            self.api.entries_create_entry("lorem " * 40)

    
    def test_raw_request(self):
        self.assertGreater(
            len(self.api.raw_request("https://wykop.pl/api/v3/tags/popular", RequestType.GET)["data"]),
            0
        )


class TestWykopApiV3Client(TestCase):
    def setUp(self):
        auth = AuthClient()
        auth.authenticate_user(
            token=env("WYKOP_USER_TOKEN"),
            refresh_token=env("WYKOP_USER_REFRESH_TOKEN")
        )
        auth.refresh_user_token()
        
        self.api = WykopApiClient(auth)

    def test_tags(self):
        tag = "wykop"

        self.api.tags_get_detail_of_tag(tag)
        self.api.tags_get_popular_tags()
        self.api.tags_get_popular_user_tags()
        self.api.tags_get_related_tag(tag)
        self.api.tags_get_stream_of_tag(tag)
        self.api.tags_get_tag_owners(tag)

    def test_entries(self):
        response = self.api.entries_create_entry("lorem " * 40)
        entry_id = str(response["data"]["id"])

        self.api.entries_get_entry(entry_id)
        self.api.entries_update_entry(entry_id, 'ipsum'* 20)

        self.api.entry_comments_list_comments(entry_id)

        response = self.api.entry_comments_create_comment(entry_id, "ipsum lorem" * 5)
        entry_comment_id = str(response["data"]["id"])
        
        self.api.entry_comments_list_comments(entry_id)
        self.api.entry_comments_update_comment(entry_id, entry_comment_id, "test " * 5)
        self.api.entry_comments_delete_comment(entry_id, entry_comment_id)

        self.api.entries_delete_entry(entry_id)

    def test_entries_voting(self):
        self.api.entries_list_entries(sort=EntriesSortType.NEWEST)
        response = self.api.entries_list_entries_by_tag("wykop")
        entry_id = response["data"][0]["id"]

        self.api.entries_vote_up_entry(entry_id)
        self.api.entries_vote_revoke_entry(entry_id)

    def test_links(self):
        response = self.api.links_list_links(LinkType.HOMEPAGE)
        link_id = response["data"][0]["id"]

        self.api.links_vote_down_link(link_id, LinkVoteDownReason.INAPPROPRIATE)
        self.api.links_vote_revoke_link(link_id)
        self.api.links_vote_up_link(link_id)
        self.api.links_vote_revoke_link(link_id)

        response = self.api.link_comments_list_comments(link_id)
        comment_id = response["data"][0]["id"]
        self.api.link_comments_vote_comment(link_id, comment_id, LinkCommentVoteType.UP)
        self.api.link_comments_vote_revoke_comment(link_id, comment_id)

        response = self.api.link_comments_create_comment(link_id, "test "* 10)
        own_comment_id = response["data"]["id"]

        self.api.link_comments_update_comment(link_id, own_comment_id, content="albo" * 10)
        response = self.api.link_comments_create_comment_to_comment(link_id, own_comment_id, content="albo" * 10)
        own_comment_to_comment_id = response["data"]["id"]

        self.api.link_comments_delete_comment(link_id, own_comment_id)
        self.api.link_comments_delete_comment(link_id, own_comment_to_comment_id)
        
    def test_notifications(self):
        self.api.notifinations_list_entries()
        self.api.notifinations_status()
        # self.api.notifinations_mark_all_readed()
        # self.api.notifinations_delete_all()

        response = self.api.notifinations_list_pms()
        # pm_id = response["data"][0]["id"]
        # self.api.notifinations_pm_mark_readed(pm_id)
        # self.api.notifinations_get_pm(pm_id)
        # self.api.notifinations_pm_delete(pm_id)

    def test_media_photos(self):
        response = self.api.photos_upload_url(
            "https://i.ibb.co/Yb1C27t/Zrzut-ekranu-2024-03-7-o-12-45-54.png",
            MediaPhotosType.COMMENTS
        )
        key = response["data"]["key"]

        self.api.photos_delete_photo(key)

    def test_media_embed(self):
        response = self.api.embed_upload_url(
            "https://www.google.com",
        )
        assert response["data"]["key"]

    def test_entry_create(self):
        self.api.links_draft_list_drafts()

        response = self.api.links_draft_create_draft_step_one(
            url="https://www.lipsum.com"
        )
        key = response["data"]["key"]

        self.api.links_draft_get_draft(key)
        self.api.links_draft_delete_draft(key)
        
        response = self.api.links_draft_create_draft_step_one(
            url="https://www.lipsum.com"
        )
        key = response["data"]["key"]
        self.api.links_draft_create_draft_step_two(
            key=key,
            title="Lorem Ipsum",
            description="lorem " * 10,
            tags=["ipsum"],
            adult=False
        )
        response = self.api.profiles_get_profile_links_added(env("WYKOP_USERNAME"))
        link_id = response["data"][0]["id"]
        self.api.links_delete_link(link_id)

    def test_pms(self):
        response = self.api.pms_list_conversations()
        self.api.pms_get_conversation(response["data"][0]["user"]["username"])
        self.api.pms_mark_all_pms_readed()

    def test_profiles(self):
        user = "m__b"

        self.api.profiles_get_my_profile()
        self.api.profiles_get_my_profile_short()
        
        self.api.profiles_get_profile(user)
        self.api.profiles_get_profile_short(user)
        self.api.profiles_get_profile_actions(user)
        self.api.profiles_get_profile_badges(user)

        self.api.profiles_get_profile_entries_added(user)
        self.api.profiles_get_profile_entries_commented(user)
        self.api.profiles_get_profile_entries_voted(user)

        self.api.profiles_get_profile_links_added(user)
        self.api.profiles_get_profile_links_commented(user)
        self.api.profiles_get_profile_links_up(user)
        # self.api.profiles_get_profile_links_down(user)
        self.api.profiles_get_profile_links_related(user)
        self.api.profiles_get_profile_links_published(user)

        self.api.profiles_get_profile_users_followers(user)
        self.api.profiles_get_profile_users_following(user)

        # self.api.profiles_get_profile_observed_tags(user)
