from itertools import permutations

from django.conf import settings

from elasticsearch_dsl import document, field, Document, Index

from kitsune.search.v2 import analyzers


default_index = Index(settings.SEARCH_V2_INDEXES['default'])


@default_index.document
class ProfileDocument(Document):
    """ES document abstraction for Profile"""

    url = field.Text(analyzer=analyzers.url)
    username = field.Text(analyzer=analyzers.lowercase)
    display_name = field.Text(analyzer=analyzers.lowercase)
    twitter_usernames = field.Text(analyzer=analyzers.lowercase, multi=True)
    avatar = field.Text(analyzers=analyzers.url)
    last_contribution_date = field.Date()
    suggest = field.Completion(analyzer='whitespace')
    indexed_on = field.Date()

    class Meta:
        model = document.MetaField('Profile')

    def clean(self):
        """Extract suggestions from document"""
        suggestion_input = [
            self.display_name,
            self.username
        ] + self.twitter_usernames

        self.suggest = {
            'input': [' '.join(p) for p in permutations(suggestion_input)]
        }

    @classmethod
    def get_related_model(cls):
        """Get related Django ORM model"""
        from kitsune.users.models import User
        return User

    @classmethod
    def get_extracted_document(cls, obj_id):
        """Prepare object for document extraction"""
        from kitsune.users.templatetags.jinja_helpers import profile_avatar

        model = cls.get_model()
        obj = model.objects.get(pk=obj_id)

        doc = {
            'url': obj.get_absolute_url(),
            'username': obj.user.username,
            'display_name': obj.display_name,
            'twitter_usernames': obj.twitter_usernames,
            'avatar': profile_avatar(obj.user, size=120),
            'last_contribution_date': obj.last_contribution_date,
        }

        return doc
