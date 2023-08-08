from django.db import models

M_OR_F = (
    (
        ('F', 'Female'),
        ('M', 'Male'),
        ('U', 'Unisex'),
    )
)

class Brand(models.Model):

    class Meta:
        verbose_name_plural = 'Brands'

    name = models.CharField(max_length=254)

    def __str__(self):
        return self.name


class Domain(models.Model):

    class Meta:
        verbose_name_plural = 'Domains'

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Category(models.Model):

    class Meta:
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)
    domain = models.ForeignKey("Domain", null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name

    def get_friendly_name(self):
        return self.friendly_name


class Product(models.Model):

    class Meta:
        verbose_name_plural = 'Products'

    brand = models.ForeignKey('Brand', null=True, on_delete=models.SET_NULL)
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    domain = models.IntegerField(null=True, blank=True)
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    m_or_f = models.CharField(null=True, max_length=254, choices=M_OR_F)

    def __str__(self):
        return self.name

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
                str(random.randint(10000, 99999))
            )

        super().save(*args, **kwargs)

