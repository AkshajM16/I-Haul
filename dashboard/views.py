from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from listings.models import Listing

@login_required
def index(request):
    """
    Dashboard home: shows the current user's listings.
    """
    my_listings = Listing.objects.filter(seller=request.user).order_by('-created_at')
    return render(request, 'dashboard/index.html', {'listings': my_listings})