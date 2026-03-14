from datetime import datetime
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import TemplateView

from feedback.models import Feedback
from important_updates.models import Update
from profiles.models import Profile
from tickets_handover.models import Ticket

def current_time(request):
    now = datetime.now()
    context = {
        'current_time': now.strftime("%Y-%m-%d %H:%M:%S")
    }
    return render(request, 'common/current_time.html', context)


class GlobalSearchView(TemplateView):
    template_name = "common/search-results.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get("q", "").strip()

        feedback_results = Feedback.objects.none()
        updates_results = Update.objects.none()
        profiles_results = Profile.objects.none()
        tickets_results = Ticket.objects.none()

        if query:
            feedback_results = Feedback.objects.select_related("owner").filter(
                Q(title__icontains=query)
                | Q(description__icontains=query)
                | Q(owner__username__icontains=query)
            ).order_by("-created_at")

            updates_results = Update.objects.select_related("made_by").filter(
                Q(title__icontains=query)
                | Q(description__icontains=query)
                | Q(category__icontains=query)
                | Q(made_by__username__icontains=query)
            ).order_by("-created_at")

            profiles_results = Profile.objects.filter(
                Q(username__icontains=query) | Q(email__icontains=query)
            ).order_by("username")

            tickets_results = Ticket.objects.select_related("created_by").filter(
                Q(type__icontains=query)
                | Q(ticket_id__icontains=query)
                | Q(title__icontains=query)
                | Q(description__icontains=query)
                | Q(status__icontains=query)
                | Q(created_by__username__icontains=query)
                | Q(status_entries__status__icontains=query)
            ).distinct().order_by("-created_at")

        context["query"] = query
        context["feedback_results"] = feedback_results
        context["updates_results"] = updates_results
        context["profiles_results"] = profiles_results
        context["tickets_results"] = tickets_results
        context["total_results"] = (
            feedback_results.count()
            + updates_results.count()
            + profiles_results.count()
            + tickets_results.count()
        ) if query else 0
        return context
