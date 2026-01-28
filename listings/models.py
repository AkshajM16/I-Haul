from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

class Category(models.Model):
    """
    Item category for the marketplace.
    """
    name = models.CharField(max_length=255)
    # Blank allowed for admin convenience.
    slug = models.SlugField(unique=True, blank=True, db_index=True)

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
    
    # Create a URL-friendly slug from the category name
    # If that slug is already taken, add “-2”, “-3”, ...
    
    def _build_unique_slug(self) -> str:
        base = slugify(self.name) or "category"
        # DB default limit = 50 for slugs
        base = base[:45]  # Leaving room for numbers at the end of slug
        slug = base
        i = 2
        while Category.objects.filter(slug=slug).exclude(pk=self.pk).exists():
            slug = f"{base}-{i}"
            i += 1
        return slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._build_unique_slug()
        
        return super().save(*args, **kwargs)


class Listing(models.Model):
    """
    A single marketplace listing posted by a user.
    """
    category = models.ForeignKey(Category, related_name="listings", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    # Allow empty descriptions
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to="item_images/", blank=True, null=True)
    is_sold = models.BooleanField(default=False)
    seller = models.ForeignKey(User, related_name="listings", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # Newest listings first.
        ordering = ("-created_at",)

    def __str__(self):
        # Keep concise representation for logs.
        return f"{self.title}"
