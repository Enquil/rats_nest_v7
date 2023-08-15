from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path(
        '', views.admin_actions,
        name='admin_actions'
    ),
    path(
        'add/', views.add_product,
        name='add_product'
    ),
    path(
        'edit/<int:product_id>/', views.edit_product,
        name='edit_product'
    ),
    path(
        'delete/<int:product_id>/', views.delete_product,
        name='delete_product'
    ),
    path(
        'newsletter/', views.newsletter,
        name='newsletter'
    ),
]
