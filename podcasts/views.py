from django.shortcuts import render
from django.views.generic import ListView

from .models import Episode


class HomePageView(ListView):
    template_name = "homepage.html"
    model = Episode
    paginate_by = 10
    context_object_name = "podcasts"

