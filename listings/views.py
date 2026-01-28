# listings/views.py
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

from .models import Category, Listing
from .forms import NewListingForm, EditListingForm

def index(request):
    """
    Browse available listings
    Accepts search via ?query=... or ?q=..., and optional ?category=<id>
    """

    # We support both 'query' and 'q' to match templates from different parts of the site
    query = request.GET.get('query', '') or request.GET.get('q', '')
    category_id = request.GET.get('category', '')

    # Only keep unsold items
    qs = Listing.objects.filter(is_sold=False)

    if category_id:
        qs = qs.filter(category_id=category_id)

    if query:
        qs = qs.filter(Q(title__icontains=query) | Q(description__icontains=query))


    # Some templates look for 'category_id', others for 'active_category', so we keep both for compatability. Can refine later.
    categories = Category.objects.all()
    ctx = {
        "listings": qs,
        "query": query,
        "categories": categories,
        "category_id": int(category_id) if category_id else 0,
        "active_category": int(category_id) if category_id else None,
    }
    return render(request, "listings/items.html", ctx)

def detail(request, pk):
    """
    Show a single listing plus a few related items from the same category.
    """
    listing = get_object_or_404(Listing, pk=pk)
    related = Listing.objects.filter(category=listing.category, is_sold=False).exclude(pk=pk)[:3]
    return render(request, "listings/detail.html", {
        "listing": listing,
        "related_listings": related,
    })

@login_required
def create(request):
    """
    Create a new listing (current user)..
    """
    if request.method == "POST":
        form = NewListingForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.seller = request.user
            obj.save()
            return redirect("listings:detail", pk=obj.pk)
    else:
        form = NewListingForm()

    return render(request, "listings/form.html", {"form": form, "title": "New listing"})

@login_required
def edit(request, pk):
    """
    Edit an existing listing. Only permitted to the seller of that particular listing.
    """
    listing = get_object_or_404(Listing, pk=pk, seller=request.user)

    if request.method == "POST":
        form = EditListingForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()
            return redirect("listings:detail", pk=listing.pk)
    else:
        form = EditListingForm(instance=listing)

    return render(request, "listings/form.html", {"form": form, "title": "Edit listing"})

@login_required
def delete(request, pk):
    """
    Delete a listing owned by the current user. 
    Currenty uses GET, will need to switch this to POST with CSRF protection for production. 
    """
    listing = get_object_or_404(Listing, pk=pk, seller=request.user)
    listing.delete()
    return redirect("listings:index")
