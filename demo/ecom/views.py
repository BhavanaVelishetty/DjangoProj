from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Item,Order,OrderItem
from .forms import ItemForm,UserRegistrationForm,OrderForm


# View to list items
def item_list(request):
    items = Item.objects.all()
    return render(request, 'item_list.html', {'items': items})

# View to add a new item
def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('item_list')
    else:
        form = ItemForm()
    return render(request, 'add_item.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('order_view')  # Redirect to item list or dashboard
        else:
            messages.error(request, 'Invalid credentials.')
    return render(request, 'login.html')

@login_required
def order_view(request):
    if request.method == 'POST':
        items = request.POST.getlist('item')  # Get list of items
        quantities = request.POST.getlist('quantity')  # Get list of quantities

        # Create an order
        order = Order.objects.create(user=request.user)

        for item_id, quantity in zip(items, quantities):
            item = Item.objects.get(id=item_id)
            #OrderItem.objects.create(order=order, item=item, quantity=quantity)
            # Check if the item already exists in the order
            order_item, created = OrderItem.objects.get_or_create(order=order, item=item)

            # If it exists, update the quantity
            if not created:
                order_item.quantity += int(quantity)  # Increment quantity
                order_item.save()  # Save the updated quantity
            else:
                order_item.quantity = int(quantity)  # Set quantity if newly created
                order_item.save()  # Save the new order item

        return redirect('order_view')  # Redirect to see the updated order summary

    # Get all items to display in the dropdown
    items = Item.objects.all()
    # Fetch orders, ordered by creation date (latest first)
    orders = Order.objects.filter(user=request.user).order_by('-order_created_date').prefetch_related('orderitem_set')
    user_profile = request.user.userprofile  # Get the user's profile for address
    return render(request, 'order_view.html', {'items': items, 'orders': orders, 'user_profile': user_profile})

