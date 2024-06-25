from django.core.exceptions import ValidationError

def validate_max_size(file):
    print("Invoking Validator")
    max_size_kb = 50 * 1024 # kb
    if file.size > max_size_kb:
         raise ValidationError(f'the max of kb is {max_size_kb / 1024}kb!')