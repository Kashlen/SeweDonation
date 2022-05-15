from django import forms
from django.forms import modelformset_factory
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


class ReservedItemsForm(forms.ModelForm):  # TODO: To be deleted if ReservedItemsFormSet works - no need to have it (I think).
    item = forms.CharField(widget=forms.HiddenInput())

    class Meta:
        model = ReservedItem
        fields = ['item', 'quantity']
    
ReservedItemsFormSet = modelformset_factory(ReservedItem, fields=["item", "quantity"])  # TODO: If doesn't work, write back `ReservedItemsForm`.
    