from django.views.generic.detail import DetailView
from .models import User


class ViewProfile(DetailView):
    """ To view user details """
    model = User
    template_name = 'profile/view_profile.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['addresses'] = user.address.all()
        context['other_address_displayed'] = False
        return context
