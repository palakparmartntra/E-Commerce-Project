from django.shortcuts import render, get_object_or_404, redirect

from django.views.generic.edit import UpdateView, CreateView, DeleteView

from .models import User, Address
from .forms import AddressForm, UserUpdateForm
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from .models import User
from django.http import Http404


class HomePageView(TemplateView):
    """ view for rendering index page"""

    template_name = 'index.html'


class AddAddress(CreateView):
    model = Address
    fields = ['receiver_name', 'house_no', 'phone_no', 'street',
              'landmark', 'city', 'state', 'zipcode']
    template_name = 'profile/add_address.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('view_profile', kwargs={'username': self.request.user.username})


def profile(request, username, pk=None):
    """" To show and update user details of current login user """

    if request.user.username == username:

        user = get_object_or_404(User, username=username)
        address = Address.objects.filter(user=request.user.id)
        if pk is not None:
            address_to_update = get_object_or_404(Address, user=request.user.id, pk=pk)
        else:
            address_to_update = address[0]

        user_form = UserUpdateForm()
        address_form = AddressForm()
        """ check url whether it is 'update-profile' or 'update-address' """
        current_url = request.path
        current_url = current_url.split("/")[2]

        """ This if condition saves user updated data if form is submitted else it shows the user profile data. 
        Internal if condition is executed when update-profile url is hit """

        if request.method == "POST":
            if current_url == "update-profile":
                updated_first_name = request.POST.get('first_name')
                updated_last_name = request.POST.get('last_name')
                updated_phone_no = request.POST.get('phone_no')
                updated_email = request.POST.get('email')
                if user_form.is_valid:
                    user.first_name = updated_first_name
                    user.last_name = updated_last_name
                    user.phone_no = updated_phone_no
                    user.email = updated_email
                    user.save()

                """ To show updated user details in form after saving data """
            user_form = UserUpdateForm(initial={
                'first_name': user.first_name,
                'last_name': user.last_name,
                'phone_no': user.phone_no,
                'email': user.email,

            })

            if current_url == "update-address" and pk is not None:
                print("=================== Update Address ====================== ")
                updated_receiver_name = request.POST.get('receiver_name')
                updated_house_no = request.POST.get('house_no')
                updated_phone_no = request.POST.get('phone_no')
                updated_street = request.POST.get('street')
                updated_landmark = request.POST.get('landmark')
                updated_city = request.POST.get('city')
                updated_state = request.POST.get('state')
                updated_zipcode = request.POST.get('zipcode')
                if address_form.is_valid:
                    address_to_update.receiver_name = updated_receiver_name
                    address_to_update.house_no = updated_house_no
                    address_to_update.phone_no = updated_phone_no
                    address_to_update.street = updated_street
                    address_to_update.landmark = updated_landmark
                    address_to_update.city = updated_city
                    address_to_update.state = updated_state
                    address_to_update.zipcode = updated_zipcode
                    address_to_update.save()

                """ To show updated user details in form after saving data """

            def get_success_url(self):
                return reverse_lazy('view_profile', kwargs={'username': self.request.user.username})
        else:
            user_form = UserUpdateForm(initial={
                'first_name': user.first_name,
                'last_name': user.last_name,
                'phone_no': user.phone_no,
                'email': user.email,

            })

            def get_success_url(self):
                return reverse_lazy('view_profile', kwargs={'username': self.request.user.username})
    else:
        raise Http404('not found')
    return render(request, 'profile/view_profile.html',
                  {'user': user, 'user_form': user_form,
                   # 'address_form': address_form,
                   'addresses': address})
