from django.db import models


class Library(models.Model):

    name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    address = models.TextField()

    latitude = models.FloatField(default=0)
    longitude = models.FloatField(default=0)

    logo = models.ImageField(
        upload_to='library_logos/',
        blank=True,
        null=True,
        help_text="Upload the library's logo image."
    )

    qr_code = models.ImageField(
        upload_to='library_qrs/',
        blank=True,
        null=True,
        help_text="Upload a UPI QR code for users to scan when paying fines."
    )

    def __str__(self):
        return self.name