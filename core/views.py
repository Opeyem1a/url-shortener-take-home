from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from core.models import Url
from core.forms import UrlForm


class HomeView(View):
    template_name = "home.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        form = UrlForm(request.POST)
        if not form.is_valid():
            return render(request, self.template_name, {"form": form})

        url = form.cleaned_data.get("url")
        custom_hash = form.cleaned_data.get("custom_hash") or None
        obj = Url.objects.create(url=url, hashed_url=custom_hash)

        return render(
            request, self.template_name, {"short_url": obj.get_full_short_url()}
        )


class HashRedirectView(View):

    def get(self, request, hash_url: str, *args, **kwargs):
        url = get_object_or_404(Url.objects, hashed_url=hash_url)
        # temporary redirect is best practice to avoid harming SEO of links
        return redirect(url.url)
