from datetime import date

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
import re

from .models import Profile


# ============================================================
# VALIDATORS
# ============================================================

NAME_VALIDATOR = RegexValidator(
    regex=r'^[A-Za-z]+$',
    message='Use alphabetic characters only.'
)

MOBILE_VALIDATOR = RegexValidator(
    regex=r'^\d{7,15}$',
    message='Mobile number must contain digits only (7 to 15 digits).'
)

USERNAME_VALIDATOR = RegexValidator(
    regex=r'^[A-Za-z0-9@.+_-]+$',
    message='Please use only letters, numbers and @ . + - _'
)


# ============================================================
# COUNTRY CODES
# ============================================================

COUNTRY_CODES = [
    ('+91', 'India (+91)'),
    ('+1', 'USA / Canada (+1)'),
    ('+44', 'United Kingdom (+44)'),
    ('+33', 'France (+33)'),
    ('+39', 'Italy (+39)'),
    ('+49', 'Germany (+49)'),
    ('+41', 'Switzerland (+41)'),
    ('+34', 'Spain (+34)'),
    ('+30', 'Greece (+30)'),
    ('+31', 'Netherlands (+31)'),
    ('+43', 'Austria (+43)'),
    ('+36', 'Hungary (+36)'),
    ('+351', 'Portugal (+351)'),
    ('+354', 'Iceland (+354)'),
    ('+47', 'Norway (+47)'),
    ('+385', 'Croatia (+385)'),
    ('+971', 'UAE (+971)'),
    ('+65', 'Singapore (+65)'),
    ('+60', 'Malaysia (+60)'),
    ('+66', 'Thailand (+66)'),
    ('+62', 'Indonesia (+62)'),
    ('+61', 'Australia (+61)'),
    ('+81', 'Japan (+81)'),
    ('+82', 'South Korea (+82)'),
]


# ============================================================
# COUNTRIES
# ============================================================

COUNTRIES = [
    ('India', 'India'),
    ('United Arab Emirates', 'United Arab Emirates'),
    ('United Kingdom', 'United Kingdom'),
    ('United States', 'United States'),
    ('Canada', 'Canada'),
    ('France', 'France'),
    ('Italy', 'Italy'),
    ('Germany', 'Germany'),
    ('Switzerland', 'Switzerland'),
    ('Spain', 'Spain'),
    ('Greece', 'Greece'),
    ('Netherlands', 'Netherlands'),
    ('Austria', 'Austria'),
    ('Portugal', 'Portugal'),
    ('Iceland', 'Iceland'),
    ('Norway', 'Norway'),
    ('Croatia', 'Croatia'),
    ('Singapore', 'Singapore'),
    ('Malaysia', 'Malaysia'),
    ('Thailand', 'Thailand'),
    ('Indonesia', 'Indonesia'),
    ('Australia', 'Australia'),
    ('Japan', 'Japan'),
    ('South Korea', 'South Korea'),
    ('Other', 'Other'),
]


# ============================================================
# PINCODE RULES
# ============================================================

PINCODE_RULES = {
    'India': (
        r'^[0-9]{6}$',
        6,
        'India PIN code must be exactly 6 digits.'
    ),

    'United States': (
        r'^[0-9]{5}(?:-[0-9]{4})?$',
        10,
        'US ZIP code must be 5 digits (or ZIP+4).'
    ),

    'Canada': (
        r'^[A-Za-z][0-9][A-Za-z][ -]?[0-9][A-Za-z][0-9]$',
        7,
        'Canada postal code must follow A1A 1A1 format.'
    ),

    'United Kingdom': (
        r'^[A-Za-z0-9 ]{5,8}$',
        8,
        'UK postcode must contain 5 to 8 letters/numbers.'
    ),

    'Australia': (
        r'^[0-9]{4}$',
        4,
        'Australia postcode must be exactly 4 digits.'
    ),

    'France': (
        r'^[0-9]{5}$',
        5,
        'France postal code must be exactly 5 digits.'
    ),

    'Germany': (
        r'^[0-9]{5}$',
        5,
        'Germany postal code must be exactly 5 digits.'
    ),

    'Italy': (
        r'^[0-9]{5}$',
        5,
        'Italy postal code must be exactly 5 digits.'
    ),

    'Spain': (
        r'^[0-9]{5}$',
        5,
        'Spain postal code must be exactly 5 digits.'
    ),

    'Greece': (
        r'^[0-9]{5}$',
        5,
        'Greece postal code must be exactly 5 digits.'
    ),

    'Netherlands': (
        r'^[0-9]{4} ?[A-Za-z]{2}$',
        6,
        'Netherlands postcode must follow 1234 AB format.'
    ),

    'Austria': (
        r'^[0-9]{4}$',
        4,
        'Austria postal code must be exactly 4 digits.'
    ),

    'Portugal': (
        r'^[0-9]{4}-[0-9]{3}$',
        8,
        'Portugal postal code must follow 1234-567 format.'
    ),

    'Switzerland': (
        r'^[0-9]{4}$',
        4,
        'Switzerland postal code must be exactly 4 digits.'
    ),

    'Croatia': (
        r'^[0-9]{5}$',
        5,
        'Croatia postal code must be exactly 5 digits.'
    ),

    'Singapore': (
        r'^[0-9]{6}$',
        6,
        'Singapore postal code must be exactly 6 digits.'
    ),

    'Malaysia': (
        r'^[0-9]{5}$',
        5,
        'Malaysia postcode must be exactly 5 digits.'
    ),

    'Thailand': (
        r'^[0-9]{5}$',
        5,
        'Thailand postcode must be exactly 5 digits.'
    ),

    'Indonesia': (
        r'^[0-9]{5}$',
        5,
        'Indonesia postal code must be exactly 5 digits.'
    ),

    'Japan': (
        r'^[0-9]{3}-?[0-9]{4}$',
        8,
        'Japan postal code must follow 123-4567 format.'
    ),

    'South Korea': (
        r'^[0-9]{5}$',
        5,
        'South Korea postal code must be exactly 5 digits.'
    ),

    'United Arab Emirates': (
        r'^[A-Za-z0-9 -]{1,10}$',
        10,
        'Enter a valid UAE postal/area code if applicable.'
    ),

    'Other': (
        r'^[A-Za-z0-9 -]{3,12}$',
        12,
        'Enter a valid postal code.'
    ),
}


