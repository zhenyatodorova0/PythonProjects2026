from profiles.util import get_profile


class AttachOwnerMixin:
    def get_initial(self) -> dict: #we want you to put an owner in the form
        initial = super().get_initial()
        initial["owner"] = get_profile()
        return initial

    def form_valid(self, form):# as a protection
        form.instance.owner = get_profile()
        return super().form_valid(form)