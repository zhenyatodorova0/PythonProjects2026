from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
    ListView,
)

from important_updates.forms import UpdateCreateForm, UpdateEditForm, UpdateDeleteForm
from important_updates.mixins import AttachOwnerMixin
from important_updates.models import Update
from profiles.util import get_profile


# Create your views here.
class UpdateCreateView(AttachOwnerMixin, CreateView):
    model = Update
    form_class = UpdateCreateForm
    success_url = reverse_lazy("profiles:home")
    template_name = "important_updates/updates-add.html"


class UpdateListView(ListView):
    model = Update
    template_name = "important_updates/updates-list.html"
    context_object_name = "important_updates"
    ordering = ["-created_at"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = get_profile()
        context["profile"] = profile
        context["liked_update_ids"] = (
            set(profile.liked_updates.values_list("id", flat=True))
            if profile
            else set()
        )
        return context


class UpdateDetailView(DetailView):
    model = Update
    template_name = "important_updates/updates-details.html"
    context_object_name = "update"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = get_profile()
        context["profile"] = profile
        context["is_liked"] = bool(
            profile and self.object.liked_by.filter(pk=profile.pk).exists()
        )
        return context


class UpdateEditView(AttachOwnerMixin, UpdateView):
    model = Update
    form_class = UpdateEditForm
    template_name = "important_updates/updates-edit.html"
    success_url = reverse_lazy("profiles:home")


class UpdateDeleteView(DeleteView):
    model = Update
    form_class = UpdateDeleteForm
    template_name = "important_updates/updates-delete.html"
    success_url = reverse_lazy("profiles:home")

    def get_initial(self) -> dict:
        return self.object.__dict__


class UpdateLikeToggleView(View):
    def post(self, request: HttpRequest, pk: int) -> HttpResponse:
        profile = get_profile()
        if not profile:
            return redirect("profiles:home")

        update = get_object_or_404(Update, pk=pk)
        if update.liked_by.filter(pk=profile.pk).exists():
            update.liked_by.remove(profile)
        else:
            update.liked_by.add(profile)

        next_url = request.POST.get("next")
        if next_url:
            return redirect(next_url)
        return redirect("important_updates:update-details", pk=pk)
