from django.shortcuts import render, get_object_or_404, redirect, HttpResponse, render_to_response, HttpResponseRedirect
from .models import Item, Review, User, Transactions, CartItem, ItemSold, UserProfile, Category 
from .forms import UserForm, EventForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.views.generic import View
import datetime
import decimal
# import razorpay

# rzp_test_P68ddsgPlfy2P5
# RjEhOFKOqmtKMVXomEVFwUSd

# Create your views here.

def index(request):
    items = Item.objects.all()

    loggedIn = []
    try:
        loggedIn = UserProfile.objects.get(user=request.user)
    except Exception as e:
        pass


    return render(request, 'Website/index.html', {'items': items, 'bal': loggedIn})

def browsehome(request):
    items = Item.objects.all()

    loggedIn = []
    try:
        loggedIn = UserProfile.objects.get(user=request.user)
    except Exception as e:
        pass


    return render(request, 'Website/browsehome.html', {'items': items, 'bal': loggedIn})


def item_details(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'GET':

        reviews = Review.objects.filter(product=item).order_by('-review_date')

        loggedIn = []
        try:
            loggedIn = UserProfile.objects.get(user=request.user)
        except Exception as e:
            pass

    # client = razorpay.Client(auth=("rzp_test_P68ddsgPlfy2P5", "RjEhOFKOqmtKMVXomEVFwUSd"))
    # client.set_app_details({"title" : "DigitalCoops", "version" : "1.11"})

    # DATA = {}
    # DATA['amount'] = 100
    # DATA['currency'] = "inr"
    # DATA['receipt'] = "2233322"
    # DATA['payment_capture'] = 1

    # client.order.create(data=DATA)

    # newid = "100011"
    # amount = "100"
    # client.payment.capture(newid, amount)

        return render(request, 'Website/item_details.html', {'item': item, 'reviews': reviews, 'bal': loggedIn})
    else:
        if request.user.is_authenticated:
            new_title = request.POST.get('title')
            new_content = request.POST.get('comment')
            usern = request.user.get_username()

            new_r = Review()
            new_r.title = new_title
            new_r.body = new_content
            new_r.user = User.objects.get(username=usern)
            new_r.product = item

            if new_r.title is not None:
                new_r.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))



