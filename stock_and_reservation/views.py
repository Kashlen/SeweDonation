from base64 import urlsafe_b64encode
from dataclasses import field  # Used for verification e-mail - currently disabled, but still in code

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import (
    default_token_generator,
)  # Used for verification e-mail - currently disabled, but still in code
from django.contrib.sites.shortcuts import (
    get_current_site,
)  # Used for verification e-mail - currently disabled, but still in code
from django.core.mail import EmailMessage  # Used for verification e-mail - currently disabled, but still in code
from django.shortcuts import redirect, render
from django.template.loader import (
    render_to_string,
)  # Used for verification e-mail - currently disabled, but still in code
from django.utils.encoding import force_bytes  # Used for verification e-mail - currently disabled, but still in code 

from .forms import RegistrationForm, ReservationForm, ReservedItemsFormSet
from .models import ItemVariation, OrganisationProfile, ReservedItem


def overview(request):
    if request.method == "POST":
        email = request.POST["email"]  # Field name is in the brackets.
        password = request.POST["password"]
        user = authenticate(email=email, password=password)  # Returns user object.

        if user is not None:
            login(request, user)
            return redirect("overview")  # TODO: Change to stock.html once created.
        else:
            return redirect("overview")

    items_list = ItemVariation.objects.all().order_by("saldo")
    three_lowest = items_list[0:3]
    return render(request, "stock_and_reservation/overview.html", {"three_lowest": three_lowest})


def registration(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)  #  It will contain all field values.
        if form.is_valid():  #  It means all required fields are filled in.
            organisation_name = form.cleaned_data["organisation_name"]
            contact_person = form.cleaned_data["contact_person"]
            phone = form.cleaned_data["phone"]
            email = form.cleaned_data["email"]
            username = (email.split("@")[1]).split(".")[0]
            password = form.cleaned_data["password"]
            address = form.cleaned_data["address"]

            user = OrganisationProfile.objects.create_user(
                organisation_name=organisation_name,
                email=email,
                username=username,
                password=password,
            )
            user.phone = phone
            user.contact_person = contact_person
            user.address = address
            user.save()

            # User activation - REQUIRES EMAIL PASSWORD IN SETTINGS (67, 17) - How to protect the password? TODO: Find out if loading from file is OK.
            # current_site = get_current_site(request)
            # mail_subject = "Prosím, aktivujte si svůj uživatelský účet na Ušij a daruj."
            # message = render_to_string('sewndonation/user_verification_email.html', {
            #    'user': user,
            #    'domain': current_site,
            #    'uid': urlsafe_b64encode(force_bytes(user.pk)),
            #    'token': default_token_generator.make_token(user),
            # })
            # to_email = email
            # send_email = EmailMessage(mail_subject, message, to=[to_email])
            # send_email.send()
            return render(request, "stock_and_reservation/registration_succeed.html")
    else:
        form = RegistrationForm()
        return render(request, "stock_and_reservation/registration.html", {"form": form})


def registration_succeed(request):
    return render(request, "stock_and_reservation/registration_succeed.html")


def log_out(
    request,
):  #  TODO: To use decorator @login_required to validate login before logout or not? / I have an if statement there (in base.html) now. (66, 15)
    logout(request)
    return redirect("overview")


def stock(request):
    items_list = ItemVariation.objects.all().order_by('item', 'size')
    if request.method == 'POST':
        form = ReservationForm(request.POST)
        formset = ReservedItemsFormSet(request.POST)
        if form.is_valid() and formset.is_valid:  # TODO: Set validation somehow - it is possible to create reservation even without corresponding reserved items. This shouldn't happen.
            reservation = form.save(commit=False)
            reservation.reservation_note = form.cleaned_data['reservation_note']
            reservation.organisation_name = request.user
            reservation.save()
            reserved_items = formset.save(commit=False)
            for reserved_item in reserved_items:
                # if one_item.quantity > 0: TODO: Move the logic to the model. - Done but cannot be checked till it won't start work. :)
                reserved_item.item = formset.cleaned_data['item'] # TODO: How it is possible to use form field name???
                reserved_item.reservation_number = reservation.reservation_number
                reserved_item.quantity = formset.cleaned_data['quantity']
                reserved_item.save()
            return render(request, "stock_and_reservation/stock.html", {"items_list": items_list, 'form': form, 'formset': formset}) # TODO: May redirect to list of reservations or reservation detail. / Once created these pages.
    else:
        form = ReservationForm()
        formset = ReservedItemsFormSet()
    return render(request, "stock_and_reservation/stock.html", {"items_list": items_list, 'form': form, 'formset': formset})


