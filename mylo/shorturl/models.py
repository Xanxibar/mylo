from django.conf import settings
from django.db import models


from .utils import create_shortcode
from .validators import validate_url

SHORTCODE_MAX = getattr(settings, "SHORTCODE_MAX", 15)

class MyUrlManager(models.Manager):
    def all(self, *args, **kwargs):
        query_set = super(MyUrlManager, self).all(*args, **kwargs)
        return query_set.filter(active=True)

    def refresh_codes(self, items=None):
        qs = KirrURL.objects.filter(pk__gte=1)
        if items is not None and isinstance(items, int):
            qs = qs.order_by('-id')[:items]
        new_codes = 0
        for q in qs:
            q.shortcode = create_shortcode(q)
            print(q.shortcode)
            q.save()
            new_codes += 1
        return "New codes created {i}".format(i=new_codes)

class MyUrl(models.Model):
    url = models.URLField(max_length=255, validators=[validate_url,])
    shortcode = models.CharField(max_length=SHORTCODE_MAX)
    timestamp = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    objects = MyUrlManager()
    
    def __str__(self):
        return str(self.url)

    def get_short_url(self):
        pass

    def save(self, *args, **kwargs):
        if self.shortcode is None or self.shortcode == "":
            self.shortcode = create_shortcode(self)
        super(MyUrl, self).save(*args, **kwargs)