class register(View):
    form_class = UserForm
    template_name = 'Website/register.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        already_member = True
        if form.is_valid():
            user = form.save(commit = False)
            
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.save()

            user = authenticate(username = username, password = password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('index')

        return render(request, self.template_name, {'form': form, 'already_member': already_member})


def add_to_cart(request, pk):
    product = Item.objects.get(pk=pk)

    cartItem = CartItem()
    cartItem.item = product
    cartItem.cart_present = request.user
    cartItem.save()

    return redirect('show_cart')


def remove_from_cart(request, pk):
    # product = Item.objects.get(pk=pk)

    to_remove = CartItem.objects.get(pk=pk)
    to_remove.delete()

    return redirect('show_cart')


def get_cart(request):
    cart = CartItem.objects.filter(cart_present = request.user)

    loggedIn = []
    try:
        loggedIn = UserProfile.objects.get(user=request.user)
    except Exception as e:
        pass

    total_cost = 0
    for product in cart:
        total_cost += product.item.unit_price

    return render(request, 'Website/show_cart.html', {'pay': str(total_cost), 'cart': cart, 'bal': loggedIn})


def thanks_buy(request, pk):
    loggedIn = []
    try:
        loggedIn = UserProfile.objects.get(user=request.user)
    except Exception as e:
        pass

    item = get_object_or_404(Item, pk=pk)

    item.quantity -= 1
    item.save()

    t = Transactions()
    t.transaction_id = len(Transactions.objects.all())
    t.user = request.user
    t.items_included = 1
    t.save()

    it = ItemSold()
    it.selling_id = len(ItemSold.objects.all())
    it.item = item
    it.transaction = t
    it.save()

    buyer = UserProfile.objects.get(user=request.user)
    buyer.wallet_balance -= item.unit_price
    buyer.save()

    return render(request, 'Website/thanks_buy.html', {'item': item, 'bal': loggedIn})


def thanks_cart(request, cost):
    loggedIn = []
    try:
        loggedIn = UserProfile.objects.get(user=request.user)
    except Exception as e:
        pass

    itemsPresent = CartItem.objects.filter(cart_present=request.user)

    t = Transactions()
    t.transaction_id = len(Transactions.objects.all())
    t.user = request.user
    t.items_included = len(itemsPresent)
    t.save()

    soldItems = []
    for items in itemsPresent:
        soldItems.append(Item.objects.get(pk=items.item.pk))

    for prod in soldItems:

        it = ItemSold()
        it.selling_id = len(ItemSold.objects.all())
        it.item = prod
        it.transaction = t
        it.save()

        prod.quantity -= 1
        prod.save()

    buyer = UserProfile.objects.get(user=request.user)
    buyer.wallet_balance -= float(cost)
    buyer.save()

    return render(request, 'Website/thanks_cart.html', {'items': itemsPresent, 'cost': cost, 'bal': loggedIn})


def clear_cart(request):

    CartItem.objects.filter(cart_present=request.user).delete()

    return render(request, 'Website/clear_cart.html', {})


def contact_us(request):
    return render(request, 'Website/contact_us.html', {})

def search(request):
    if request.method == 'GET': 
        sq = request.GET.get('search', None)

        items = Item.objects.filter(name__icontains=sq)

        users = User.objects.all()

        if items:
            return render(request,'Website/search_result.html', {'items':items})
        else:
            return render(request, 'Website/search_none.html', {})


def viewHistory(request):

    loggedIn = []
    try:
        loggedIn = UserProfile.objects.get(user=request.user)
    except Exception as e:
        pass

    allTrans = Transactions.objects.filter(user=request.user).order_by('transaction_date')

    # print allTrans

    trans_dict = {}
    for trans in allTrans:
        itemsInTrans = ItemSold.objects.filter(transaction=trans)
        trans_dict[trans] = itemsInTrans

    # print trans_dict

    return render(request, 'Website/viewHistory.html', {'allTrans': trans_dict, 'bal': loggedIn})


def delete_product(request, pk):
    prod = Item.objects.get(pk=pk)
    prod.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def edit_product(request, pk):
    if request.method == 'POST':
        event_form = EventForm(request.POST, request.FILES)
        if event_form.is_valid():
            item = get_object_or_404(Item, pk=pk)
            item.delete()

            new_item = event_form.save(commit=False)
            new_item.item_id = len(Item.objects.all())
            new_item.save()

        items = Item.objects.all()
        event_form = EventForm()
        return render(request, 'Website/administration.html', {'items': items, 'event_form': event_form})
    else:
        item = get_object_or_404(Item, pk=pk)
        event_form = EventForm()
        return render(request, 'Website/edit_product.html', {'item': item, 'event_form': event_form})    


def add_category(request):
    if request.method == 'POST':
        catName = request.POST['catname']

        newCat = Category()
        newCat.name = catName
        newCat.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))        


def administration(request):
    if request.method == 'POST':
        event_form = EventForm(request.POST, request.FILES)
        # print event_form 
        if event_form.is_valid():
            # print "there"
            prod = event_form.save(commit=False)
            prod.item_id = len(Item.objects.all()) + 100
            prod.save()

        # print "where"
        items = Item.objects.all()
        return render(request, 'Website/administration.html', {'event_form': event_form, 'items': items})
    else:
        items = Item.objects.all()
        event_form = EventForm()
        return render(request, 'Website/administration.html', {'event_form': event_form, 'items': items})


def sell_history(request):

    allTrans = Transactions.objects.all().order_by('-transaction_date')

    trans_dict = {}
    total = {}
    for trans in allTrans:
        itemsInTrans = ItemSold.objects.filter(transaction=trans)

        for it in itemsInTrans:
            if trans in total:
                total[trans] += it.item.unit_price
            else:
                total[trans] = it.item.unit_price   

        trans_dict[trans] = itemsInTrans

    # print total

    return render(request, 'Website/sell_history.html', {'allTrans': trans_dict, 'total': total})


def categorize(request, arg):

    if(arg == 'none'):
        items = Item.objects.all()
    else:
        items = Item.objects.filter(category__name=arg)

    users = User.objects.all()

    if items:
        return render(request,'Website/search_result.html', {'items':items})
    else:
        return render(request, 'Website/search_none.html', {})