from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views import View
from django.views.generic import DetailView

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
            request.session.pop("profile_last_login", None)
            return render(request, 'profiles/home-no-profile.html', context)

        if not request.session.get("profile_last_login"):
            request.session["profile_last_login"] = timezone.localtime().strftime("%d %b %Y, %H:%M:%S")

        seven_days_ago = timezone.now() - timezone.timedelta(days=7)
        recent_important_updates = list(Update.objects.filter(
            created_at__gte=seven_days_ago
        ).order_by("-created_at")[:5])
        context.update({
            "profile": profile,
            "recent_important_updates": recent_important_updates,
            "recent_updates_count": len(recent_important_updates),
            "important_updates_count": profile.updates_made_by.count(),
            "liked_updates_count": profile.liked_updates.count(),
            "last_login": request.session.get("profile_last_login"),
        })

        return render(request, 'profiles/home-with-profile.html', context)


    def post(self, request: HttpRequest) -> HttpResponse:
            form = ProfileForm(request.POST)

            if form.is_valid():
                form.save()
                request.session["profile_last_login"] = timezone.localtime().strftime("%d %b %Y, %H:%M:%S")
                return redirect('profiles:home')

            return render(request, 'profiles/home-no-profile.html', {'form': form})

class ProfileDetailView(DetailView):
    template_name = 'profiles/profile-details.html'

    def get(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if not get_profile():
            return render(
                request,
                self.template_name,
                {"no_profile_message": "You are not logged in your profile yet!"},
            )
        return super().get(request, *args, **kwargs)

    def get_object(self, queryset=None) -> Profile:
        return get_profile()

    def get_context_data(self, **kwargs) -> dict:
        kwargs.update({
            "important_updates_count": self.object.updates_made_by.count(),
        })
        return super().get_context_data(**kwargs)

class ProfileDeleteView(View):
    template_name = 'profiles/profile-delete.html'

    def get(self, request: HttpRequest) -> HttpResponse:
        return render(request, self.template_name)

    def post(self, request: HttpRequest) -> HttpResponse:
        profile = get_profile()
        if profile:
            profile.delete()
        return redirect('profiles:home')
