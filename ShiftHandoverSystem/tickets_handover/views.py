from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.views import View

from profiles.util import get_profile
from tickets_handover.forms import TicketCreateForm, TicketDeleteForm, TicketEditForm, TicketStatusForm
from tickets_handover.models import Ticket, TicketStatusHistory


class TicketHandoverListView(ListView):
    model = Ticket
    template_name = "tickets_handover/handover-list.html"
    context_object_name = "tickets"
    ordering = ["-created_at"]

    def get_queryset(self):
        return super().get_queryset().select_related("created_by").prefetch_related("status_entries")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_nav"] = "handover"
        return context


class TicketHandoverCreateView(CreateView):
    model = Ticket
    form_class = TicketCreateForm
    template_name = "tickets_handover/handover-add.html"
    success_url = reverse_lazy("tickets_handover:list")

    def dispatch(self, request, *args, **kwargs):
        if not get_profile():
            return redirect("profiles:home")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.created_by = get_profile()
        response = super().form_valid(form)
        TicketStatusHistory.objects.create(ticket=self.object, status=self.object.status)
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_nav"] = "handover"
        return context


class TicketHandoverEditView(UpdateView):
    model = Ticket
    form_class = TicketEditForm
    template_name = "tickets_handover/handover-edit.html"
    success_url = reverse_lazy("tickets_handover:list")

    def dispatch(self, request, *args, **kwargs):
        if not get_profile():
            return redirect("profiles:home")
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_nav"] = "handover"
        return context

    def form_valid(self, form):
        previous_status = self.get_object().status
        response = super().form_valid(form)
        if self.object.status != previous_status:
            TicketStatusHistory.objects.create(ticket=self.object, status=self.object.status)
        return response


class TicketHandoverDeleteView(DeleteView):
    model = Ticket
    form_class = TicketDeleteForm
    template_name = "tickets_handover/handover-delete.html"
    success_url = reverse_lazy("tickets_handover:list")

    def dispatch(self, request, *args, **kwargs):
        if not get_profile():
            return redirect("profiles:home")
        return super().dispatch(request, *args, **kwargs)

    def get_initial(self) -> dict:
        return self.object.__dict__

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_nav"] = "handover"
        return context


class TicketHandoverStatusView(View):
    def post(self, request, pk: int):
        if not get_profile():
            return redirect("profiles:home")
        ticket = get_object_or_404(Ticket, pk=pk)
        if ticket.status == Ticket.Status.DONE:
            return redirect("tickets_handover:list")
        form = TicketStatusForm(request.POST)
        if form.is_valid():
            TicketStatusHistory.objects.create(
                ticket=ticket,
                status=form.cleaned_data["status_text"].strip(),
            )
        return redirect("tickets_handover:list")
