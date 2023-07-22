from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse

from django.core.validators import MinValueValidator

class User(AbstractUser):
    pass


class Listing(models.Model):

    name = models.CharField("listing name", max_length=50)
    lister = models.ForeignKey(User, verbose_name=("lister name"), on_delete=models.CASCADE)
    starting_bid = models.FloatField(("starting bid"), validators=[MinValueValidator(0.01)])
    image_url = models.URLField(("image url"), max_length=256)
    description = models.TextField(("listing description"))
    datetime = models.DateTimeField(("datetime"), auto_now_add=True)
    
    class Meta:
        verbose_name = ("listing")
        verbose_name_plural = ("listings")

    def __str__(self):
        return f"{self.name} by {self.lister}"

    def get_absolute_url(self):
        return reverse("listing_detail", kwargs={"pk": self.pk})

class Watchlist(models.Model):
    user = models.ForeignKey(User, verbose_name=("username"), on_delete=models.CASCADE)
    listing = models.ManyToManyField(Listing)

    class Meta:
        verbose_name = "watchlist"
        verbose_name_plural = "watchlists"

    def __str__(self):
        return f"{self.user.username}'s Watchlist"
