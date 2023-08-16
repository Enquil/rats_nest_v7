from django.db import models
import random

M_OR_F = (
    (
        ('F', 'Female'),
        ('M', 'Male'),
        ('U', 'Unisex'),
    )
)


class Common(models.Model):
    ''' common fields for models '''
    name = models.CharField(max_length=254)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Friendly(models.Model):
    '''
    Common class for models that has friendly name
    '''
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    class Meta:
        abstract = True

    def get_friendly_name(self):
        return self.friendly_name


class Color(Common):

    class Meta:
        verbose_name_plural = 'Colors'


class Brand(Common):

    class Meta:
        verbose_name_plural = 'Brands'


class Domain(Common, Friendly):

    class Meta:
        verbose_name_plural = 'Domains'


class Category(Common, Friendly):

    class Meta:
        verbose_name_plural = 'Categories'

    domain = models.ForeignKey(
        "Domain", null=True, blank=True, on_delete=models.SET_NULL
    )


class Product(Common):

    class Meta:
        verbose_name_plural = 'Products'

    brand = models.ForeignKey('Brand', null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(
        'Category', null=True, blank=True, on_delete=models.SET_NULL
    )
    domain = models.IntegerField(null=True, blank=True)
    sku = models.CharField(max_length=254, null=True, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(
        max_digits=6, decimal_places=2, null=True, blank=True
    )
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    m_or_f = models.CharField(null=True, max_length=254, choices=M_OR_F)
    color = models.ForeignKey(
        'Color', null=True, blank=True, on_delete=models.SET_NULL
    )
    has_sizes = models.BooleanField(default=False, null=True, blank=True)

    def save(self, *args, **kwargs):
        '''
        Autofills domain and sku
        '''
        if not self.domain:
            self.domain = self.category.domain.id

        if not self.sku:
            self.sku = (
                f'{self.domain}' +
                f'{self.brand.id}' +
                f'{self.category.id}' +
                f'{self.color.id}' +
                str(random.randint(10000, 99999))
            )

        super().save(*args, **kwargs)
