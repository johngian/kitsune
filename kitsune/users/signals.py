from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from kitsune.users.models import Profile


@receiver(post_save, sender=Profile)
def search_index_post_save(sender, instance, **kwargs):
    """Index profile instances on save"""

    from kitsune.search.v2.helpers import index_object
    index_object.delay('ProfileDocument', instance.id)


@receiver(post_delete, sender=Profile)
def search_unindex_post_delete(sender, instance, **kwargs):
    """Unindex deleted instance on delete"""

    from kitsune.search.v2.helpers import unindex_object
    unindex_object.delay('ProfileDocument', instance.id)
