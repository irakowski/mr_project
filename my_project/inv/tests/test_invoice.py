import pytest
from django.urls import reverse
from inv.models import Customer, Product, Invoice, InvoiceItem


@pytest.mark.django_db
def test_create_preorder_invoice_view_access(user_company, client):
    """
    Veryfies view is returning 'OK' for logged in user
    """
    create_invoice_url = reverse('add-preorder-invoice')
    response = client.get(create_invoice_url)
    assert response.status_code == 200
    if not user_company:
        assert response.status_code == 302


import datetime
@pytest.mark.django_db
def test_create_preorder_invoice_POST(user_company, client, sample_customer, sample_product):
    """
    Veryfies Invoice and InvoiceItems gets saved into database with calculations
    upon form and formset submittion
    """
    create_invoice_url = reverse('add-preorder-invoice')
    assert Invoice.objects.count() == 0
    post_data = {'users_company': user_company, 
                'customer': sample_customer.pk,
                'number':'02/2020',
                'invoice_type': 'VAT',
                'date_issued': datetime.date(2020, 8, 31), 
                'order_date': datetime.date(2020, 8, 31), 
                'payment_option': 'Przelew',
                'due_date': datetime.date(2020, 9, 3),
                #management formset_data
                'invoiceitem_set-TOTAL_FORMS': '3',
                'invoiceitem_set-INITIAL_FORMS': '0', 
                'invoiceitem_set-MIN_NUM_FORMS': '0', 
                'invoiceitem_set-MAX_NUM_FORMS':'1000',
                #first_invoiceitem
                #'invoiceitem_set-0-id': '0',
                'invoiceitem_set-0-product': sample_product.pk,
                'invoiceitem_set-0-product_quantity': '2',
                'invoiceitem_set-0-vat_fee': '0.23',
                'invoiceitem_set-0-DELETE': False, 

                #second invoiceitem                
                #'invoiceitem_set-1-id': 1,
                'invoiceitem_set-1-product_quantity': '0',
                'invoiceitem_set-1-vat_fee': '0.23',
                'invoiceitem_set-1-DELETE': True,

                #third invoiceitem
                #'invoiceitem_set-2-id': 2,
                'invoiceitem_set-2-product_quantity': '0',
                'invoiceitem_set-2-vat_fee': '0.23',
                'invoiceitem_set-2-DELETE': True }
    response = client.post(create_invoice_url, post_data)
    assert response.status_code == 302
    assert Invoice.objects.count() == 1
    invoice = Invoice.objects.all().last()
    prod_qnt = post_data.get('invoiceitem_set-0-product_quantity')
    ##comparing floating points with approx class
    assert invoice.total_net_amount == pytest.approx(sample_product.price_net * int(prod_qnt))
    assert response.url == reverse('invoices')


@pytest.mark.django_db
def test_create_vat_invoice(user_company, sample_customer, sample_product, client):
    """
    Verifies creation of invoice instance upon successfull form and formset submition
    """ 
    create_vat_inv_url = reverse('add-vat-invoice')
    response = client.get(create_vat_inv_url)
    assert response.status_code == 200

    assert Invoice.objects.count() == 0
    post_data = {'users_company': user_company, 
                'customer': sample_customer.pk,
                'number':'01/2020',
                'invoice_type': 'Pro-Forma',
                'date_issued': datetime.date(2020, 8, 31), 
                'order_date': datetime.date(2020, 8, 31), 
                'payment_option': 'Przelew',
                'due_date': datetime.date(2020, 9, 3),
                #management formset_data
                'invoiceitem_set-TOTAL_FORMS': '3',
                'invoiceitem_set-INITIAL_FORMS': '0', 
                'invoiceitem_set-MIN_NUM_FORMS': '0', 
                'invoiceitem_set-MAX_NUM_FORMS':'1000',
                #first_invoiceitem
                #'invoiceitem_set-0-id': '0',
                'invoiceitem_set-0-product': sample_product.pk,
                'invoiceitem_set-0-product_quantity': '5',
                'invoiceitem_set-0-vat_fee': '0.23',
                'invoiceitem_set-0-DELETE': False, 

                #second invoiceitem                
                #'invoiceitem_set-1-id': 1,
                'invoiceitem_set-1-product': sample_product.pk,
                'invoiceitem_set-1-product_quantity': '3',
                'invoiceitem_set-1-vat_fee': '0.23',
                'invoiceitem_set-1-DELETE': False,

                #third invoiceitem
                #'invoiceitem_set-2-id': 2,
                'invoiceitem_set-2-product_quantity': '0',
                'invoiceitem_set-2-vat_fee': '0.23',
                'invoiceitem_set-2-DELETE': True }
    response = client.post(create_vat_inv_url, post_data)
    assert response.status_code == 302 
    assert Invoice.objects.count() == 1
    invoice = Invoice.objects.all().last()
    invoice_items = InvoiceItem.objects.filter(invoice=invoice)
    assert len(invoice_items) == 2
    #calculation for total net invoice
    f_prod = post_data.get('invoiceitem_set-0-product')
    f_price_net = Product.objects.get(pk=int(f_prod))
    f_prod_qnt = post_data.get('invoiceitem_set-0-product_quantity')
    f_net = f_price_net.price_net * int((f_prod_qnt))

    s_prod = post_data.get('invoiceitem_set-1-product')
    s_price_net = Product.objects.get(pk=int(s_prod))
    s_prod_qnt = post_data.get('invoiceitem_set-1-product_quantity')
    s_net = s_price_net.price_net * int(s_prod_qnt)
    ##total for invoice instance == calculations for net for invoiceitems instance
    assert invoice.total_net_amount == pytest.approx(s_net + f_net)
    assert response.url == reverse('invoices')


