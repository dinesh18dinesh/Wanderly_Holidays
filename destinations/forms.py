from django import forms
from .models import Enquiry, NewsletterSubscriber, Review


class EnquiryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')

    class Meta:
        model = Enquiry
        fields = [
            'name', 'city', 'email', 'phone', 'whatsapp', 'destination',
            'travel_date', 'travelers', 'vacation_type', 'message'
        ]
        widgets = {
            'travel_date': forms.DateInput(attrs={'type': 'date'}),
            'message': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Tell us your preferred hotels, activities, budget or special requirements.'}),
        }


class NewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = ['email']
        widgets = {'email': forms.EmailInput(attrs={'placeholder': 'Your email address'})}


class ReviewForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault('class', 'form-control')

    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {'comment': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Tell other travellers about your experience.'})}
