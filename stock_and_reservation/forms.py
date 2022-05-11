from django import forms
from .models import OrganisationProfile, Reservation, ReservedItem


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = OrganisationProfile
        fields = [
            "organisation_name",
            "contact_person",
            "phone",
            "email",
            "password",
            "address",
        ]

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs["class"] = "form-control"


class ReservationForm(forms.ModelForm):

    class Meta:
        model = Reservation
        fields = ['reservation_note']


class ReservedItemsForm(forms.ModelForm):

    class Meta:
        model = ReservedItem
        fields = ['quantity']
    

