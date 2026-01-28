from django.shortcuts import render, redirect
from listings.models import Category, Listing
from .forms import SignUpForm

def index(request):
    """
    Homepage that shows a small selection of available listings and all categories.
    """
    listings = Listing.objects.filter(is_sold=False).order_by('-id')[:6]
    categories = Category.objects.all()
    return render(request, 'main/index.html', {
        'categories': categories,
        'listings': listings,
    })

def signup(request):
    """
    Signup flow:
    POST: Validate fields then redirect to login
    GET: Empty form
    """
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login/')
    else:
        form = SignUpForm()
    return render(request, 'main/signup.html', {'form': form})


