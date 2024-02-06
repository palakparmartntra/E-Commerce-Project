
from django.views.generic.edit import CreateView
from .models import Address
from django.urls import reverse_lazy
from django.views.generic import TemplateView

# Create your views here.


class Index(TemplateView):
    """ view for the render index page """
    template_name = 'index.html'


class HomePageView(TemplateView):
    """ view for rendering index page """

    template_name = 'index.html'


class AddAddress(CreateView):
    """ view for add address """

    model = Address
    fields = ['receiver_name', 'house_no', 'phone_no', 'street',
              'landmark', 'city', 'state', 'zipcode']
    template_name = 'profile/add_address.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('view_profile', kwargs={'pk': self.request.user.pk})
