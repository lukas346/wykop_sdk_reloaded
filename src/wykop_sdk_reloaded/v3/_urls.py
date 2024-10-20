API_URL = "https://wykop.pl/api/v3"

AUTH_URL = f"{API_URL}/auth"
CONNECT_URL = f"{API_URL}/connect"
REFRESH_TOKEN_URL = f"{API_URL}/refresh-token"

# links
LINKS_URL = f"{API_URL}/links"
LINKS_LINK_URL = lambda id: f"{API_URL}/links/{id}"
LINKS_VOTES_URL = lambda id: f"{API_URL}/links/{id}/votes"
LINKS_VOTE_UP_URL = lambda id: f"{API_URL}/links/{id}/votes/up"
LINKS_VOTE_DOWN_URL = lambda id, reason: f"{API_URL}/links/{id}/votes/down/{reason}"

# link comments
LINK_COMMENTS_URL = lambda id: f"{API_URL}/links/{id}/comments"
LINK_COMMENTS_COMMENT_URL = lambda id, comment_id: f"{API_URL}/links/{id}/comments/{comment_id}"
LINK_COMMENTS_COMMENT_VOTE_URL = lambda id, comment_id, type: f"{API_URL}/links/{id}/comments/{comment_id}/votes/{type}"
LINK_COMMENTS_COMMENT_VOTE_REVOKE_URL = lambda id, comment_id: f"{API_URL}/links/{id}/comments/{comment_id}/votes"

# link drafs
LINK_DRAFTS_URL = f"{API_URL}/links/draft"
LINK_DRAFTS_DRAFT_URL = lambda key: f"{API_URL}/links/draft/{key}"

# tags
TAGS_POPULAR_URL = f"{API_URL}/tags/popular"
TAGS_POPULAR_USER_URL = f"{API_URL}/tags/popular-user-tags"
TAGS_RELATED_TAG_URL = lambda tag: f"{API_URL}/tags/{tag}/related"
TAGS_DETAIL_TAG_URL = lambda tag: f"{API_URL}/tags/{tag}"
TAGS_STREAM_TAG_URL = lambda tag: f"{API_URL}/tags/{tag}/stream"
TAGS_TAG_OWNERS_URL = lambda tag: f"{API_URL}/tags/{tag}/users"

# articles
ARTICLES_URL = f"{API_URL}/articles"
ARTICLES_ARTICLE_URL= lambda id: f"{API_URL}/articles/{id}"

# entries
ENTRIES_URL = f"{API_URL}/entries"
ENTRIES_SEARCH_URL = f"{API_URL}/search/entries"
ENTRIES_ENTRY_URL = lambda id: f"{API_URL}/entries/{id}"
ENTRIES_ENTRY_VOTES_URL = lambda id: f"{API_URL}/entries/{id}/votes"

# entry comments
ENTRY_COMMENTS_URL = lambda id: f"{API_URL}/entries/{id}/comments"
ENTRY_COMMENTS_COMMENT_URL = lambda entry_id, comment_id: f"{API_URL}/entries/{entry_id}/comments/{comment_id}"
ENTRY_COMMENTS_VOTES_URL = lambda entry_id, comment_id: f"{API_URL}/entries/{entry_id}/comments/{comment_id}/votes"

# notifications
NOTIFICATIONS_STATUS_URL = f"{API_URL}/notifications/status"

NOTIFICATIONS_ENTRIES_URL = f"{API_URL}/notifications/entries"
NOTIFICATIONS_ENTRIES_ALL_URL = f"{API_URL}/notifications/entries/all"
NOTIFICATIONS_ENTRY_URL = lambda id: f"{API_URL}/notifications/entries/{id}"

NOTIFICATIONS_PMS_URL = f"{API_URL}/notifications/pm"
NOTIFICATIONS_PMS_ALL_URL = f"{API_URL}/notifications/pm/all"
NOTIFICATIONS_PM_URL = lambda id: f"{API_URL}/notifications/pm/{id}"

# media - photos
MEDIA_PHOTOS_UPLOAD_URL = f"{API_URL}/media/photos"
MEDIA_PHOTOS_UPLOAD_FILE = f"{API_URL}/media/photos/upload"
MEDIA_PHOTOS_GET_PHOTO_URL = lambda key: f"{API_URL}/media/photos/{key}"

# media - embed
MEDIA_EMBED_UPLOAD_URL = f"{API_URL}/media/embed"

# profile
PROFILES_OWN_PROFILE_URL = f"{API_URL}/profile"
PROFILES_OWN_SHORT_PROFILE_URL = f"{API_URL}/profile/short"
PROFILES_PROFILE_URL = lambda username: f"{API_URL}/profile/users/{username}"
PROFILES_PROFILE_SHORT_URL = lambda username: f"{API_URL}/profile/users/{username}/short"
PROFILES_PROFILE_ACTIONS_URL = lambda username: f"{API_URL}/profile/users/{username}/actions"
PROFILES_PROFILE_ENTRIES_ADDED_URL = lambda username: f"{API_URL}/profile/users/{username}/entries/added"
PROFILES_PROFILE_ENTRIES_VOTED_URL = lambda username: f"{API_URL}/profile/users/{username}/entries/voted"
PROFILES_PROFILE_ENTRIES_COMMENTED_URL = lambda username: f"{API_URL}/profile/users/{username}/entries/commented"
PROFILES_PROFILE_LINKS_ADDED_URL = lambda username: f"{API_URL}/profile/users/{username}/links/added"
PROFILES_PROFILE_LINKS_PUBLISHED_URL = lambda username: f"{API_URL}/profile/users/{username}/links/published"
PROFILES_PROFILE_LINKS_UP_URL = lambda username: f"{API_URL}/profile/users/{username}/links/up"
PROFILES_PROFILE_LINKS_DOWN_URL = lambda username: f"{API_URL}/profile/users/{username}/links/down"
PROFILES_PROFILE_LINKS_COMMENTED_URL = lambda username: f"{API_URL}/profile/users/{username}/links/commented"
PROFILES_PROFILE_LINKS_RELATED_URL = lambda username: f"{API_URL}/profile/users/{username}/links/related"
PROFILES_PROFILE_BADGES_URL = lambda username: f"{API_URL}/profile/users/{username}/badges"
PROFILES_PROFILE_TAGS_URL = lambda username: f"{API_URL}/profile/users/{username}/tags"
PROFILES_PROFILE_OBSERVED_TAGS_URL = lambda username: f"{API_URL}/profile/users/{username}/observed/tags"
PROFILES_PROFILE_OBSERVED_FOLLOWING_URL = lambda username: f"{API_URL}/profile/users/{username}/observed/users/following"
PROFILES_PROFILE_OBSERVED_FOLLOWERS_URL = lambda username: f"{API_URL}/profile/users/{username}/observed/users/followers"

# pms
PMS_READ_ALL_URL = f"{API_URL}/pm/read-all"
PMS_CONVERSATIONS_URL = f"{API_URL}/pm/conversations"
PMS_CONVERSATION_URL = lambda username: f"{API_URL}/pm/conversations/{username}"
