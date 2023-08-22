from django.shortcuts import render, reverse, get_object_or_404, redirect
from .forms import ProductForm, NewsletterForm
from products.models import Product
from .models import Newsletter
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.conf import settings


@login_required
def admin_actions(request):

    if request.user.is_superuser:
        template = 'admin_actions/admin_actions.html'
        return render(request, template)
    else:
        raise PermissionDenied


@login_required
def add_product(request):
    """ Add a product to the store """
    if request.user.is_superuser:
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'Successfully added product!')
                return redirect(reverse('add_product'))
            else:
                messages.error(
                    request,
                    'Failed to add product. Please ensure the form is valid.'
                )
        else:
            form = ProductForm()

        template = 'admin_actions/add_product.html'
        context = {
            'form': form,
        }

        return render(request, template, context)
    else:
        raise PermissionDenied


@login_required
def edit_product(request, product_id):
    """ Edit an existing product """

    # Get the product from the id passed as an argument
    if request.user.is_superuser:
        product = get_object_or_404(Product, pk=product_id)

        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES, instance=product)
            if form.is_valid():
                form.save()
                messages.success(request, 'Successfully updated product!')
                return redirect(reverse('product_detail', args=[product.id]))
            else:
                messages.error(
                    request,
                    'Failed to update product. '
                    'Please ensure the form is valid.'
                )
        else:
            form = ProductForm(instance=product)
            messages.info(request, f'You are editing {product.name}')

        template = 'admin_actions/edit_product.html'
        context = {
            'form': form,
            'product': product,
        }

        return render(request, template, context)
    else:
        raise PermissionDenied


@login_required
def delete_product(request, product_id):
    """ Delete a product from the store """
    if request.user.is_superuser:
        product = get_object_or_404(Product, pk=product_id)
        product.delete()
        messages.success(request, 'Product deleted!')
        return redirect(reverse('products'))
    else:
        raise PermissionDenied


@login_required
def newsletter(request):
    """ Newsletter view """
    if request.user.is_superuser:
        if request.method == 'POST':
            form = NewsletterForm(request.POST, request.FILES, instance=product)
            # if form.is_valid():
            #     form.save()
            send_mail(
                f'{request.POST["subject"]}',
                f'{request.POST["content"]}',
                "from@example.com",
                ["to@example.com", "example2@example.com"],
                fail_silently=False,
            )
            return redirect(reverse('newsletter'))
        else:
            form = NewsLetterForm()
            template = 'admin_actions/newsletter.html'
            context = {
                'form': form,
            }
        return render(request, template, context)
    else:
        raise PermissionDenied
