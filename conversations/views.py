from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from listings.models import Listing
from .forms import ConversationMessageForm
from .models import Conversation 

@login_required
def new_conversation(request, listing_pk):
    """
    Start a new conversation about a listing.
    
    Exclude 2 cases: seller = buyer (self-messaging), and already an existing conversation about this listing
    """
    listing = get_object_or_404(Listing, pk=listing_pk)

    # Prevent self-messaging
    if listing.seller == request.user:
        return redirect('listings:detail', pk=listing_pk)

    # Reuse existing conversation, if it exists.
    conversations = Conversation.objects.filter(listing=listing).filter(members__in=[request.user.id])
    if conversations:
        return redirect('conversations:detail', pk=conversations.first().id)

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)
        if form.is_valid():
            conversation = Conversation.objects.create(listing=listing)
            conversation.members.add(request.user)
            conversation.members.add(listing.seller)
            conversation.save()

            message = form.save(commit=False)
            message.conversation = conversation
            message.created_by = request.user
            message.save()

            return redirect('listings:detail', pk=listing_pk)
    else:
        form = ConversationMessageForm()

    return render(request, 'conversations/new.html', {'form': form})


@login_required
def inbox(request):
    """
    Show user's current conversations, newest first.
    """
    conversations = Conversation.objects.filter(members__in=[request.user.id]).order_by('-modified_at')
    return render(request, 'conversations/inbox.html', {'conversations': conversations})


@login_required
def detail(request, pk):
    """
    Show selected conversation (allowing message posting)
    """
    conversation = Conversation.objects.filter(members__in=[request.user.id]).get(pk=pk)

    if request.method == 'POST':
        form = ConversationMessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = conversation
            message.created_by = request.user
            message.save()

            conversation.save()
            return redirect('conversations:detail', pk=pk)
    else:
        form = ConversationMessageForm()

    return render(request, 'conversations/detail.html', {'conversation': conversation, 'form': form})
