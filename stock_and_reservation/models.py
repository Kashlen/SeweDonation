from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from django.utils import timezone


# ITEMS


class Item(models.Model):
    item_name = models.CharField(max_length=100, verbose_name="název")
    description = models.TextField(max_length=500, verbose_name="popis", blank=True)
    image = models.ImageField(upload_to="", blank=True)  #  TODO: ? To create a preview in admin? (115)

    class Meta:
        verbose_name = "Položka"
        verbose_name_plural = "Položky"

    def __str__(self):
        return self.item_name


size_choice = (("32", "32"), ("44", "44"), ("52", "52"))

fabric_design_choice = (
    ("uni", "uni"),
    ("dívčí", "dívčí"),
    ("chlapecký", "chlapecký"),
)


class ItemVariation(models.Model):
    item = models.ForeignKey(Item, verbose_name="položka", on_delete=models.CASCADE)
    size = models.CharField(choices=size_choice, max_length=50, verbose_name="velikost", blank=False)
    fabric_design = models.CharField(choices=fabric_design_choice, max_length=50, verbose_name="vzor", blank=False)
    description = models.TextField(max_length=500, verbose_name="popis", blank=True)
    on_stock = models.PositiveIntegerField(verbose_name="na skladě")
    reserved_quantity = models.IntegerField(
        verbose_name="rezervované množství"
    )  # TODO: Make coonection to reservations so quantity is automaticaly reloaded.
    saldo = models.IntegerField(blank=True, editable=False)

    class Meta:
        verbose_name = "Varianta"
        verbose_name_plural = "Varianty"

    def __str__(self):
        return self.item.item_name + " (vel. " + self.size + ", vzor " + self.fabric_design + ")"

    def save(self, **kwargs):
        self.saldo = self.on_stock - self.reserved_quantity
        return super().save(**kwargs)

    @property
    def image(self):
        return self.item.image


# ACCOUNTS


class MyAccountManager(BaseUserManager):
    def create_user(self, organisation_name, username, email, password=None):
        if not email:
            raise ValueError("Vyplňte e-mailovou adresu.")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            organisation_name=organisation_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, organisation_name, username, email, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            organisation_name=organisation_name,
        )

        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class OrganisationProfile(AbstractBaseUser):
    email = models.EmailField(verbose_name="E-mailová adresa", max_length=100, unique=True)
    username = models.CharField(verbose_name="Uživatelské jméno", max_length=50, unique=True)
    organisation_name = models.CharField(verbose_name="Název organizace", max_length=100, unique=True)
    contact_person = models.CharField(verbose_name="Kontaktní osoba", max_length=50, blank=True)
    address = models.CharField(verbose_name="Adresa", max_length=200, blank=True)
    phone = models.CharField(verbose_name="Telefon", max_length=30, blank=True)
    notes = models.TextField(verbose_name="Poznámky", blank=True)

    #  TODO: ? I will resolve later: reservations        = models.ForeignKey(Reservation, verbose_name="Rezervace", on_delete=models.CASCADE)

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["organisation_name", "username"]

    objects = MyAccountManager()

    class Meta:
        verbose_name = "Organizace"
        verbose_name_plural = "Organizace"

    def __str__(self):
        return self.organisation_name

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True


# RESERVATIONS

status_choice = (
    ("new", "nová"),
    ("in progress", "rozpracovaná"),
    ("completed", "připravená k odeslání"),
    ("closed", "uzavřená"),
)


class Reservation(models.Model):
    reservation_number = models.IntegerField(
        verbose_name="Rezervační číslo",
        primary_key=True,
        auto_created=True,
        editable=False,
        unique=True,
    )
    status = models.CharField(choices=status_choice, max_length=50, default="new")
    organisation_name = models.ForeignKey(OrganisationProfile, on_delete=models.CASCADE, verbose_name="Organizace")
    created_at = models.DateTimeField(verbose_name="Vytvořena dne", auto_created=True, default=timezone.now)
    updated_at = models.DateTimeField(verbose_name="Upravena dne", default=timezone.now, blank=True)
    reservation_note = models.TextField(max_length=500, verbose_name="Poznámka k rezervaci", blank=True)

    class Meta:
        verbose_name = "Rezervace"
        verbose_name_plural = "Rezervace"

    def __unicode__(self):
        return self.reservation_number


class ReservedItem(models.Model):
    item = models.ForeignKey(ItemVariation, on_delete=models.CASCADE, verbose_name='Rezervovaná položka')
    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, verbose_name='Rezervace')
    quantity = models.IntegerField(verbose_name="Počet kusů")

    def __str__(self):
        return self.item