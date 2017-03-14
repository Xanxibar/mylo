from django.db import models

from shorturl.models import MyURL


class ClickEventManager(models.Manager):

    def create_event(self, instance):
        if isinstance(instance, MyURL):
            obj, created = self.get_or_create(myurl=instance)
            obj.count += 1
            obj.save()
            return obj.count
        return None

class ClickEvent(models.Model):
    myurl = models.OneToOneField(MyURL, related_name="clicks")
    count = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = ClickEventManager()

    def __str__(self):
        return "{i}".format(i=self.count)


class ImpressionEventManager(models.Manager):
    
    def create_impression(self, instance):
        if isinstance(instance, MyURL):
            obj, created = self.get_or_create(myurl=instance)
            obj.count += 1
            obj.save()
            return obj.count
        return None



class ImpressionEvent(models.Model):
    myurl = models.OneToOneField(MyURL , related_name="impressions")
    count = models.IntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = ImpressionEventManager()

    def __str__(self):
        return "{i}".format(i=self.count)