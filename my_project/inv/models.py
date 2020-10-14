from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.template.defaultfilters import slugify
from .validators import nip_validator
from .choices import CUSTOMER_TYPE_CHOICES, BUSINESS, INDIVIDUAL, INVOICE_TYPE, PRO_FORMA, \
    VAT, KOREKTA, PAYMENT_OPTIONS, PRZELEW, GOTOWKA, VAT_CHOICES
# Create your models here


class Customer(models.Model):
    """
    Model Respresenting user's Clients
    """
    user = models.ForeignKey('Company', on_delete=models.CASCADE, related_name='user_company')
    
    customer_type = models.CharField(max_length=15, 
                                      choices=CUSTOMER_TYPE_CHOICES, 
                                      default=BUSINESS, verbose_name='Typ klienta')
    name = models.CharField(max_length=100, verbose_name='Nazwa Klienta')
    nip = models.CharField(max_length=11, blank=True, validators=[nip_validator], 
                            verbose_name='NIP')
    address = models.CharField(max_length=100, verbose_name='Adres')
    city = models.CharField(max_length=100, verbose_name='Miasto')
    zip_code = models.CharField(max_length=10, verbose_name='Kod poczt.')
    country = models.CharField(max_length=100, verbose_name='Kraj')
    bank_account = models.CharField(max_length=25, blank=True, verbose_name='Konto bankowe') 
    regon = models.CharField(max_length=20, blank=True, verbose_name="REGON")
    krs = models.CharField(max_length=20, blank=True, verbose_name="KRS")
    contact = models.CharField(max_length=150,blank=True, verbose_name='Kontakt')
    email = models.EmailField(blank=True)
    webpage = models.URLField(blank=True, verbose_name='Strona WWW')
    representation = models.CharField(max_length=100, blank=True, 
                verbose_name='Osoba reprezentująca')
    date_added = models.DateTimeField(auto_now_add=True) 
    last_modified = models.DateTimeField(auto_now=True)
    
    objects = models.Manager()

    def __str__(self):
        return f'{self.name}({self.nip})'

def user_directory_path(instance, filename):
    """specifies path to users' logo uploads"""
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class Company(models.Model):
    """
    Model representation of User's company. One User - One company
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150, unique=True)
    nip = models.CharField(max_length=10, validators=[nip_validator])
    logo = models.ImageField(upload_to=user_directory_path, blank=True)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    bank_account = models.CharField(max_length=25, blank=True)
    position = models.CharField(max_length=100, blank=True, verbose_name="Stanowisko")
    
    objects = models.Manager()

    def save(self, *args, **kwargs):
        """
        Automatically creates slug for user's company name
        """
        self.slug = slugify(self.name)
        super(Company, self).save(*args, **kwargs)

    def __str__(self):
        """
        Returns human-readable name of the user's company
        """
        return f'{self.name}(NIP:{self.nip})'

class Product(models.Model):
    """
    Model representation for Product table
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    
    name = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=50, blank=True) #unique=true
    manufacturer = models.CharField(max_length=300, blank=True)
    price_net = models.FloatField()
    description = models.TextField(blank=True)
    available = models.BooleanField(default=True) 
    stock = models.PositiveIntegerField(default=1)
    photo = models.ImageField(upload_to='product_photo', blank=True, default='default.jpg')##need to set default
    slug = models.SlugField(max_length=100, editable=False)
    
    objects = models.Manager()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}({self.price_net} zł)'

class Invoice(models.Model):
    users_company = models.ForeignKey(Company,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, related_name='invoices')
    products = models.ManyToManyField(Product, through='InvoiceItem')
    
    number = models.CharField(max_length=100)
    invoice_type = models.CharField(max_length=15, choices=INVOICE_TYPE)
    date_issued = models.DateField(default=date.today)
    order_date = models.DateField(default=date.today)
    payment_option = models.CharField(max_length=10, choices=PAYMENT_OPTIONS, 
                                        blank=True, default=PRZELEW)
    due_date = models.DateField(default=date.today)
    total_net_amount = models.FloatField(default=0.00, null=True)
    total_gross_amount = models.FloatField(default=0.00, null=True)
    total_vat_amount = models.FloatField(default=0.00, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True, null=True)

    objects = models.Manager()
    
    class Meta:
        ordering = ['-date_issued']
        
    def __str__(self):
        return f'{self.number}({self.date_issued})'


class InvoiceItem(models.Model): 
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    invoice = models.ForeignKey(Invoice,on_delete=models.CASCADE)
    
    vat_fee = models.FloatField(choices=VAT_CHOICES, default=0.23)
    product_quantity = models.PositiveIntegerField(default=0)
    total_per_products = models.FloatField()
    total_net = models.FloatField()
    total_vat = models.FloatField()  
    objects =models.Manager()
    
    def __str__(self):
        return self.invoice.number

