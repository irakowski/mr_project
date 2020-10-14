import pytest
from django.urls import reverse
from inv.models import Product
from faker import Faker
from django.db.models import ProtectedError

fake = Faker()

@pytest.mark.django_db
def test_add_product_view_for_unauthenticated_users(client):
    """
    Test if unauthenticated will be redirected to login page
    """
    add_product_url = reverse('add-product')
    response = client.get(add_product_url)
    assert response.status_code == 302
    assert response.url == "/accounts/login/?next=/products/add-product/"

@pytest.mark.django_db
def test_add_product_view_for_authenticated_users(user_company, client):
    """
    Verifies that authenticated users can view this page
    """
    add_product_url = reverse('add-product')
    response = client.get(add_product_url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_form_submition_and_product_creation(user_company, client, authenticated_user):
    """
    Verifies product gets created upon form submittion and redirects
    """
    add_product_url = reverse('add-product')
    response = client.post(add_product_url, {
        'name': 'Test_product_name',
        'serial_number': 'XZ001', 
        'manufacturer': 'Test company',
        'price_net': 415.26,
        'description': fake.paragraph(),
        'stock': 16
    })
    assert response.status_code == 302
    product = Product.objects.get(name='Test_product_name')
    assert response.url == reverse('product-detail',kwargs={'pk': product.pk}) 
    assert product.user == authenticated_user
    assert product in Product.objects.all()
    
@pytest.mark.django_db
def test_product_list_view(sample_product, user_company, client):
    """
    Veryfies that list view returns all created products
    """
    product_list_url = reverse('product-list')
    response = client.get(product_list_url)
    assert response.status_code == 200
    assert Product.objects.count() == 9
    products = Product.objects.all()
    content = response.content.decode(response.charset)
    for product in products:
        assert product.name in content

@pytest.mark.django_db
def test_product_detail_view(client, sample_product, user_company, authenticated_user):
    """
    Verifies that all routes for products returning "OK" status if exists and 404 if not
    """
    products = Product.objects.all()
    for product in products:
        product_detail_view = reverse('product-detail', kwargs={'pk': product.pk})
        response = client.get(product_detail_view)
        #The view should return 200 for each product that exists
        assert response.status_code == 200
        content = response.content.decode(response.charset)
        #With content specific for each product
        assert product.name in content
    #checking for "page not found" if product does not exist
    product_not_exist_detail_view = reverse('product-detail', kwargs={'pk':104})
    response = client.get(product_not_exist_detail_view)
    assert response.status_code == 404 
    #Authenticated user but not the owner of the product returns 404
    if authenticated_user and not user_company:
        product_detail_view = reverse('product-detail', kwargs={'pk': 6})
        response = client.get(product_detail_view)
        assert response.status_code == 404
    
@pytest.mark.django_db
def test_edit_product_view(client, sample_product, user_company, authenticated_user):  
    products = Product.objects.all()
    assert len(products) == 9
    for product in products:
        edit_product_url = reverse('edit-product', kwargs={'pk': product.pk})
        response = client.get(edit_product_url)
        assert response.status_code == 200
  
        response = client.post(edit_product_url, {'name': fake.company(),
                        'serial_number': fake.ean8(),
                        'manufacturer': fake.company(),
                        'price_net': 199.99,
                        'description': fake.paragraph(),
                        'stock': 5,
                        'user':authenticated_user}, )
        assert response.status_code == 302
        assert response.url == reverse('product-detail', kwargs={'pk': product.pk})  
        product.refresh_from_db()
        assert product.stock == 5 
    assert len(products) == 9

@pytest.mark.django_db
def test_delete_product_view(client, sample_product, user_company, authenticated_user):
    products = Product.objects.all()
    assert len(products) == 9
    for product in products:
        delete_product_url = reverse('delete-product', kwargs={'pk':product.pk})
        response = client.get(delete_product_url)
        assert response.status_code == 200
    single_product = products[2]
    response = client.post(delete_product_url,{'id':single_product.id})
    assert response.status_code == 302
    assert response.url == reverse('product-list')
    assert Product.objects.count() == 8

@pytest.mark.django_db
def test_delete_protected(client, invoice_with_product_and_customer):
    for product in invoice_with_product_and_customer.products.all():
        delete_product_url = reverse('delete-product', kwargs={'pk': product.pk})
        response = client.post(delete_product_url)
        assert response.status_code == 200
            
