import json

from django import forms
from django.utils import timezone

from .models import Booking, BookingTraveler, SavedTraveler


class BookingForm(forms.ModelForm):

    coupon_code = forms.CharField(
        required=False,
        max_length=30
    )

    traveler_phone = forms.CharField(
        required=True,
        max_length=15,
        min_length=7,
        label='Primary phone number'
    )

    traveler_data = forms.CharField(
        required=False,
        widget=forms.HiddenInput()
    )

    class Meta:
        model = Booking

        fields = [
            'travel_date',
            'number_of_travelers',
            'traveler_name',
            'traveler_phone',
            'traveler_email',
            'coupon_code',
            'special_requests'
        ]

        widgets = {

            'travel_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'min': timezone.localdate().isoformat(),
                }
            ),

            'special_requests': forms.Textarea(
                attrs={
                    'rows': 4
                }
            ),
        }

    def __init__(self, *args, package=None, **kwargs):

        super().__init__(*args, **kwargs)

        self.package = package

        for field in self.fields.values():

            field.widget.attrs.setdefault(
                'class',
                'form-control'
            )

        if package:

            self.fields[
                'number_of_travelers'
            ].widget.attrs.update({

                'min': 1,

                'max': min(
                    package.available_seats,
                    20
                )

            })

        # Trip phone number
        self.fields[
            'traveler_phone'
        ].widget.attrs.update({

            'type': 'tel',

            'inputmode': 'numeric',

            'pattern': '[0-9]*',

            'autocomplete': 'tel',

            'placeholder':
                'Enter phone number',

        })

    def clean_travel_date(self):

        value = self.cleaned_data[
            'travel_date'
        ]

        if value < timezone.localdate():

            raise forms.ValidationError(
                'Travel date cannot be in the past.'
            )

        return value

    def clean_number_of_travelers(self):

        value = self.cleaned_data[
            'number_of_travelers'
        ]

        if (
            self.package
            and value > self.package.available_seats
        ):

            raise forms.ValidationError(
                f'Only {self.package.available_seats} '
                f'seats are available.'
            )

        if value > 20:

            raise forms.ValidationError(
                'Maximum 20 travellers can be added '
                'in one booking.'
            )

        return value

    def clean_traveler_phone(self):

        phone = self.cleaned_data.get(
            'traveler_phone',
            ''
        ).strip()

        # Only numbers
        if not phone.isdigit():

            raise forms.ValidationError(
                'Phone number must contain numbers only.'
            )

        # Prevent extremely short/long numbers
        if not 7 <= len(phone) <= 15:

            raise forms.ValidationError(
                'Please enter a valid phone number.'
            )

        return phone

    def clean_traveler_data(self):

        raw = self.cleaned_data.get(
            'traveler_data',
            ''
        )

        if not raw:

            return []

        try:

            data = json.loads(raw)

        except (TypeError, ValueError):

            raise forms.ValidationError(
                'Please check the traveller details.'
            )

        if not isinstance(data, list):

            raise forms.ValidationError(
                'Invalid traveller list.'
            )

        required_count = (
            self.cleaned_data.get(
                'number_of_travelers'
            ) or 1
        )

        if len(data) < required_count:

            raise forms.ValidationError(
                f'Please provide details for all '
                f'{required_count} travellers.'
            )

        for index, traveler in enumerate(
            data[:required_count],
            start=1
        ):

            # First name
            if not (
                traveler.get('first_name')
                or ''
            ).strip():

                raise forms.ValidationError(
                    f'Traveller {index}: '
                    f'first name is required.'
                )

            # Phone
            phone = (
                traveler.get('phone')
                or ''
            ).strip()

            if not phone:

                raise forms.ValidationError(
                    f'Traveller {index}: '
                    f'phone number is mandatory.'
                )

            if not phone.isdigit():

                raise forms.ValidationError(
                    f'Traveller {index}: '
                    f'phone number must contain '
                    f'numbers only.'
                )

            # Email
            email = (
                traveler.get('email')
                or ''
            ).strip()

            if not email:

                raise forms.ValidationError(
                    f'Traveller {index}: '
                    f'email is required.'
                )

            if not email.lower().endswith(
                '@gmail.com'
            ):

                raise forms.ValidationError(
                    f'Traveller {index}: '
                    f'email must end with @gmail.com.'
                )

        return data


class SavedTravelerForm(forms.ModelForm):

    phone = forms.CharField(
        required=True,
        max_length=30,
        label='Phone number (mandatory)'
    )

    class Meta:

        model = SavedTraveler

        fields = [
            'first_name',
            'last_name',
            'relation',
            'date_of_birth',
            'gender',
            'nationality',
            'phone',
            'email',
            'passport_number',
            'id_number'
        ]

        widgets = {

            'date_of_birth': forms.DateInput(
                attrs={
                    'type': 'date',
                    'min': '1900-01-01',
                    'max': timezone.localdate().isoformat(),
                }
            )
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for field in self.fields.values():

            field.widget.attrs.setdefault(
                'class',
                'form-control'
            )

    def clean_date_of_birth(self):

        dob = self.cleaned_data.get(
            'date_of_birth'
        )

        if dob:

            today = timezone.localdate()

            if dob > today:

                raise forms.ValidationError(
                    'Date of birth cannot be in the future.'
                )

            if dob.year < 1900:

                raise forms.ValidationError(
                    'Please enter a valid date of birth.'
                )

        return dob