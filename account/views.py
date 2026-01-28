from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from listings.models import Listing
from .forms import ProfileForm

@login_required
def profile(request):
    """
    Show the logged in user's profile along with their own listings.
    """
    my_listings = Listing.objects.filter(seller=request.user).order_by('-created_at')
    return render(request, 'account/profile.html', {
        'user_obj': request.user,
        'listings': my_listings,
    })

@login_required
def edit_profile(request):
    """
    Allow the logged in user to edit their account details via ProfileForm.
    """
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('account:profile')
    else:
        form = ProfileForm(instance=request.user)

    return render(request, 'account/edit.html', {'form': form})
