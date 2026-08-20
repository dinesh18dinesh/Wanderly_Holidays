import json
from datetime import datetime
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from destinations.models import Coupon, TravelPackage
from .forms import BookingForm, SavedTravelerForm
from .models import Booking, BookingTraveler, SavedTraveler


def _save_travelers(booking, data):
    booking.traveler_details.all().delete()
    for item in data[:booking.number_of_travelers]:
        first=(item.get('first_name') or '').strip()
        if not first: continue
        dob=None
        if item.get('date_of_birth'):
            try: dob=datetime.strptime(item['date_of_birth'],'%Y-%m-%d').date()
            except ValueError: dob=None
        BookingTraveler.objects.create(
            booking=booking, first_name=first, last_name=(item.get('last_name') or '').strip(),
            relation=item.get('relation') or 'friend', date_of_birth=dob, gender=item.get('gender') or '',
            nationality=item.get('nationality') or 'Indian', phone=(item.get('phone') or '').strip(), email=item.get('email') or '',
            passport_number=item.get('passport_number') or '', id_number=item.get('id_number') or '',
            special_needs=item.get('special_needs') or '')

@login_required
def book_package(request, slug):
    package=get_object_or_404(TravelPackage,slug=slug)
    if package.available_seats < 1:
        messages.error(request,'This package is currently sold out.'); return redirect('package_detail',slug=package.slug)
    if request.method=='POST':
        form=BookingForm(request.POST,package=package)
        if form.is_valid():
            travelers=form.cleaned_data['number_of_travelers']
            data=form.cleaned_data.get('traveler_data') or []
            base_total=package.effective_price*travelers
            coupon_code=form.cleaned_data.get('coupon_code','').strip().upper(); discount=Decimal('0.00')
            if coupon_code:
                try: coupon=Coupon.objects.get(code__iexact=coupon_code)
                except Coupon.DoesNotExist:
                    form.add_error('coupon_code','Invalid coupon code.'); return render(request,'bookings/book_package.html',{'package':package,'form':form,'saved_travelers':SavedTraveler.objects.filter(user=request.user)})
                if not coupon.is_valid():
                    form.add_error('coupon_code','This coupon is expired or inactive.'); return render(request,'bookings/book_package.html',{'package':package,'form':form,'saved_travelers':SavedTraveler.objects.filter(user=request.user)})
                discount=(base_total*Decimal(coupon.discount_percent)/Decimal('100')).quantize(Decimal('0.01'))
            total=max(Decimal('0.00'),base_total-discount)
            with transaction.atomic():
                package=TravelPackage.objects.select_for_update().get(pk=package.pk)
                if travelers>package.available_seats:
                    form.add_error('number_of_travelers',f'Only {package.available_seats} seats are available.'); return render(request,'bookings/book_package.html',{'package':package,'form':form,'saved_travelers':SavedTraveler.objects.filter(user=request.user)})
                booking=form.save(commit=False); booking.user=request.user; booking.package=package; booking.total_amount=total; booking.discount_amount=discount; booking.coupon_code=coupon_code; booking.save()
                package.available_seats-=travelers; package.save(update_fields=['available_seats'])
                _save_travelers(booking,data)
            request.session['booking_id']=booking.booking_id
            return redirect('initiate_payment')
    else:
        form=BookingForm(package=package,initial={'traveler_name':request.user.get_full_name(),'traveler_email':request.user.email})
    return render(request,'bookings/book_package.html',{'package':package,'form':form,'saved_travelers':SavedTraveler.objects.filter(user=request.user)})

@login_required
def my_bookings(request):
    status=request.GET.get('status',''); bookings=Booking.objects.filter(user=request.user).select_related('package','package__destination').prefetch_related('traveler_details')
    if status in dict(Booking.STATUS_CHOICES): bookings=bookings.filter(status=status)
    return render(request,'bookings/my_bookings.html',{'bookings':bookings,'selected_status':status})

