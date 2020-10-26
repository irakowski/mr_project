#from django import forms
#from django.forms import ModelForm, inlineformset_factory, formset_factory
#from .models import Invoice, InvoiceItem, Product, Customer
#from django.contrib.auth.models import User
#from django.contrib.auth.forms import UserCreationForm
#
#
#class RegistrationForm(UserCreationForm):
#    class Meta:
#        model = User
#        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
#
#
#class SearchForm(forms.Form):
#    search_query = forms.CharField(max_length=150)
#
#
#class InvoiceForm(ModelForm):
#    class Meta:
#        model = Invoice
#        exclude = ('users_company', 'products', 'total_net_amount', 'total_gross_amount', 'total_vat_amount')
#        widgets = {'invoice_type': forms.HiddenInput()}
#
#
#class InvoiceItemForm(ModelForm):
#    class Meta:
#        model = InvoiceItem
#        exclude = ()
#
#InvoiceItemFormSet = inlineformset_factory(Invoice, 
#                                InvoiceItem, 
#                                fields=('product','product_quantity','vat_fee'), 
#                                widgets={'product': forms.Select(attrs={'class': 'form-control'})},
#                                extra=3)
#
##possibly better option to override formset.save() and call it in a view
##class InvoiceItemInlineFormSet(BaseInlineFormSet):
##    def save(self):
##        super().save()
##        # example custom validation across forms in the formset
##        for form in self.forms:
##            # your custom formset validation
#