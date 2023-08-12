from django.shortcuts import render
from .forms import ProductForm

def add_product(request):
    """ Add a product to the store """
    form = ProductForm()
    template = 'admin_actions/admin_actions.html'
    context = {
        'form': form,
    }

    return render(request, template, context)
