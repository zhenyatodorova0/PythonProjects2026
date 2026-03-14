from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from feedback.forms import FeedbackCreateForm
from feedback.models import Feedback
from profiles.util import get_profile


class FeedbackListView(ListView):
    model = Feedback
    template_name = "feedback/feedback-list.html"
    context_object_name = "feedback_items"
    ordering = ["-created_at"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_nav"] = "feedback"
        return context


class FeedbackCreateView(CreateView):
    model = Feedback
    form_class = FeedbackCreateForm
    template_name = "feedback/feedback-add.html"
    success_url = reverse_lazy("feedback:list")

    def dispatch(self, request, *args, **kwargs):
        if not get_profile():
            return redirect("profiles:home")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.owner = get_profile()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["active_nav"] = "feedback"
        return context
