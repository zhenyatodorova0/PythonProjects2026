from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import DetailView, DeleteView

from important_updates.models import Update
from profiles.forms import ProfileForm
from profiles.models import Profile
from profiles.util import get_profile


# Create your views here.
class HomeView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        profile = get_profile()

        context = {
            'form': ProfileForm(),
        }

        if not profile:
            return render(request, 'profiles/home-no-profile.html', context)

        all_updates = Update.objects.all()
        context['important_updates'] = all_updates

        return render(request, 'profiles/home-with-profile.html', context)


    def post(self, request: HttpRequest) -> HttpResponse:
            form = ProfileForm(request.POST)

            if form.is_valid():
                form.save()
                return redirect('profiles:home')

            return render(request, 'profiles/home-no-profile.html', {'form': form})

class ProfileDetailView(DetailView):
    template_name = 'profiles/profile-details.html'

    def get_object(self, queryset=None) -> Profile:
        return get_profile()

    def get_context_data(self, **kwargs) -> dict:
        kwargs.update({
            "important_updates_count": self.object.important_updates.count(),
        })
        return super().get_context_data(**kwargs)

class ProfileDeleteView(DeleteView):
    template_name = 'profiles/profile-delete.html'

    def post(self, request):
        get_profile().delete()
        return redirect('profiles:home')