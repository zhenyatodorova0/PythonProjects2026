from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView, DeleteView, ListView

from important_updates.forms import UpdateCreateForm, UpdateEditForm
from important_updates.mixins import AttachOwnerMixin
from important_updates.models import Update
from profiles.util import get_profile


# Create your views here.
class UpdateCreateView(CreateView, AttachOwnerMixin):
    model = Update
    form_class = UpdateCreateForm
    success_url = reverse_lazy('profiles:home')
    template_name = 'important_updates/updates-add.html'

class UpdateListView(ListView):
    model = Update
    template_name = 'important_updates/updates-list.html'
    context_object_name = 'important_updates'
    ordering = ['-created_at']


class UpdateDetailView(DetailView):
    model = Update
    template_name = 'important_updates/updates-details.html'
    context_object_name = 'update'


class UpdateEditView(UpdateView, AttachOwnerMixin):
    model = Update
    form_class = UpdateEditForm
    template_name = 'important_updates/updates-edit.html'
    success_url = reverse_lazy('profiles:home')


class UpdateDeleteView(DeleteView):
    model = Update
    template_name = 'important_updates/updates-delete.html'
    success_url = reverse_lazy('profiles:home')
