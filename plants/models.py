from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=150)
    flag = models.ImageField(upload_to="countries/")

    def __str__(self):
        return self.name


class Plant(models.Model):

    class CategoryChoices(models.TextChoices):
        INDOOR = "indoor", "Indoor"
        OUTDOOR = "outdoor", "Outdoor"
        SUCCULENT = "succulent", "Succulent"
        HERB = "herb", "Herb"
        OTHER = "other", "Other"

    name = models.CharField(max_length=200)
    about = models.TextField()
    used_for = models.TextField()
    image = models.ImageField(upload_to="plants/")
    category = models.CharField(
        max_length=20,
        choices=CategoryChoices.choices
    )
    is_edible = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    countries = models.ManyToManyField(
        Country,
        related_name="plants",
        blank=True,
    )

    def __str__(self):
        return self.name
