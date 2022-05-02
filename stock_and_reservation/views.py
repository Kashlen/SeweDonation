from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render

from .forms import RegistrationForm
from .models import ItemVariation, OrganisationProfile


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
    if request.method == "POST":
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

    # TODO: to be finished later in stock view:
    # def get_available_quantity(self):
    #   _ = self.on_stock - self.reserved_quantity
    #  if _ <= 0:
    #        available_quantity = 0
    #   else:
    #      available_quantity = _
    # return available_quantity

    # available_quantity = self.get_available_quantity()
