import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from inv.models import Company

@pytest.mark.django_db
def test_update_user_company_url_access(user_company, client, authenticated_user):
    update_user_company_url = reverse('update-company-profile', kwargs={'slug': user_company.slug})
    response = client.get(update_user_company_url)
    assert response.status_code == 200
    if authenticated_user and not user_company:
        assert response.status_code == 404


from django.core.files.uploadedfile import SimpleUploadedFile
@pytest.mark.django_db
def test_update_user_company_POST(user_company, client, authenticated_user):
    update_user_company_url = reverse('update-company-profile', kwargs={
                                                            'slug': user_company.slug})
    logo = SimpleUploadedFile(name='my_new_cool_logo.png', 
                    content=open('inv/tests/my_new_cool_logo.png', 'rb').read(), 
                    content_type='image/png')

    response = client.post(update_user_company_url, {
        'name': 'New Name', 
        'logo': logo,
        'nip': user_company.nip, 
        'address': 'ul. Updated Street 2', 
        'city': user_company.city,
        'zip_code':user_company.zip_code,
        'country': 'Poland', 
        'position': 'Promoted to Main Accountant'
    })
    assert response.status_code == 302
    assert response.url == reverse('main')
    company = Company.objects.get(name='New Name')
    assert company.nip == '3934678723'
    
@pytest.mark.django_db
def test_company_detail_view(user_company, client, authenticated_user):
    company_detail_url = reverse('company-profile', kwargs={'slug':user_company.slug})
    response = client.get(company_detail_url)
    assert response.status_code == 200
    if authenticated_user and not user_company:
        assert response.status_code == 404