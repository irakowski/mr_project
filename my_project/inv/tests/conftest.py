import pytest
from django.test import Client
from django.contrib.auth.models import User 
from faker import Faker
from inv.models import Company, Product, Customer, Invoice, InvoiceItem
from django.core.files.uploadedfile import SimpleUploadedFile

@pytest.fixture
def client():
    """
    Creates a client instance for the tests
    """
    client = Client()
    return client


@pytest.fixture
def authenticated_user(client):
    """
    Creates an authenticated user for the tests
    """
    user = User(username='test_username_123')
    user.set_password('test_password_123')
    user.save()    
    
    client.login(username='test_username_123', password='test_password_123')
    return user
   

fake = Faker()
@pytest.fixture
def user_company(authenticated_user):
    """
    Creates Company for the authenticated user
    """
    logo = SimpleUploadedFile(name='test_logo.png', 
                    content=open('inv/tests/test_logo.png', 'rb').read(), 
                    content_type='image/png')

    company = Company(user=authenticated_user,
                    name='Company For User',
                    nip='3934678723',
                    address = fake.street_address(),
                    city=fake.city(),
                    zip_code=fake.postcode(),
                    country=fake.country(),
                    position=fake.job(),
                    logo=logo)
    company.save()
    return company


import random
@pytest.fixture
def sample_product(authenticated_user):
    for _ in range(1,10):
        product = Product(name=fake.company(),
                        serial_number=fake.ean8(),
                        manufacturer=fake.company(),
                        price_net=random.uniform(150.00, 450.00),
                        description=fake.paragraph(),
                        stock=random.randint(1,16),
                        user=authenticated_user)
        product.save()
    return product


@pytest.fixture
def sample_customer(user_company):
    for _ in range(1,10):
        customer = Customer(user=user_company, customer_type=random.choice(['Indywidualny', 'Biznesowy']),
            name=fake.company(),nip=random.choice(['1189201244','5190575248', '5274393925', '7980553696']),
            address=fake.street_address(),city=fake.city(), zip_code=fake.postcode(),
            country=fake.country(), regon=fake.ean(), krs=fake.ean(),
            contact=fake.phone_number(), email=fake.company_email(), 
            representation=fake.name()) 
        customer.save()
    return customer


@pytest.fixture
def sample_invoice(user_company, sample_product, sample_customer):
    for _ in range(1,10):
        invoice = Invoice(users_company=user_company, customer=sample_customer,
                        number=fake.bothify(text='????-####'), invoice_type=random.choice(['Pro-Forma', 'VAT']),
                        payment_option=random.choice(['Przelew', 'Gotówka']))
        invoice.save()
    return invoice

from datetime import date
@pytest.fixture
def invoice_with_product_and_customer(sample_customer, sample_product, user_company):
    invoice = Invoice(users_company=user_company, customer=sample_customer,
                    number='08/31/2020', invoice_type='Pro-Forma',
                    date_issued=date(2020, 8, 31), order_date=date(2020, 8, 31),
                    payment_option='Przelew',due_date=date(2020, 9, 3))
    invoice.save()
    invoice_item = InvoiceItem(product=sample_product, invoice=invoice, vat_fee=0.23, product_quantity=2)
    invoice_item.total_net = sample_product.price_net * invoice_item.product_quantity
    invoice_item.total_vat = invoice_item.total_net * invoice_item.vat_fee
    invoice_item.total_per_products = invoice_item.total_net + invoice_item.total_vat
    invoice_item.save()
    invoice.total_net_amount = invoice_item.total_net
    invoice.total_vat_amount = invoice_item.total_vat
    invoice.total_gross_amount = invoice_item.total_per_products
    invoice.save()
    return invoice