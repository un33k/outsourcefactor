from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class BookmarkManager(models.Manager):
        
    def get_query_set(self):
        return super(BookmarkManager, self).get_query_set().order_by('-updated_at')

    def get_all_bookmarks_for_this_model_for_any_user(self, model):
        """ Returns all bookmarks of a given model for any user """
        content_type = ContentType.objects.get_for_model(model)
        queryset = self.get_query_set().filter(content_type=content_type)
        return queryset
    
    def get_all_bookmarks_for_this_model_for_this_user(self, user, model):
        """ Returns all bookmarks of a model type for a given user """
        queryset = self.get_all_bookmarks_for_this_model_for_any_user(model).filter(user=user)
        return queryset
    
    def get_all_bookmarks_for_this_object_type_for_any_user(self, obj):
        """ Returns all bookmarks of a given object by its type for any user"""
        content_type = ContentType.objects.get_for_model(type(obj))
        queryset = self.get_query_set().filter(content_type=content_type)
        return queryset

    def get_all_bookmarks_for_this_object_type_for_this_user(self, obj):
        """ Returns all bookmarks of a given object by its type for a given user """
        queryset = self.get_all_bookmarks_for_this_object_type_for_any_user(model).filter(user=user)
        return queryset

    def get_all_bookmarks_for_this_exact_object_for_any_user(self, obj):
        """ Returns all bookmarks of an specific object for any user """
        content_type = ContentType.objects.get_for_model(type(obj))
        queryset = self.get_query_set().filter(content_type=content_type, object_id=obj.pk)
        return queryset

    def get_the_bookmark_for_this_object_for_this_user(self, user, obj):
        """ Returns a single bookmark of a given object for a given user """
        content_type = ContentType.objects.get_for_model(type(obj))
        queryset = self.get_query_set().get(content_type=content_type, object_id=obj.pk, user=user)
        return queryset

    def get_all_bookmarks_for_this_user(self, user):
        """ Returns all bookmarks of all models & types for this user """
        return self.get_query_set().filter(user=user)
 
    def create_bookmark(self, user, obj):
        """ Returns a bookmak, but fitching it for creating it """
        try:
            bm = self.get_the_bookmark_for_this_object_for_this_user(user, obj)
        except:
            content_type = ContentType.objects.get_for_model(type(obj))
            bm = Bookmark(user=user, content_type=content_type, object_id=obj.pk, content_object=obj)
            bm.save()
            try:
                bm.content_object.set_bookmark(increment=True)
            except:
                pass
        return bm

    def delete_bookmark(self, user, obj):
        try:
            bm = self.get_the_bookmark_for_this_object_for_this_user(user, obj)
        except:
            pass
        else:
            try:
                bm.content_object.set_bookmark(increment=False)
            except:
                pass
            bm.delete()
        return
               
class Bookmark(models.Model):
    """ Bookmark objects for this user """

    user = models.ForeignKey(User, related_name="%(class)s", null=False)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = BookmarkManager()

    class Meta:
        verbose_name = _('bookmark')
        verbose_name_plural = _('bookmarks')
        unique_together = (('user', 'content_type', 'object_id'),)

    def __unicode__(self):
        return u'%s-[%s]' % (self.user, self.content_object)

