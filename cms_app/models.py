from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


def upload_articles(instance, filename):
    ext = filename.split(".")[-1]
    name = "{:%Y%m%d_%H%M%S}_{}".format(datetime.now(), instance.slug)
    return "articles/{}.{}".format(name, ext)

def upload_teams(instance, filename):
    ext = filename.split(".")[-1]
    name = "{:%Y%m%d_%H%M%S}_{}".format(datetime.now(), instance.name)
    return "teams/{}.{}".format(name, ext)


def upload_file(instance, filename):
    ext = filename.split(".")[-1]
    name = "{:%Y%m%d_%H%M%S}_{}".format(datetime.now(), instance.name)
    return "file/{}.{}".format(name, ext)


# Create your models here.
class IPAddressDetail(models.Model):
    ip = models.GenericIPAddressField()
    network = models.CharField(max_length=18)  # /22 adalah karakter maksimum untuk CIDR
    version = models.CharField(max_length=10)
    city = models.CharField(max_length=100, null=True, blank=True)
    region = models.CharField(max_length=100, null=True, blank=True)
    region_code = models.CharField(max_length=10, null=True, blank=True)
    country = models.CharField(max_length=5)  # Kode negara pendek
    country_name = models.CharField(max_length=100)
    country_code = models.CharField(max_length=5)  # Kode negara
    country_code_iso3 = models.CharField(max_length=3)  # Kode negara ISO3
    country_capital = models.CharField(max_length=100, null=True, blank=True)
    country_tld = models.CharField(max_length=10)  # TLD negara
    continent_code = models.CharField(max_length=2)  # Kode benua
    in_eu = models.BooleanField(default=False)
    postal = models.CharField(max_length=20, null=True, blank=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    timezone = models.CharField(max_length=50)
    utc_offset = models.CharField(max_length=10)  # Misalnya +0700
    country_calling_code = models.CharField(max_length=10)
    currency = models.CharField(max_length=10)
    currency_name = models.CharField(max_length=50)
    languages = models.CharField(max_length=100)  # Daftar bahasa
    country_area = models.FloatField()  # Luas negara
    country_population = models.BigIntegerField()  # Populasi negara
    asn = models.CharField(max_length=50)  # ASN
    org = models.CharField(max_length=100, null=True, blank=True)  # Organisasi

    def _str_(self):
        return f"{self.ip} - {self.city}, {self.country_name}"


class Article(models.Model):
    # Inisial Tabel
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to=upload_articles, null=True, blank=True)
    content = models.TextField()
    slug = models.SlugField(max_length=255, unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="articles")
    status = models.CharField(
        max_length=10,
        choices=(
            ("draft", "Draft"),
            ("published", "Published"),
        ),
        default="published",
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)


class Team(models.Model):
    # Inisial Tabel
    name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    image = models.ImageField(upload_to=upload_teams, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)


class Visitor(models.Model):
    ipaddressdetail = models.ForeignKey(
        IPAddressDetail,
        on_delete=models.SET_NULL,
        related_name="ipaddress_detail_visitor",
        null=True,
    )
    ip_address = models.CharField(max_length=255)
    agent = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-id"]


class MasterFile(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to=upload_file, null=True)
    size = models.CharField(max_length=16, null=True, blank=True)
    type = models.CharField(max_length=5, null=True, blank=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        related_name="create_file",
        null=True,
    )
    updated_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="updated_file", null=True
    )
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-updated_at"]