# ============================================================
# REGISTRATION FORM
# ============================================================

class RegistrationForm(UserCreationForm):

    # --------------------------------------------------------
    # USERNAME
    # --------------------------------------------------------

    username = forms.CharField(
        max_length=150,
        min_length=3,
        required=True,
        validators=[USERNAME_VALIDATOR],
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Choose a username',
                'autocomplete': 'username',
            }
        ),
        error_messages={
            'required': 'Please enter a username.',
            'max_length': 'Username is too long.',
            'min_length': 'Username must contain at least 3 characters.',
        }
    )

    # --------------------------------------------------------
    # EMAIL
    # --------------------------------------------------------

    email = forms.EmailField(
        required=True,
        validators=[
            RegexValidator(
                r'^[A-Za-z0-9._%+-]+@gmail\.com$',
                'Please enter a valid @gmail.com email address.'
            )
        ],
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'example@gmail.com',
                'autocomplete': 'gmail',
            }
        ),
        error_messages={
            'required': 'Please enter your Gmail address.',
            'invalid': 'Please enter a valid Gmail address.',
        }
    )

    # --------------------------------------------------------
    # FIRST NAME
    # --------------------------------------------------------

    first_name = forms.CharField(
        max_length=30,
        required=True,
        validators=[NAME_VALIDATOR],
        widget=forms.TextInput(
            attrs={
                'pattern': '[A-Za-z]+',
                'title': 'Alphabetic characters only',
                'placeholder': 'First name',
                'autocomplete': 'given-name',
            }
        ),
        error_messages={
            'required': 'Please enter your first name.',
            'max_length': 'First name is too long.',
        }
    )

    # --------------------------------------------------------
    # LAST NAME
    # --------------------------------------------------------

    last_name = forms.CharField(
        max_length=30,
        required=True,
        validators=[NAME_VALIDATOR],
        widget=forms.TextInput(
            attrs={
                'pattern': '[A-Za-z]+',
                'title': 'Alphabetic characters only',
                'placeholder': 'Last name',
                'autocomplete': 'family-name',
            }
        ),
        error_messages={
            'required': 'Please enter your last name.',
            'max_length': 'Last name is too long.',
        }
    )

    # --------------------------------------------------------
    # COUNTRY CODE
    # --------------------------------------------------------

    phone_country_code = forms.ChoiceField(
        choices=COUNTRY_CODES,
        required=True,
        label='Country code',
        widget=forms.Select(
            attrs={
                'class': 'form-select'
            }
        )
    )

    # --------------------------------------------------------
    # MOBILE NUMBER
    # --------------------------------------------------------

    phone_number = forms.CharField(
        max_length=15,
        min_length=7,
        required=True,
        validators=[MOBILE_VALIDATOR],
        widget=forms.TextInput(
            attrs={
                'inputmode': 'numeric',
                'pattern': '[0-9]{7,15}',
                'maxlength': '15',
                'placeholder': '9876543210',
                'autocomplete': 'tel',
                'oninput': "this.value=this.value.replace(/[^0-9]/g,'')",
            }
        ),
        label='Mobile number',
        error_messages={
            'required': 'Please enter your mobile number.',
            'min_length': 'Mobile number must contain at least 7 digits.',
            'max_length': 'Mobile number cannot exceed 15 digits.',
        }
    )

    # --------------------------------------------------------
    # DATE OF BIRTH
    # --------------------------------------------------------

    date_of_birth = forms.DateField(
        required=False,
        input_formats=[
            '%d/%m/%Y',
            '%Y-%m-%d',
        ],
        widget=forms.TextInput(
            attrs={
                'class': 'dob-picker-input',
                'placeholder': 'DD/MM/YYYY',
                'autocomplete': 'bday',
                'readonly': 'readonly',
                'aria-haspopup': 'dialog',
                'aria-expanded': 'false',
            }
        )
    )

    # --------------------------------------------------------
    # GENDER
    # --------------------------------------------------------

    gender = forms.ChoiceField(
        required=False,
        choices=[
            ('', 'Select'),
            ('male', 'Male'),
            ('female', 'Female'),
            ('other', 'Other'),
        ]
    )

    # --------------------------------------------------------
    # ADDRESS
    # --------------------------------------------------------

    address = forms.CharField(
        required=False,
        widget=forms.Textarea(
            attrs={
                'rows': 2,
                'placeholder': 'Enter your address',
            }
        )
    )

    # --------------------------------------------------------
    # CITY
    # --------------------------------------------------------

    city = forms.CharField(
        max_length=80,
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'City',
            }
        )
    )

    # --------------------------------------------------------
    # STATE
    # --------------------------------------------------------

    state = forms.CharField(
        max_length=80,
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'State',
            }
        )
    )

    # --------------------------------------------------------
    # COUNTRY OF RESIDENCE
    # --------------------------------------------------------

    country = forms.ChoiceField(
        choices=COUNTRIES,
        required=True,
        initial='India',
        label='Country of residence'
    )

    # --------------------------------------------------------
    # PINCODE
    # --------------------------------------------------------

    pincode = forms.CharField(
        max_length=12,
        required=True,
        widget=forms.TextInput(
            attrs={
                'autocomplete': 'postal-code',
                'placeholder': 'Enter pincode',
            }
        ),
        error_messages={
            'required': 'Please enter your pincode.'
        }
    )

    # --------------------------------------------------------
    # NEWSLETTER
    # --------------------------------------------------------

    newsletter_subscribed = forms.BooleanField(
        required=False,
        initial=True
    )

    # ========================================================
    # META
    # ========================================================

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        ]

    # ========================================================
    # EMAIL VALIDATION
    # ========================================================

    def clean_email(self):
        email = self.cleaned_data['email'].strip().lower()

        if not email.endswith('@gmail.com'):
            raise forms.ValidationError(
                'Email must end with @gmail.com.'
            )

        return email

    # ========================================================
    # FIRST NAME VALIDATION
    # ========================================================

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name', '').strip()

        if not first_name:
            raise forms.ValidationError(
                'Please enter your first name.'
            )

        if not re.fullmatch(r'[A-Za-z]+', first_name):
            raise forms.ValidationError(
                'First name must contain letters only.'
            )

        return first_name

    # ========================================================
    # LAST NAME VALIDATION
    # ========================================================

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name', '').strip()

        if not last_name:
            raise forms.ValidationError(
                'Please enter your last name.'
            )

        if not re.fullmatch(r'[A-Za-z]+', last_name):
            raise forms.ValidationError(
                'Last name must contain letters only.'
            )

        return last_name

    # ========================================================
    # MOBILE VALIDATION
    # ========================================================

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number', '').strip()

        if not phone:
            raise forms.ValidationError(
                'Please enter your mobile number.'
            )

        if not phone.isdigit():
            raise forms.ValidationError(
                'Mobile number must contain digits only.'
            )

        if not 7 <= len(phone) <= 15:
            raise forms.ValidationError(
                'Mobile number must contain 7 to 15 digits.'
            )

        return phone

    # ========================================================
    # DATE OF BIRTH VALIDATION
    # ========================================================

    def clean_date_of_birth(self):
        dob = self.cleaned_data.get('date_of_birth')

        if dob:
            today = date.today()

            if dob > today:
                raise forms.ValidationError(
                    'Date of birth cannot be in the future.'
                )

            if dob.year < 1900:
                raise forms.ValidationError(
                    'Please select a valid year from 1900 onwards.'
                )

        return dob

    # ========================================================
    # COUNTRY + COUNTRY CODE VALIDATION
    # ========================================================

    def clean(self):
        cleaned = super().clean()

        country = cleaned.get('country')
        code = cleaned.get('phone_country_code')

        expected = {
            'India': '+91',
            'United States': '+1',
            'Canada': '+1',
            'United Kingdom': '+44',
            'France': '+33',
            'Italy': '+39',
            'Germany': '+49',
            'Switzerland': '+41',
            'Spain': '+34',
            'Greece': '+30',
            'Netherlands': '+31',
            'Austria': '+43',
            'Hungary': '+36',
            'Portugal': '+351',
            'Iceland': '+354',
            'Norway': '+47',
            'Croatia': '+385',
            'United Arab Emirates': '+971',
            'Singapore': '+65',
            'Malaysia': '+60',
            'Thailand': '+66',
            'Indonesia': '+62',
            'Australia': '+61',
            'Japan': '+81',
            'South Korea': '+82',
        }

        if country in expected and code:
            if code != expected[country]:
                self.add_error(
                    'phone_country_code',
                    'Please select the country code that matches your country of residence.'
                )

        return cleaned

    # ========================================================
    # PINCODE VALIDATION
    # ========================================================

    def clean_pincode(self):
        pincode = self.cleaned_data.get('pincode', '').strip()
        country = self.cleaned_data.get('country')

        rule = PINCODE_RULES.get(
            country,
            PINCODE_RULES['Other']
        )

        if not re.match(
            rule[0],
            pincode,
            re.IGNORECASE
        ):
            raise forms.ValidationError(rule[2])

        return pincode

    # ========================================================
    # SAVE USER + PROFILE
    # ========================================================

    def save(self, commit=True):
        user = super().save(commit=False)

        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()

        profile, created = Profile.objects.get_or_create(
            user=user
        )

        profile_fields = [
            'phone_country_code',
            'phone_number',
            'date_of_birth',
            'gender',
            'address',
            'city',
            'state',
            'country',
            'pincode',
            'newsletter_subscribed',
        ]

        for field in profile_fields:
            setattr(
                profile,
                field,
                self.cleaned_data.get(field)
            )

        if commit:
            profile.save()

        return user


