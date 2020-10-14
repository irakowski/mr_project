import pytest
from django.urls import reverse
from inv.models import Customer
from faker import Faker
from django.db.models import ProtectedError

fake = Faker()

@pytest.mark.django_db
def test_add_customer_view_for_unauthenticated_users(client):
    """
    Test if unauthenticated will be redirected to login page
    """
    add_customer_url = reverse('add-customer')
    response = client.get(add_customer_url)
    assert response.status_code == 302
    assert "/accounts/login/" in response.url

@pytest.mark.django_db
def test_add_customer_view_for_authenticated_users(user_company, client):
    """
    Verifies that authenticated users can view this page
    """
    add_customer_url = reverse('add-customer')
    response = client.get(add_customer_url)
    assert response.status_code == 200

import random
@pytest.mark.django_db
def test_form_submition_and_customer_creation(user_company, client):
    """
    Verifies customer gets created upon form submittion and redirects
    """
    add_customer_url = reverse('add-customer')
    response = client.post(add_customer_url, {
        'user': user_company, 'customer_type': random.choice(['Indywidualny', 'Biznesowy']),
        'name': 'TEST Client Company','nip': random.choice(['1189201244','5190575248', '5274393925', '7980553696']),
        'address': fake.street_address(),
        'city': fake.city(), 'zip_code':fake.postcode(),
        'country': fake.country(), 'regon': fake.ean(), 'krs':fake.ean(),
        'contact': fake.phone_number(), 'email': fake.company_email(), 
        'representation':fake.name()
    })
    assert response.status_code == 302
    sample_customer = Customer.objects.get(name='TEST Client Company')
    assert response.url == reverse('customers') 
    assert sample_customer.user == user_company
    assert sample_customer in Customer.objects.all()
    

@pytest.mark.django_db
def test_customer_list_view(sample_customer, user_company, client):
    """
    Veryfies that list view returns all created products
    """
    customer_list_url = reverse('customers')
    response = client.get(customer_list_url)
    assert response.status_code == 200
    assert Customer.objects.count() == 9
    customers = Customer.objects.all()
    content = response.content.decode(response.charset)
    for customer in customers:
        assert customer.name in content

@pytest.mark.django_db
def test_customer_detail_view(client, sample_product, user_company, authenticated_user):
    """
    Verifies that all routes for customers returning "OK" status if exists and 404 if not
    """
    customers = Customer.objects.all()
    for customer in customers:
        customer_detail_view = reverse('customer-detail', kwargs={'pk': customer.pk})
        response = client.get(customer_detail_view)
        #The view should return 200 for each product that exists
        assert response.status_code == 200
        content = response.content.decode(response.charset)
        #With content specific for each product
        assert customer in content
    #checking for "page not found" if product does not exist
    customer_not_exist_detail_view = reverse('customer-detail', kwargs={'pk':41})
    response = client.get(customer_not_exist_detail_view)
    assert response.status_code == 404 
    #Authenticated user but not the owner of the product returns 404
    if authenticated_user and not user_company:
        customer_detail_view = reverse('customer-detail', kwargs={'pk': 6})
        response = client.get(customer_detail_view)
        assert response.status_code == 404
    
@pytest.mark.django_db
def test_edit_customer_view(client, sample_customer, user_company, authenticated_user):  
    customers = Customer.objects.all()
    assert len(customers) == 9
    for customer in customers:
        edit_customer_url = reverse('edit-customer', kwargs={'pk': customer.pk})
        response = client.get(edit_customer_url)
        assert response.status_code == 200
  
        response = client.post(edit_customer_url, {
                'user': user_company, 'customer_type': random.choice(['Indywidualny', 'Biznesowy']),
                'name': fake.company(),'nip': random.choice(['1189201244','5190575248', '5274393925', '7980553696']),
                'address': fake.street_address(),
                'city': fake.city(), 'zip_code':fake.postcode(),
                'country': 'Polska', 'regon': fake.ean(), 'krs':fake.ean(),
                'contact': fake.phone_number(), 'email': fake.company_email(), 
                'representation':fake.name() })
        assert response.status_code == 302
        assert response.url == reverse('customers')  
        customer.refresh_from_db()
        assert customer.country == 'Polska' 
    assert len(customers) == 9
    if authenticated_user and not user_company:
        customer_detail_view = reverse('customer-detail', kwargs={'pk': 6})
        response = client.get(customer_detail_view)
        assert response.status_code == 404

@pytest.mark.django_db
def test_delete_customer_view(client, sample_customer, user_company, authenticated_user):
    customers = Customer.objects.all()
    assert len(customers) == 9
    for customer in customers:
        delete_customer_url = reverse('delete-customer', kwargs={'pk': customer.pk})
        response = client.get(delete_customer_url)
        assert response.status_code == 200
    single_customer = customers[2]
    response = client.post(delete_customer_url,{'id':single_customer.id})
    assert response.status_code == 302
    assert response.url == reverse('customers')
    assert Customer.objects.count() == 8


@pytest.mark.django_db
def test_delete_with_protected(client, invoice_with_product_and_customer):
    customer = invoice_with_product_and_customer.customer
    delete_customer_url = reverse('delete-customer', kwargs={'pk': customer.pk})
    response = client.post(delete_customer_url)
    assert response.status_code == 200
            