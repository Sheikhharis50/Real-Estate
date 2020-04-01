from django.shortcuts import render, redirect
from .models import Contact
from django.contrib import messages
from django.core.mail import send_mail

def contact(request):
    if request.method == 'POST':
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']

        # check if user already made the Inquiry
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.all().filter(
                listing_id=listing_id,user_id=user_id)
            if has_contacted:
                messages.error(
                    request, "You have already made the Inquiry of this listing")
                return redirect('/listings/'+listing_id)

        contact = Contact(listing=listing, listing_id=listing_id,
                          name=name, email=email, message=message,
                          phone=phone, user_id=user_id)
        contact.save()

        # Send mail
        # send_mail(
        #     'Property Listing Inquiry',
        #     'There has been an Inquiry for '+ listing + ". Sign into the admin panel for more info",
        #     'cuteharry50@gmail.com',
        #     [realtor_email, 'cuteharry50@gmail.com'],
        #     fail_silently=False
        # )

        messages.success(request, "Your request is submitted, realtor will contact you soon")
        return redirect('/listings/'+listing_id)
