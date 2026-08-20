from django import forms
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.forms import modelform_factory
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from bookings.models import Booking, BookingTraveler

from .admin_panel_registry import BADGE_MAP, SECTIONS

TEXT_WIDGET_CLASS = 'form-control'
SELECT_WIDGET_CLASS = 'form-select'
CHECK_WIDGET_CLASS = 'form-check-input'


def staff_required(view_func):
    return user_passes_test(lambda u: u.is_active and u.is_staff, login_url='/accounts/login/')(view_func)


def _style_form_fields(form):
    """Attach Bootstrap-ish CSS classes to every widget so the generic
    form template renders consistently without per-field template code."""
    for name, field in form.fields.items():
        widget = field.widget
        if isinstance(widget, forms.CheckboxInput):
            widget.attrs['class'] = f"{widget.attrs.get('class', '')} {CHECK_WIDGET_CLASS}".strip()
        elif isinstance(widget, (forms.Select, forms.SelectMultiple)):
            widget.attrs['class'] = f"{widget.attrs.get('class', '')} {SELECT_WIDGET_CLASS}".strip()
        else:
            widget.attrs['class'] = f"{widget.attrs.get('class', '')} {TEXT_WIDGET_CLASS}".strip()
        if isinstance(widget, forms.Textarea):
            widget.attrs.setdefault('rows', 4)
    return form


def _get_section(section_key):
    config = SECTIONS.get(section_key)
    if not config:
        raise Http404('Unknown admin section')
    return config


SPECIAL_ACCESSORS = {
    'traveler_name_display': lambda obj: obj.traveler_name or obj.user.username,
    'blog_image_url': lambda obj: obj.image.url if obj.image else '',
}


def _badge_class(value):
    key = value
    if isinstance(value, bool):
        key = value
    return BADGE_MAP.get(key, 'blue')


def _build_rows(config, objects):
    rows = []
    for obj in objects:
        cells = []
        for attr, label, kind in config['list_fields']:
            if attr in SPECIAL_ACCESSORS:
                value = SPECIAL_ACCESSORS[attr](obj)
            else:
                value = getattr(obj, attr, '')
            cells.append({'label': label, 'kind': kind, 'value': value, 'badge_class': _badge_class(value) if kind == 'badge' or kind == 'boolean' else ''})
        rows.append({'obj': obj, 'cells': cells})
    return rows


@staff_required
def section_list(request, section):
    config = _get_section(section)
    qs = config['model'].objects.all()
    order_by = config.get('order_by')
    if order_by:
        qs = qs.order_by(*order_by.split(','))

    query = request.GET.get('q', '').strip()
    if query and config.get('search_fields'):
        filters = Q()
        for f in config['search_fields']:
            filters |= Q(**{f'{f}__icontains': query})
        qs = qs.filter(filters)

    paginator = Paginator(qs, 12)
    page_obj = paginator.get_page(request.GET.get('page'))
    rows = _build_rows(config, page_obj.object_list)

    context = {
        'section': section,
        'config': config,
        'page_obj': page_obj,
        'rows': rows,
        'query': query,
        'active': section,
        'total_count': qs.count(),
    }
    return render(request, 'admin_panel/list.html', context)


@staff_required
def section_add(request, section):
    config = _get_section(section)
    FormClass = modelform_factory(config['model'], fields=config['form_fields'])
    if request.method == 'POST':
        form = _style_form_fields(FormClass(request.POST, request.FILES))
        if form.is_valid():
            new_obj = form.save()
            messages.success(request, f"{config['singular']} created successfully.")
            if section == 'destinations':
                messages.info(request, f'Now add a package for {new_obj.name}.')
                return redirect(f"{reverse('admin_section_add', kwargs={'section': 'packages'})}?destination={new_obj.pk}")
            return redirect('admin_section_list', section=section)
    else:
        initial = {}
        if section == 'packages' and request.GET.get('destination'):
            initial['destination'] = request.GET.get('destination')
        form = _style_form_fields(FormClass(initial=initial))
    context = {'section': section, 'config': config, 'form': form, 'active': section, 'mode': 'add'}
    return render(request, 'admin_panel/form.html', context)


@staff_required
def section_edit(request, section, pk):
    config = _get_section(section)
    obj = get_object_or_404(config['model'], pk=pk)
    FormClass = modelform_factory(config['model'], fields=config['form_fields'])
    if request.method == 'POST':
        form = _style_form_fields(FormClass(request.POST, request.FILES, instance=obj))
        if form.is_valid():
            form.save()
            messages.success(request, f"{config['singular']} updated successfully.")
            return redirect('admin_section_list', section=section)
    else:
        form = _style_form_fields(FormClass(instance=obj))
    context = {'section': section, 'config': config, 'form': form, 'obj': obj, 'active': section, 'mode': 'edit'}
    return render(request, 'admin_panel/form.html', context)


@staff_required
def section_delete(request, section, pk):
    config = _get_section(section)
    obj = get_object_or_404(config['model'], pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, f"{config['singular']} deleted.")
    return redirect('admin_section_list', section=section)