# ============================================================
# PROFILE UPDATE FORM
# ============================================================

class ProfileUpdateForm(forms.ModelForm):

    first_name = forms.CharField(
        max_length=30,
        required=False,
        validators=[NAME_VALIDATOR]
    )

    last_name = forms.CharField(
        max_length=30,
        required=False,
        validators=[NAME_VALIDATOR]
    )

    email = forms.EmailField(
        required=False,
        validators=[
            RegexValidator(
                r'^[A-Za-z0-9._%+-]+@gmail\.com$',
                'Please enter a valid @gmail.com email address.'
            )
        ]
    )

    class Meta:
        model = Profile

        fields = [
            'phone_country_code',
            'phone_number',
            'date_of_birth',
            'gender',
            'address',
            'city',
            'state',
            'country',
            'pincode',
            'profile_picture',
            'newsletter_subscribed',
        ]

        widgets = {
            'phone_country_code': forms.Select(
                choices=COUNTRY_CODES
            ),

            'phone_number': forms.TextInput(
                attrs={
                    'inputmode': 'numeric',
                    'pattern': '[0-9]{7,15}',
                    'maxlength': '15',
                    'oninput': "this.value=this.value.replace(/[^0-9]/g,'')",
                }
            ),

            'date_of_birth': forms.DateInput(
                attrs={
                    'type': 'date',
                    'min': '1900-01-01',
                    'max': date.today().isoformat(),
                }
            ),

            'address': forms.Textarea(
                attrs={
                    'rows': 3
                }
            ),

            'country': forms.Select(
                choices=COUNTRIES
            ),
        }

    # ========================================================
    # INITIALIZATION
    # ========================================================

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs.setdefault(
                'class',
                'form-control'
            )

        self.fields['phone_number'].validators = [
            MOBILE_VALIDATOR
        ]

        self.fields['phone_number'].required = True
        self.fields['phone_country_code'].required = True
        self.fields['pincode'].required = True

    # ========================================================
    # PROFILE PINCODE VALIDATION
    # ========================================================

    def clean_pincode(self):
        pincode = self.cleaned_data.get(
            'pincode',
            ''
        ).strip()

        country = self.cleaned_data.get('country')

        rule = PINCODE_RULES.get(
            country,
            PINCODE_RULES['Other']
        )

        if not re.match(
            rule[0],
            pincode,
            re.IGNORECASE
        ):
            raise forms.ValidationError(rule[2])

        return pincode

    # ========================================================
    # PROFILE EMAIL VALIDATION
    # ========================================================

    def clean_email(self):
        email = self.cleaned_data.get(
            'email',
            ''
        ).strip().lower()

        if email and not email.endswith('@gmail.com'):
            raise forms.ValidationError(
                'Email must end with @gmail.com.'
            )

        return email