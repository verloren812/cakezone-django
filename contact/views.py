from django.contrib import messages
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _

from .forms import ContactMessageForm
from .models import ContactInfo


def index(request):
    """Contact Us page: the contact information and the feedback form."""
    if request.method == "POST":
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("Thank you! We have received your message."))
            return redirect("contact:index")
    else:
        form = ContactMessageForm()

    context = {
        "contact_info": ContactInfo.objects.filter(is_active=True).first(),
        "form": form,
    }
    return render(request, "contact/contact_us.html", context)
