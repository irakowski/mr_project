"""twitter_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from inv.views import Main, SearchView, CustomerList, CustomerDetails, AddCustomer, \
EditCustomer, DeleteCustomer, ProductList, ProductDetail, AddProduct, EditProduct, \
DeleteProduct, InvoiceItem, InvoiceList, InvoiceDetail, InvoiceUpdateView, \
CreatePreOrderInvoice, CreateVATinvoice, CreateCompanyProfile, \
LandingPage, RegistrationView, CompanyProfileDetail, UpdateCompanyProfile, Pdf, \
DeleteInvoice


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LandingPage.as_view(), name='landing-page'),
    path('register/', RegistrationView.as_view(), name='register'), 
    path('accounts/', include('django.contrib.auth.urls')),
    path('add-company/', CreateCompanyProfile.as_view(),name='create-company-profile'),
    path('main/<str:slug>/', CompanyProfileDetail.as_view(), name='company-profile'),
    path('main/<str:slug>/edit/', UpdateCompanyProfile.as_view(), name='update-company-profile'),
    path('main/', Main.as_view(), name="main"),
    path('search/', SearchView.as_view(), name='search'),
    
    path('customers/', CustomerList.as_view(), name='customers'),
    path('customers/<int:pk>/', CustomerDetails.as_view(), name='customer-detail'),
    path('customers/add-customer/', AddCustomer.as_view(), name='add-customer'), 
    path('customers/edit-customer/<int:pk>/', EditCustomer.as_view(), name='edit-customer'),
    path('customers/delete-customer/<int:pk>/', DeleteCustomer.as_view(), name='delete-customer'),

    path('products/', ProductList.as_view(), name='product-list'),
    path('products/<int:pk>/',ProductDetail.as_view(), name='product-detail'),
    path('products/add-product/', AddProduct.as_view(), name='add-product'),
    path('products/edit-product/<int:pk>/', EditProduct.as_view(), name='edit-product'),
    path('products/delete-product/<int:pk>/', DeleteProduct.as_view(), name='delete-product'),
    
    path('invoices/', InvoiceList.as_view(), name='invoices'), 
    path('invoices/add-preorder-invoice/', CreatePreOrderInvoice.as_view(), name='add-preorder-invoice'),
    path('invoices/add-vat-invoice/', CreateVATinvoice.as_view(), name='add-vat-invoice'),
    path('invoices/<int:pk>/', InvoiceDetail.as_view(), name='invoice-detail'),
    path('invoices/<int:pk>/edit/', InvoiceUpdateView.as_view(), name='edit-invoice'),
    path('invoices/<int:pk>/delete/',DeleteInvoice.as_view(), name='delete-invoice'),
    path('invoices/render-pdf/<int:pk>/', Pdf.as_view(), name='pdf'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
