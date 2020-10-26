from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect, HttpResponse
from django.template.loader import get_template
from django.views import View
from django.views.generic import TemplateView, DetailView, ListView, CreateView, \
    UpdateView, DeleteView, FormView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login
from django.utils import timezone
from django.urls import reverse_lazy
from django.db.models import Q

# Create your views here.
#from .models import Company, Customer, InvoiceItem, Invoice, Product
#from .forms import RegistrationForm, InvoiceItemFormSet, InvoiceItemForm, \
##    InvoiceForm, SearchForm
#
#
#class LandingPage(TemplateView):
#    """
#    Starting page of the website
#    """
#    
#    template_name = 'inv/landing_page.html'
#
#
#class RegistrationView(SuccessMessageMixin, FormView):
#    """
#    Displays User Registration Form that allows to save&register new users.
#    """
#    template_name = 'registration/registration_form.html'
#    form_class = RegistrationForm
#    success_message = "Dziękujęmy za rejestrację. Prosimy o wypelnienie danych firmy,"
#    success_url = reverse_lazy('create-company-profile')
#
#    def form_valid(self, form):
#        """
#        Security check complete. Create and Log the user in.
#        """
#        user = form.save()
#        username = form.cleaned_data['username']
#        password = form.cleaned_data['password1']
#        
#        user = authenticate(username=username, password=password)
#        login(self.request, user)
#        return HttpResponseRedirect(self.get_success_url())
#
#
#class CreateCompanyProfile(LoginRequiredMixin, SuccessMessageMixin, CreateView):
#    """
#    Creates Company profile for the current user and sets current user to the newly created 
#    company instance
#    """
#    model = Company
#    fields =('name', 'logo', 'nip', 'address', 'city', 'zip_code', 'country', 
#            'bank_account', 'position' )
#    login_url = 'login'
#    success_url = reverse_lazy('main')
#    success_message = "Profil firmy utworzono pomyślnie!"
#
#    def form_valid(self, form):
#        """
#        Sets current user to his company and creates company
#        """
#        self.object = form.save(commit=False)
#        self.object.user_id = self.request.user.id
#        self.object.save()
#        return super().form_valid(form)
#
#
#class Main(LoginRequiredMixin, TemplateView):
#    """
#    Main page of the Dashboard
#    """
#    def get(self, request):
#        return render(request, 'inv/main-dashboard.html')
#
#
#class CompanyProfileDetail(LoginRequiredMixin, DetailView):
#    """
#    Displays company profile
#    """
#    model = Company
#    template_name = 'inv/company_detail.html'
#
#    from django.utils import timezone
#    def get_context_data(self, **kwargs):
#        """
#        Returns context for the customers list view
#        """
#        context = super().get_context_data(**kwargs)
#        current_month = timezone.now().month
#        invoices = Invoice.objects.filter(users_company=self.request.user.company).filter(date_issued__month=current_month)
#        context['invoices'] = invoices
#        return context
#
#class UpdateCompanyProfile(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
#    """
#    Updates company profile
#    """
#    model = Company
#    fields =('name', 'logo', 'nip', 'address', 'city', 'zip_code', 'country', 
#            'bank_account', 'position' )
#    template_name_suffix = '_update'
#    success_message = "Profil firmy został zmieniony"
#    success_url = reverse_lazy('main')
#
#                                 ##SITE CONTENT##
#######################################CLIENTS#######################################################
#class AddCustomer(LoginRequiredMixin, SuccessMessageMixin, CreateView):
#    """
#    View for creating user's company customers
#    """
#    model = Customer
#    fields = ('customer_type', 'name', 'nip', 'address', 'city', 'zip_code','country',
#              'bank_account', 'regon', 'krs', 'contact', 'email', 'webpage', 'representation')
#    success_url = reverse_lazy('customers')
#    login_url = 'login'
#    success_message = 'Dodano pomyślnie'
#
#    def form_valid(self, form):
#        """
#        Links added customer with user company
#        """
#        self.object = form.save(commit=False)
#        self.object.user = self.request.user.company
#        self.object.save()
#        return super().form_valid(form)
#
#
#class CustomerList(LoginRequiredMixin, ListView):
#    """
#    Displays Customers of the logged user company
#    """
#    model = Customer
#    login_url = 'login'
#    paginate_by = 10
#
#    def get_queryset(self):
#        """
#        Returns customers that belong to the current user
#        """
#        queryset = self.model.objects.filter(user=self.request.user.company).order_by('-id')
#        return queryset
#    
#    def get_context_data(self, **kwargs):
#        """
#        Returns context for the customers list view
#        """
#        context = super().get_context_data(**kwargs)
#        customers = self.get_queryset()
#        context['customers'] = customers
#        return context
#
#
#class EditCustomer(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
#    """
#    Updates customers information
#    """
#    model = Customer
#    fields = ('customer_type', 'name', 'nip', 'address', 'city', 'zip_code','country',
#              'bank_account', 'regon', 'krs', 'contact', 'email', 'webpage', 'representation')
#    template_name_suffix = '_edit'
#    success_url = reverse_lazy('customers')
#    login_url = 'login'
#    success_message = "Dane Klienta zaktualizowano pomyślnie"
#
#    def get_queryset(self, *args, **kwargs):
#        queryset = super().get_queryset(*args, **kwargs)
#        if not self.request.user.is_superuser:
#            queryset = self.model.objects.filter(user=self.request.user.company)
#        return queryset
#
#
#class DeleteCustomer(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
#    """
#    Deletes customer if customer not linked to invoice
#    Raises protected otherwise and displays message to the user
#    """
#    model = Customer
#    login_url = 'login'
#    success_url = reverse_lazy('customers')
#    success_message = 'Usunęto pomyślnie'
#
#    def get_queryset(self, *args, **kwargs):
#        """
#        Returns only customers of the current user
#        """
#        queryset = super().get_queryset(*args, **kwargs)
#        if not self.request.user.is_superuser:
#            queryset = self.model.objects.filter(user=self.request.user.company)
#        return queryset
#
#    def post(self, request, *args, **kwargs):
#        """
#        Catches protectedError and redirect to the template with information for the user
#        """
#        try:
#            return self.delete(request, *args, **kwargs)
#        except ProtectedError:
#            return render(request, "inv/protected_item.html")
#
#
#class CustomerDetails(LoginRequiredMixin, DetailView):
#    """
#    Displays customer Details
#    """
#    model = Customer
#
#    def get_queryset(self, *args, **kwargs):
#        """
#        Filters customers for account
#        """
#        queryset = super().get_queryset(*args, **kwargs)
#        if not self.request.user.is_superuser:
#            queryset = self.model.objects.filter(user=self.request.user.company)
#        return queryset
#    
#    def get_context_data(self,**kwargs):
#        """
#        Additional context displaying customers's invoices
#        """
#        context = super().get_context_data(**kwargs)
#        self.object = self.get_object()
#        context['invoices'] = Invoice.objects.filter(customer=self.object)
#        return context
#
#############################################PRODUCTS###############################################
#class AddProduct(LoginRequiredMixin, SuccessMessageMixin, CreateView):
#    """
#    Adds product and links added product to the user
#    """
#    model = Product
#    fields = ('name', 'description', 'serial_number', 'photo', 'manufacturer',
#    'price_net', 'available', 'stock')
#    login_url = 'login'
#    success_message = 'Produkt dodano pomyślnie'
#
#    def get_success_url(self):
#        """
#        Redirects to detail view for newly created product
#        """
#        return reverse_lazy('product-detail', kwargs={'pk': self.object.pk})
#
#    def form_valid(self, form):
#        """
#        Links added product with user
#        """
#        self.object = form.save(commit=False)
#        self.object.user = self.request.user
#        self.object.save()
#        return super().form_valid(form)
#
#
#class ProductList(LoginRequiredMixin, ListView):
#    """
#    Displays user's products
#    """
#    model = Product
#    login_url = 'login'
#    paginate_by = 10
#
#    def get_queryset(self):
#        """
#        Returns Products of the current user
#        """
#        #queryset = super().get_queryset(*args, **kwargs)
#        queryset = self.model.objects.filter(user=self.request.user).order_by('-id')
#        return queryset
#    
#    def get_context_data(self, **kwargs):
#        """
#        Returns context for the list view
#        """
#        context = super().get_context_data(**kwargs)
#        products = self.get_queryset()
#        context['products'] = products
#        return context
#
#
#class ProductDetail(LoginRequiredMixin, DetailView):
#    """
#    Displays products of the user
#    """
#    model = Product
#    login_url = 'login'
#    
#    def get_queryset(self, *args, **kwargs):
#        queryset = super().get_queryset(*args, **kwargs)
#        if not self.request.user.is_superuser:
#            queryset = self.model.objects.filter(user=self.request.user)
#        return queryset
#
#
#class EditProduct(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
#    """
#    Editing available products
#    """
#    model = Product
#    template_name_suffix = '_edit'
#    fields = ('name', 'description', 'serial_number', 'photo', 'manufacturer',
#    'price_net', 'available', 'stock')
#    success_message = 'Produkt zaktualizowano pomyślnie'
#    login_url = 'login'
#
#    def get_queryset(self, *args, **kwargs):
#        queryset = super().get_queryset(*args, **kwargs)
#        if not self.request.user.is_superuser:
#            queryset = self.model.objects.filter(user=self.request.user)
#        return queryset
#
#    def get_success_url(self):
#        """
#        Redirects to detail view for edited product
#        """
#        return reverse_lazy('product-detail', kwargs={'pk': self.kwargs['pk']})
#
#
#class DeleteProduct(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
#    """
#    Deletes product if product not linked to invoice
#    Raises protected otherwise and displays message to the user
#    """
#    model = Product
#    success_url = reverse_lazy('product-list')
#    success_message = "Usunięto pomyślnie"
#    login_url = 'login'
#
#    def get_queryset(self, *args, **kwargs):
#        queryset = super().get_queryset(*args, **kwargs)
#        if not self.request.user.is_superuser:
#            queryset = self.model.objects.filter(user=self.request.user)
#        return queryset
#
#    def post(self, request, *args, **kwargs):
#        """
#        Catches protectedError and redirect to the template with information for the user
#        """
#        try:
#            return self.delete(request, *args, **kwargs)
#        except ProtectedError:
#            return render(request, "inv/protected_item.html")
#####################################INVOICE##########################################################
#
#class CreatePreOrderInvoice(LoginRequiredMixin, SuccessMessageMixin, CreateView):
#    """
#    CREATES INVOICE TYPE'Pro-forma' 
#    """
#    model = Invoice
#    template_name = 'inv/pre_order_invoice_form.html'
#    form_class = InvoiceForm
#    success_url = reverse_lazy('invoices')
#    login_url = 'login'
#    success_message = 'Fakturę zapisano' #for some reason not called?!?
#
#    def get(self, request, *args, **kwargs):
#        self.object = None
#        form_class = self.get_form_class()
#        form = self.get_form(form_class)
#        form.fields["customer"].queryset = Customer.objects.filter(user=self.request.user.company)
#        invoice_item_form = InvoiceItemFormSet()
#        for f in invoice_item_form:
#            f.fields['product'].queryset = Product.objects.filter(user=self.request.user)
#        return self.render_to_response(self.get_context_data(
#                                       form=form, 
#                                       invoice_item_form=invoice_item_form))
#
#    def post(self, request, *args, **kwargs):
#        """
#        Handles POST requests, instantiating a form instance and its inline
#        formsets with the passed POST variables and then checking them for
#        validity.
#        """
#        self.object = None
#        form_class = self.get_form_class()
#        form = self.get_form(form_class)
#
#        invoice_item_form = InvoiceItemFormSet(self.request.POST)
#        if form.is_valid() and invoice_item_form.is_valid():
#            #print(form.cleaned_data, invoice_item_form.cleaned_data)
#            return self.form_valid(form, invoice_item_form)
#        else:
#            #print(form.errors, invoice_item_form.errors)
#            return self.form_invalid(form, invoice_item_form)
#
#    def form_valid(self, form, invoice_item_form):
#        """
#        Called if all forms are valid. Creates Invoice instance along with the
#        associated InvoiceItem instances then redirects to success url
#        Args:
#            form: Invoice Form
#            invoice_item_form: Invoice Item Form
#
#        Returns: an HttpResponse to success url
#        """
#        self.object = form.save(commit=False)
#        self.object.total_gross_amount = 0
#        self.object.total_net_amount = 0
#        self.object.total_vat_amount = 0
#        self.object.users_company = self.request.user.company
#        self.object = form.save()
#        invoice_item_form.instance = self.object
#        invoice_item_form.save(commit=False)
#        for item in invoice_item_form:
#            if item.cleaned_data["DELETE"] == True:
#                continue ## a bit hacky but idk how to properly do this
#            else:
#                data = item.cleaned_data
#                product = data.get('product')
#                product_quantity = data.get('product_quantity')
#                vat_fee = data.get('vat_fee')
#                total_net = (product.price_net * product_quantity)
#                total_vat = (total_net * float(vat_fee))
#                total_per_products = (total_vat + total_net)
#                self.object.total_net_amount = self.object.total_net_amount + total_net
#                self.object.total_gross_amount = total_per_products + self.object.total_gross_amount
#                self.object.total_vat_amount = total_vat + self.object.total_vat_amount
#                self.object.save(update_fields=['total_net_amount', 'total_gross_amount','total_vat_amount'])
#                InvoiceItem.objects.create(product=product, product_quantity=product_quantity, invoice=self.object,vat_fee=vat_fee,
#                total_per_products=total_per_products, total_net=total_net, total_vat=total_vat)
#            
#        return HttpResponseRedirect(self.get_success_url())
#
#    def form_invalid(self, form, invoice_item_form):
#        """
#        Called if a form is invalid. Re-renders the context data with the
#        data-filled forms and errors.
#
#        Args:
#            form: Invoice Form
#            invoice_item_form: Invoice Item Form
#        """
#        return self.render_to_response(
#                 self.get_context_data(form=form,
#                                       invoice_item_form=invoice_item_form
#                                       )
#        )
#
#class CreateVATinvoice(CreatePreOrderInvoice):
#    """CREATES INVOICE WITH TYPE 'VAT'"""
#
#    template_name = 'inv/invoice_form.html'
#
#
#
#class InvoiceList(LoginRequiredMixin, ListView):
#    """Displays invoices belonging to logged in user"""
#    model = Invoice
#    paginate_by = 10
#    login_url = 'login'
#
#    def get_queryset(self, *args, **kwargs):
#        queryset = super().get_queryset(*args, **kwargs)
#        if not self.request.user.is_superuser:
#            queryset = self.model.objects.filter(users_company=self.request.user.company)
#        return queryset
#
#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        context['invoices'] = Invoice.objects.filter(users_company=self.request.user.company)
#        return context
#
#
#class InvoiceDetail(LoginRequiredMixin, DetailView):
#    """Details of invoice"""
#    model = Invoice
#    template_name = 'inv/invoice_detail.html'
#
#    def get_queryset(self, *args, **kwargs):
#        queryset = super().get_queryset(*args, **kwargs)
#        if not self.request.user.is_superuser:
#            queryset = self.model.objects.filter(users_company=self.request.user.company)
#        return queryset
#
#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        context['invoice_items'] = InvoiceItem.objects.filter(invoice=self.object)
#        #items_23 = InvoiceItem.objects.filter(invoice=last_inv).values('vat_fee').filter(vat_fee=0.23)
#        #items_23.aggregate(Sum('total_net')) //{'total_net__sum': 4898.0}
#        #items_23.aggregate(Sum('total_vat')) //{'total_vat__sum': 1126.54}
#        #items_23.aggregate(Sum('total_per_products'))//{'total_per_products__sum': 6024.54}
#        return context
#
#class InvoiceUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
#
#    """UPDATES INVOICE"""
#    model = Invoice
#    template_name = 'inv/invoice_update_form.html'
#    form_class = InvoiceForm
#    success_message = "Zaktualizowano pomyślnie"
#
#    def get_object(self, queryset=None):
#        obj = super(InvoiceUpdateView, self).get_object()
#        return obj
#
#    def get_queryset(self, *args, **kwargs):
#        queryset = super().get_queryset(*args, **kwargs)
#        if not self.request.user.is_superuser:
#            queryset = self.model.objects.filter(users_company=self.request.user.company)
#        return queryset
#
#    
#    def get(self, request, *args, **kwargs):
#        """
#        Handles GET requests and instantiates blank versions of the form
#        and its inline formsets.
#        """
#        self.object = self.get_object()
#        form = InvoiceForm(instance=self.object)
#        form.fields["customer"].queryset = Customer.objects.filter(user=self.request.user.company)
#        invoice_item_form = InvoiceItemFormSet(instance=self.object)
#        for f in invoice_item_form:
#            f.fields['product'].queryset = Product.objects.filter(user=self.request.user)
#        return self.render_to_response(self.get_context_data(
#                                       form=form, 
#                                       invoice_item_form=invoice_item_form))
#    
#    def get_success_url(self):
#        return reverse_lazy('invoice-detail', kwargs={'pk': self.kwargs['pk']})
#
#    def post(self, request, *args, **kwargs):
#        """
#        Handles POST requests, instantiating a form instance and its inline
#        formsets with the passed POST variables and then checking them for
#        validity.
#        """
#        self.object = self.get_object()
#        form = InvoiceForm(self.request.POST, instance=self.object)
#        invoice_item_form = InvoiceItemFormSet(self.request.POST,
#                                               instance=self.object)
#        if form.is_valid() and invoice_item_form.is_valid():
#            #print(form.cleaned_data, invoice_item_form.cleaned_data)
#            return self.form_valid(form, invoice_item_form)
#        else:
#            #print(form.errors, invoice_item_form.errors)
#            return self.form_invalid(form, invoice_item_form)
#            
#    def form_valid(self, form, invoice_item_form):
#
#        self.object = form.save(commit=False)
#        #reinstalizing the total amount to 0
#        self.object.total_gross_amount = 0
#        # same to total_net and vat
#        self.object.total_net_amount = 0
#        self.object.total_vat_amount = 0
#        #saving invoice instance
#        self.object.save()
#        self.object = form.save()
#        invoice_item_form.instance = self.object
#        invoice_item_form.save(commit=False)
#        for item in invoice_item_form:
#            if item.cleaned_data["DELETE"] == True:
#                continue ## a bit hacky but idk how to properly do this
#            else:
#                data = item.cleaned_data
#                product = data.get('product')
#                product_quantity = data.get('product_quantity')
#                vat_fee = data.get('vat_fee')
#                total_net = product.price_net * int(product_quantity)
#                total_vat = total_net * float(vat_fee)
#                total_per_products = (total_net + total_vat)
#                obj = item.save(commit=False)               
#                obj.invoice = self.object
#                obj.product = product
#                obj.product_quantity = product_quantity
#                obj.vat_fee = vat_fee
#                obj.total_net = total_net
#                obj.total_vat = total_vat
#                obj.total_per_products = total_per_products
#                obj.save()
#                #assigning new values to the edited invoice
#                self.object.total_gross_amount = total_per_products + self.object.total_gross_amount
#                self.object.total_net_amount = total_net + self.object.total_net_amount
#                self.object.total_vat_amount= total_vat +self.object.total_vat_amount
#                self.object.save(update_fields=['total_net_amount', 'total_gross_amount', 'total_vat_amount' ])
#        return HttpResponseRedirect(self.get_success_url())
#
#    def form_invalid(self, form, invoice_item_form):
#        self.object = self.get_object()
#        return self.render_to_response(self.get_context_data())
#
#class DeleteInvoice(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
#    """
#    Deletes invoice
#    """
#    model = Invoice
#    success_url = reverse_lazy('invoices')
#    success_message = "Usunięto pomyślnie"
#    login_url = 'login'
#
#########################SEARCH
#class SearchView(LoginRequiredMixin, ListView):
#    """Search by 
#        -client NIP and name
#        -number of invoice
#        ##T search by invoice_date
#    """
#    template_name = 'inv/search_result.html'
#    login_url = 'login'
#    form_class = SearchForm
#
#    def get_queryset(self):
#        query = self.request.GET.get('q')
#        return query
#
#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        query = self.get_queryset()
#        context['customers'] = Customer.objects.filter(user=self.request.user.company).filter(Q(nip__icontains=query) | Q(name__icontains=query))
#        context['invoices'] = Invoice.objects.filter(users_company=self.request.user.company).filter(number__icontains=query)
#        return context  
#
####################################################PDF
#from .render import Render
#
#class Pdf(View):
#
#    def get(self, request, pk):
#        invoice = Invoice.objects.get(pk=pk)
#        invoice_items = InvoiceItem.objects.filter(invoice=invoice)
#        params = {
#            'invoice': invoice,
#            'invoice_items': invoice_items,
#            'user': self.request.user,
#        }
#        return Render.render('pdf/test.html', params)
#
#