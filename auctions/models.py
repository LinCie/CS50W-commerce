from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from django.core.validators import MinValueValidator
from .functions import USD_format

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
    
    def usd_formatted(self):
        return USD_format(self.starting_bid)


class Watchlist(models.Model):
    
    user = models.ForeignKey(User, verbose_name=("username"), on_delete=models.CASCADE)
    listing = models.ManyToManyField(Listing)

    class Meta:
        verbose_name = "watchlist"
        verbose_name_plural = "watchlists"

    def __str__(self):
        return f"{self.user.username}'s Watchlist"


class Category(models.Model):

    name = models.CharField("Category", unique=True, max_length=64)
    slug = models.SlugField("Slug URL", unique=True, default="")
    listing = models.ManyToManyField(Listing)

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        slug = slugify(self.name)
        return reverse("category_detail", kwargs={"slug": slug})
    
    
class Bid(models.Model):

    listing = models.ForeignKey(Listing, verbose_name=_("listing"), on_delete=models.CASCADE)
    bidder = models.ForeignKey(User, verbose_name=_("user"), on_delete=models.CASCADE)
    bid = models.FloatField(_("Bid"), validators=[MinValueValidator(0.01)])

    class Meta:
        verbose_name = _("bid")
        verbose_name_plural = _("bids")

    def __str__(self):
        return f"{self.bidder} bid of ${self.bid:,.2f} for {self.listing}"
    
    def get_absolute_url(self):
            return reverse("bid", kwargs={"pk": self.pk})
        
    def usd_formatted(self):
        return USD_format(self.bid)


class Comment(models.Model):

    listing = models.ForeignKey(Listing, verbose_name=_("listing"), on_delete=models.CASCADE)
    commenter = models.ForeignKey(User, verbose_name=_("user"), on_delete=models.CASCADE)
    comment = models.TextField(_("comment"))

    class Meta:
        verbose_name = _("comment")
        verbose_name_plural = _("comments")

    def __str__(self):
        return f"{self.commenter}'s comments {self.comment} on {self.listing}"

    def get_absolute_url(self):
        return reverse("comment_detail", kwargs={"pk": self.pk})