# ---------------------------------------------------------------------------
# Users (auth.User) - special-cased: username/password handling differs from
# the generic ModelForm flow above.
# ---------------------------------------------------------------------------

class AdminUserCreateForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, min_length=6)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput, min_length=6)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active']

    def clean(self):
        cleaned = super().clean()
        p1, p2 = cleaned.get('password1'), cleaned.get('password2')
        if p1 and p2 and p1 != p2:
            raise forms.ValidationError('Passwords do not match.')
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class AdminUserEditForm(forms.ModelForm):
    new_password = forms.CharField(
        label='New Password', widget=forms.PasswordInput, required=False, min_length=6,
        help_text='Leave blank to keep the current password.'
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active']

    def save(self, commit=True):
        user = super().save(commit=False)
        new_password = self.cleaned_data.get('new_password')
        if new_password:
            user.set_password(new_password)
        if commit:
            user.save()
        return user


@staff_required
def user_list(request):
    qs = User.objects.all().order_by('-date_joined')
    query = request.GET.get('q', '').strip()
    if query:
        qs = qs.filter(Q(username__icontains=query) | Q(email__icontains=query) | Q(first_name__icontains=query) | Q(last_name__icontains=query))
    paginator = Paginator(qs, 12)
    page_obj = paginator.get_page(request.GET.get('page'))
    context = {'page_obj': page_obj, 'query': query, 'active': 'users', 'total_count': qs.count()}
    return render(request, 'admin_panel/user_list.html', context)


@staff_required
def user_add(request):
    if request.method == 'POST':
        form = _style_form_fields(AdminUserCreateForm(request.POST))
        if form.is_valid():
            form.save()
            messages.success(request, 'User created successfully.')
            return redirect('admin_users_list')
    else:
        form = _style_form_fields(AdminUserCreateForm())
    return render(request, 'admin_panel/user_form.html', {'form': form, 'active': 'users', 'mode': 'add'})


@staff_required
def user_edit(request, pk):
    obj = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        form = _style_form_fields(AdminUserEditForm(request.POST, instance=obj))
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully.')
            return redirect('admin_users_list')
    else:
        form = _style_form_fields(AdminUserEditForm(instance=obj))
    return render(request, 'admin_panel/user_form.html', {'form': form, 'obj': obj, 'active': 'users', 'mode': 'edit'})


@staff_required
def user_delete(request, pk):
    obj = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        if obj.pk == request.user.pk:
            messages.error(request, "You can't delete your own account while logged in.")
        else:
            obj.delete()
            messages.success(request, 'User deleted.')
    return redirect('admin_users_list')


# ---------------------------------------------------------------------------
# Booking travelers - nested CRUD under a single booking.
# ---------------------------------------------------------------------------

TRAVELER_FIELDS = [
    'first_name', 'last_name', 'relation', 'date_of_birth', 'gender', 'nationality',
    'phone', 'email', 'passport_number', 'id_number', 'special_needs',
]


@staff_required
def traveler_list(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    travelers = booking.traveler_details.all()
    return render(request, 'admin_panel/traveler_list.html', {'booking': booking, 'travelers': travelers, 'active': 'bookings'})


@staff_required
def traveler_add(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    FormClass = modelform_factory(BookingTraveler, fields=TRAVELER_FIELDS)
    if request.method == 'POST':
        form = _style_form_fields(FormClass(request.POST))
        if form.is_valid():
            traveler = form.save(commit=False)
            traveler.booking = booking
            traveler.save()
            messages.success(request, 'Traveler added successfully.')
            return redirect('admin_travelers_list', pk=booking.pk)
    else:
        form = _style_form_fields(FormClass())
    return render(request, 'admin_panel/traveler_form.html', {'form': form, 'booking': booking, 'active': 'bookings', 'mode': 'add'})


@staff_required
def traveler_edit(request, booking_pk, pk):
    booking = get_object_or_404(Booking, pk=booking_pk)
    traveler = get_object_or_404(BookingTraveler, pk=pk, booking=booking)
    FormClass = modelform_factory(BookingTraveler, fields=TRAVELER_FIELDS)
    if request.method == 'POST':
        form = _style_form_fields(FormClass(request.POST, instance=traveler))
        if form.is_valid():
            form.save()
            messages.success(request, 'Traveler updated successfully.')
            return redirect('admin_travelers_list', pk=booking.pk)
    else:
        form = _style_form_fields(FormClass(instance=traveler))
    return render(request, 'admin_panel/traveler_form.html', {'form': form, 'booking': booking, 'traveler': traveler, 'active': 'bookings', 'mode': 'edit'})


@staff_required
def traveler_delete(request, booking_pk, pk):
    booking = get_object_or_404(Booking, pk=booking_pk)
    traveler = get_object_or_404(BookingTraveler, pk=pk, booking=booking)
    if request.method == 'POST':
        traveler.delete()
        messages.success(request, 'Traveler removed.')
    return redirect('admin_travelers_list', pk=booking.pk)