@login_required
def edit_booking(request, booking_id):
    booking=get_object_or_404(Booking.objects.select_related('package','package__destination'),booking_id=booking_id,user=request.user)
    if booking.status not in ('pending','confirmed'):
        messages.warning(request,'This booking is no longer editable.'); return redirect('my_bookings')
    package=booking.package
    if request.method=='POST':
        form=BookingForm(request.POST,instance=booking,package=package)
        if form.is_valid():
            new_count=form.cleaned_data['number_of_travelers']; delta=new_count-booking.number_of_travelers
            if booking.payment_status and delta!=0:
                form.add_error('number_of_travelers','Traveller count cannot be changed after payment. Contact support for a refund or additional payment.')
            elif delta>package.available_seats:
                form.add_error('number_of_travelers',f'Only {package.available_seats} additional seats are available.')
            else:
                with transaction.atomic():
                    package=TravelPackage.objects.select_for_update().get(pk=package.pk)
                    if delta>package.available_seats:
                        form.add_error('number_of_travelers',f'Only {package.available_seats} additional seats are available.')
                    else:
                        updated=form.save(commit=False)
                        base=package.effective_price*new_count
                        discount=Decimal('0.00')
                        if updated.coupon_code:
                            try:
                                c=Coupon.objects.get(code__iexact=updated.coupon_code)
                                if c.is_valid(): discount=(base*Decimal(c.discount_percent)/100).quantize(Decimal('0.01'))
                            except Coupon.DoesNotExist: pass
                        updated.discount_amount=discount; updated.total_amount=max(Decimal('0.00'),base-discount); updated.save()
                        if delta: package.available_seats-=delta; package.save(update_fields=['available_seats'])
                        _save_travelers(updated,form.cleaned_data.get('traveler_data') or [])
                messages.success(request,f'Booking {booking.booking_id} updated successfully.'); return redirect('my_bookings')
    else:
        current=[{'first_name':t.first_name,'last_name':t.last_name,'relation':t.relation,'date_of_birth':t.date_of_birth.isoformat() if t.date_of_birth else '','gender':t.gender,'nationality':t.nationality,'phone':t.phone,'email':t.email,'passport_number':t.passport_number,'id_number':t.id_number,'special_needs':t.special_needs} for t in booking.traveler_details.all()]
        form=BookingForm(instance=booking,package=package,initial={'traveler_data':json.dumps(current)})
    return render(request,'bookings/edit_booking.html',{'booking':booking,'package':package,'form':form,'saved_travelers':SavedTraveler.objects.filter(user=request.user)})

@login_required
def save_traveler(request):
    if request.method!='POST': return redirect('my_bookings')
    form=SavedTravelerForm(request.POST)
    if form.is_valid():
        obj=form.save(commit=False); obj.user=request.user; obj.save(); messages.success(request,f'{obj} was saved to your traveller list.')
    else: messages.error(request,'Please correct the traveller details.')
    return redirect(request.POST.get('next') or 'my_bookings')

@login_required
def saved_travelers(request):
    travelers=SavedTraveler.objects.filter(user=request.user)
    return render(request,'bookings/saved_travelers.html',{'travelers':travelers,'form':SavedTravelerForm()})

@login_required
def traveler_data_api(request, traveler_id):
    t=get_object_or_404(SavedTraveler,pk=traveler_id,user=request.user)
    return JsonResponse({'first_name':t.first_name,'last_name':t.last_name,'relation':t.relation,'date_of_birth':t.date_of_birth.isoformat() if t.date_of_birth else '','gender':t.gender,'nationality':t.nationality,'phone':t.phone,'email':t.email,'passport_number':t.passport_number,'id_number':t.id_number})

@login_required
@transaction.atomic
def cancel_booking(request,booking_id):
    booking=get_object_or_404(Booking.objects.select_for_update(),booking_id=booking_id,user=request.user)
    if request.method!='POST': return redirect('my_bookings')
    if booking.status in ('pending','confirmed'):
        if not booking.payment_status: booking.package.available_seats+=booking.number_of_travelers; booking.package.save(update_fields=['available_seats'])
        else: booking.package.available_seats+=booking.number_of_travelers; booking.package.save(update_fields=['available_seats'])
        booking.status='cancelled'; booking.save(update_fields=['status','updated_at']); messages.success(request,f'Booking {booking.booking_id} has been cancelled.')
    else: messages.warning(request,'This booking cannot be cancelled.')
    return redirect('my_bookings')

@login_required
def download_invoice(request,booking_id):
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    from reportlab.lib.units import cm
    booking=get_object_or_404(Booking,booking_id=booking_id,user=request.user)
    response=HttpResponse(content_type='application/pdf'); response['Content-Disposition']=f'attachment; filename="invoice_{booking.booking_id}.pdf"'
    p=canvas.Canvas(response,pagesize=A4); width,height=A4; p.setFont('Helvetica-Bold',20); p.drawString(2*cm,height-2*cm,'Wanderly Travel & Holidays'); p.setFont('Helvetica',11); p.drawString(2*cm,height-2.7*cm,'Booking Invoice'); p.line(2*cm,height-3*cm,width-2*cm,height-3*cm)
    lines=[f'Invoice Date: {datetime.now().strftime("%d %B %Y")}',f'Booking ID: {booking.booking_id}',f'Customer: {booking.traveler_name or booking.user.get_full_name() or booking.user.username}',f'Email: {booking.traveler_email or booking.user.email}',f'Phone: {booking.traveler_phone}',f'Package: {booking.package.name}',f'Destination: {booking.package.destination.city}, {booking.package.destination.country}',f'Travel Date: {booking.travel_date}',f'Travellers: {booking.number_of_travelers}',f'Status: {booking.get_status_display()}',f'Payment: {"Paid" if booking.payment_status else "Unpaid"}',f'Total Amount: Rs. {booking.total_amount}','','Traveller details:']
    for t in booking.traveler_details.all(): lines.append(f'- {t.first_name} {t.last_name} ({t.get_relation_display()}) | {t.email or "—"}')
    y=height-4*cm
    for line in lines: p.drawString(2*cm,y,line[:110]); y-=0.55*cm
    p.setFont('Helvetica-Oblique',9); p.drawString(2*cm,2*cm,'Thank you for travelling with Wanderly. Have a wonderful journey!'); p.showPage(); p.save(); return response
