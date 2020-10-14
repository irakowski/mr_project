from django.core.exceptions import ValidationError
#Custom Validators

def nip_validator(nip_str):
    nip_str = nip_str.replace('-', '') 
    if len(nip_str) != 10 or not nip_str.isdigit():  
        raise ValidationError("Nieprawidowa długość NIPu")
    digits = [int(i) for i in nip_str] 
    weights = (6, 5, 7, 2, 3, 4, 5, 6, 7) 
    check_sum = sum(d * w for d, w in zip(digits, weights)) % 11 
    if check_sum != digits[9]:
        raise ValidationError("Niepoprawny numer NIPu")

