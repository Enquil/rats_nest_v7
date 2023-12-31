from django import forms
from products.models import Product, Category, Color, Brand, Domain
from .models import Newsletter


class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        self.fields['category'].choices = friendly_names
        self.fields['category'].required = True
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'


class NewsletterForm(forms.ModelForm):

    class Meta:
        model = Newsletter
        fields = ('subject', 'content')
    