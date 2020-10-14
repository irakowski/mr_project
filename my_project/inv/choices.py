"""Different Choices for models"""

#invoice.invoice_type
PRO_FORMA = 'Pro-Forma'
VAT = 'VAT'
KOREKTA = 'Korygująca'
INVOICE_TYPE = (
    (PRO_FORMA, 'Pro-Forma'),
    (VAT, 'VAT'),
    (KOREKTA, 'Korygująca'),
)

#invoice_item.tax_fee
VAT_CHOICES = (
    (0.23, '23%'),
    (0.08, '8%'),
    (0.05, '5%'),
    (0.00, '0%')
)

#invoice.payment_option
GOTOWKA = 'Gotowka'
PRZELEW = 'Przelew'
PAYMENT_OPTIONS = (
    (GOTOWKA, 'Gotowka'), 
    (PRZELEW, 'Przelew')

)
#client.client_type
INDIVIDUAL = 'Indywidualny'
BUSINESS = 'Biznesowy'
CUSTOMER_TYPE_CHOICES = (
    (INDIVIDUAL, 'Indywidualny'),
    (BUSINESS, 'Biznesowy')
)