@pytest.mark.django_db
def test_invoice_list(user_company, client, sample_invoice, authenticated_user):
    """
    Veryfies view returns all invoices for current users_company
    """
    invoice_list_url = reverse('invoices')
    response = client.get(invoice_list_url)
    assert response.status_code == 200
    assert Invoice.objects.count() == 9
    invoices = Invoice.objects.all()
    content = response.content.decode(response.charset)
    for invoice in invoices:
        assert invoice.number in content
    if authenticated_user and not user_company:
        assert Invoice.objects.count() == 0


@pytest.mark.django_db
def test_invoice_detail_view(user_company, authenticated_user, client, sample_invoice):
    invoices = Invoice.objects.all()
    for invoice in invoices:
        invoice_detail_url = reverse('invoice-detail', kwargs={'pk':invoice.pk})
        response = client.get(invoice_detail_url)
        assert response.status_code == 200
        content = response.content.decode(response.charset)
        #With content specific for each invoice
        assert invoice.number in content
    #checking for "page not found" if invoice does not exist
    invoice_not_exist_detail_view = reverse('invoice-detail', kwargs={'pk': 154})
    response = client.get(invoice_not_exist_detail_view)
    assert response.status_code == 404 
    #Authenticated user but not the owner of the invoice returns 404
    if authenticated_user and not user_company:
        invoice_detail_view = reverse('invoice-detail', kwargs={'pk': 10})
        response = client.get(invoice_detail_view)
        assert response.status_code == 404


from faker import Faker
from datetime import date
fake = Faker()
@pytest.mark.django_db
def test_edit_invoice(user_company, client, sample_customer, sample_product, sample_invoice):
    invoices = Invoice.objects.all()
    assert len(invoices) == 9
    for invoice in invoices:
        edit_invoice_url = reverse('edit-invoice', kwargs={'pk': invoice.pk})
        response = client.get(edit_invoice_url)
        assert response.status_code == 200

        response = client.post(edit_invoice_url, {'number': fake.bothify(text='Edited Invoice: ??-2020'),
                        'users_company': user_company,
                        'customer': sample_customer.pk,
                        'invoice_type': 'VAT',
                        'date_issued': date(2020, 8, 31),
                        'order_date': date(2020, 8, 29),
                        'payment_option': 'Przelew',
                        'due_date':date (2020, 9, 3), 
                        #management formset_data
                        'invoiceitem_set-TOTAL_FORMS': '3',
                        'invoiceitem_set-INITIAL_FORMS': '0', 
                        'invoiceitem_set-MIN_NUM_FORMS': '0', 
                        'invoiceitem_set-MAX_NUM_FORMS':'1000',
                        #first_invoiceitem
                        #'invoiceitem_set-0-id': '0',
                        'invoiceitem_set-0-product': sample_product.pk,
                        'invoiceitem_set-0-product_quantity': '5',
                        'invoiceitem_set-0-vat_fee': '0.23',
                        'invoiceitem_set-0-DELETE': False, 
                        
                        #second invoiceitem                
                        #'invoiceitem_set-1-id': 1,
                        'invoiceitem_set-1-product_quantity': '0',
                        'invoiceitem_set-1-vat_fee': '0.23',
                        'invoiceitem_set-1-DELETE': True,

                        #third invoiceitem
                        #'invoiceitem_set-2-id': 2,
                        'invoiceitem_set-2-product_quantity': '0',
                        'invoiceitem_set-2-vat_fee': '0.23',
                        'invoiceitem_set-2-DELETE': True })
    
        assert response.status_code == 302
        assert response.url == reverse('invoice-detail', kwargs={'pk': invoice.pk})  
        invoice.refresh_from_db()
        assert invoice.invoice_type == 'VAT'
    assert len(invoices) == 9