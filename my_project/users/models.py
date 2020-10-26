from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from core import settings
import re

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser,PermissionsMixin):
    """
    Custom User Model. 
    Required fields: Email, First name, Last name, Password
    """
    first_name = models.CharField(_('First Name'), max_length=150)
    last_name = models.CharField(_('Last Name'), max_length=150)
    email = models.EmailField(_('Email adres'), max_length=250, unique=True,
        error_messages={
            'unique':_('User with such email already exists.')
        })
    is_staff = models.BooleanField(_('Staff Status'), default=False, help_text=
        _('Designates whether user can log in into admin site'))
    is_active = models.BooleanField(_('Active'), default=True, help_text=
        _('Designates whether user should be treated as active.'
          'Unselect instead of deleting account.'))
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(_('Date joined'), default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
      
    def get_full_name(self):
        """Return user's full name separated by space"""
        return f'{self.first_name} {self.last_name}'

    def short_name(self):
        """Short name for the user"""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send email to the user"""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

def user_directory_path(instance, filename):
    pass
#    """specifies path to users' logo uploads"""
#    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
#    return 'user_{0}/{1}'.format(instance.user.id, filename)

def nip_validator(value):
    if not value.isdigit():
        raise ValidationError('Digits only')  
    match = re.match(r'^[0-9]{3}\-?[0-9]{3}\-?(?:[0-9]{2}\-[0-9]{2}|[0-9]{4})$', value)
    if match is None:
        raise ValidationError('Incorrect format')
    nip_str = value.replace('-', '') 
    if len(nip_str) != 10: 
        raise ValidationError('Must be 10-digits long')
    digits = [int(i) for i in nip_str] 
    weights = (6, 5, 7, 2, 3, 4, 5, 6, 7) 
    check_sum = sum(d * w for d, w in zip(digits, weights)) % 11 
    if check_sum != digits[9]:
        raise ValidationError('Not a valid Tax Number')

class UserCompany(models.Model):
    """
    Model representation of User's company
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(_('Company Name'), max_length=150)
    slug = models.SlugField(max_length=150, unique=True)
    nip = models.CharField(_('Tax Indentification Number'), max_length=13, validators=[nip_validator], help_text=
        _('Correct format should be "123-456-32-18" or "1234563218". Digits only.'))
    logo = models.ImageField(upload_to=user_directory_path, blank=True, default='default.jpeg')
    address = models.CharField(_('Company address'),max_length=100, help_text=
        _('Street name and building number'))
    city = models.CharField(_('City'), max_length=100)
    zip_code = models.CharField(_('Zip code'), max_length=30)
    country = models.CharField(_('Country'), max_length=100)
    bank_account = models.CharField(max_length=25, blank=True)
    position = models.CharField(_('Position within a company'), max_length=100, blank=True, help_text=
        _('Designates user\'s position withing the company structures. CEO, Main Accountant etc.'))
    
    objects = models.Manager()