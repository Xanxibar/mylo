from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import View
# Create your views here.

from analytics.models import ClickEvent, ImpressionEvent
from .forms import SubmitURLForm
from .models import MyURL


class HomeView(View):
    template_name = "shorturl/home.html"

    def get(self, request, *args, **kwargs):
        the_form = SubmitURLForm()
        context = {
            "title": "url-shortener",
            "form": the_form,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = SubmitURLForm(request.POST)
        context = {
            "title": "url-shortener",
            "form": form
        }       
        if form.is_valid():
            new_url = form.cleaned_data.get('url')
            obj, created = KirrURL.objects.get_or_create(url=new_url)
            host = request.get_host()
            uri = request.build_absolute_uri()
            context = {
                "object": obj,
                "created": created,
                "host": host,
                "uri": uri,
                
            }
            if created:
                self.template_name = 'shorturl/success.html'
            else:
                self.template_name = 'shorturl/already-exists.html'
            ImpressionEvent.objects.create_impression(obj)
        return render(request, self.template_name, context)

class URLRedirectView(View):
    def get(self, request, shortcode=None, *args, **kwargs):
        obj = get_object_or_404(KirrURL, shortcode=shortcode)
        ClickEvent.objects.create_event(obj)
        return HttpResponseRedirect(obj.url)