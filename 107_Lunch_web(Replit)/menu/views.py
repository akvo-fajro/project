from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,Permission
from django.http import Http404

# import self define models and form
from .models import Food,Order
from .forms import FoodCreateForm,FoodChangeForm,OrderCreateForm,PayMoneyForm

# Create your views here.

# manager
@login_required(login_url='login')
def pay_back_money(request,user_id,*args,**kargs):
    user = User.objects.get(username=request.user)
    if not user.has_perm('menu.is_manager'):
        return render(request,'manager_pages/no_permition.html',{})
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        user.useradditionalinformation.money_pay_back = 0
        user.useradditionalinformation.save()
        return redirect('/manager/money_paying')
    context = {
        'user':user
    }
    return render(request,'manager_pages/pay_back_money_view.html',context)

@login_required(login_url='login')
def pay_money(request,user_id,*args,**kargs):
    user = User.objects.get(username=request.user)
    if not user.has_perm('menu.is_manager'):
        return render(request,'manager_pages/no_permition.html',{})
    form = PayMoneyForm()
    user = User.objects.get(id=user_id)
    if request.method == 'POST':
        money = int(request.POST.get('money'))
        if (user.useradditionalinformation.money_to_pay - money) >= 0:
            user.useradditionalinformation.money_to_pay -= money
            user.useradditionalinformation.save()
        else:
            user.useradditionalinformation.money_pay_back = money - user.useradditionalinformation.money_to_pay
            user.useradditionalinformation.money_to_pay = 0
            user.useradditionalinformation.save()
        return redirect('/manager/money_paying')
    context = {
        'form':form,
        'user':user
    }
    return render(request,'manager_pages/pay_money_view.html',context)

@login_required(login_url='login')
def money_paying_condition(request,*args,**kargs):
    user = User.objects.get(username=request.user)
    if not user.has_perm('menu.is_manager'):
        return render(request,'manager_pages/no_permition.html',{})
    nonpay_user_list = []
    money_to_give_user_list = []
    for user in User.objects.all():
        if user.useradditionalinformation.money_to_pay != 0:
            nonpay_user_list.append(user)
        if user.useradditionalinformation.money_pay_back != 0:
            money_to_give_user_list.append(user)
    context = {
        'nonpay_user_list':nonpay_user_list,
        'money_to_give_user_list':money_to_give_user_list
    }
    return render(request,'manager_pages/money_paying_condition.html',context)

@login_required(login_url='login')
def manager_view(request,*args,**kargs):
    user = User.objects.get(username=request.user)
    if not user.has_perm('menu.is_manager'):
        return render(request,'manager_pages/no_permition.html',{})
    return render(request,'manager_pages/manager_view.html',{})

@login_required(login_url='login')
def be_a_manager(request,*args,**kargs):
    user = User.objects.get(username=request.user)
    perm = Permission.objects.get(codename='is_manager')
    user.user_permissions.add(perm)
    return redirect('/manager')

@login_required(login_url='login')
def all_order_view(request,*args,**kargs):
    user = User.objects.get(username=request.user)
    if not user.has_perm('menu.is_manager'):
        return render(request,'manager_pages/no_permition.html',{})
    every_food = list(Food.objects.all())
    food_order_number = []
    food_name = []
    food_count_price = []
    total_price = 0
    for food in every_food:
        food_all_order = list(Order.objects.filter(food_id=food.food_id))
        order_number = 0
        for food_order in food_all_order:
            order_number += food_order.number_of_ordering
        if order_number != 0:
            total_price += order_number*food.price
            food_order_number.append(order_number)
            food_name.append(str(food.name))
            food_count_price.append(food.price*order_number)
    all_list = []
    for i in range(len(food_order_number)):
        all_list.append([i+1,food_name[i],food_order_number[i],food_count_price[i]])
    context = {
        'all_list':all_list,
        'total_price':total_price
    }
    return render(request,'manager_pages/all_order_view.html',context)


#order
@login_required(login_url='login')
def cart_view(request,*args,**kargs):
    user_sit_number = request.user.useradditionalinformation.sit_number
    user_order_list = list(Order.objects.filter(order_sit_number=user_sit_number))
    total_price = 0
    for user_order in user_order_list:
        total_price += user_order.food_price*user_order.number_of_ordering
    context={
        'user_order_list':user_order_list,
        'total_price':total_price
    }
    return render(request,'order_pages/cart_view.html',context)

@login_required(login_url='login')
def order_create_view(request,my_food_id,*args,**kargs):
    my_food = Food.objects.get(food_id = my_food_id)
    user = User.objects.get(username=request.user)
    try:
        old_order = Order.objects.get(food_name=my_food.name,order_sit_number=request.user.useradditionalinformation.sit_number)
        orderform = OrderCreateForm(instance=old_order)
        old_order_number = old_order.number_of_ordering
    except Order.DoesNotExist:
        old_order = False
        orderform = OrderCreateForm()
    if request.method == "POST":
        number_of_order = int(request.POST.get('number_of_ordering'))
        if old_order != False:
            old_money = old_order.food_price*old_order.number_of_ordering
            old_order.number_of_ordering = number_of_order
            old_order.save()
            my_food.popular = my_food.popular - old_order_number + number_of_order
            my_food.save()
            user.useradditionalinformation.money_to_pay += my_food.price*number_of_order - old_money
            user.useradditionalinformation.save()
            return redirect('/food/detail')
        else:
            new_order = Order(food_name=my_food.name,food_price=my_food.price,order_sit_number=request.user.useradditionalinformation.sit_number,number_of_ordering=number_of_order,food_id=my_food.food_id)
            new_order.save()
            my_food.popular += number_of_order
            my_food.save()
            user.useradditionalinformation.money_to_pay += my_food.price*number_of_order
            user.useradditionalinformation.save()
            return redirect('/food/detail')
    context={
        'orderform':orderform,
        'my_food':my_food
    }
    return render(request,'order_pages/order_create_view.html',context)


# food
@login_required(login_url='login')
def food_delete(request,my_food_id,*args,**kargs):
    user = User.objects.get(username=request.user)
    if not user.has_perm('menu.can_delete'):
        return redirect('/food/detail')
    try:
        obj = Food.objects.get(food_id = my_food_id)
    except Food.DoesNotExist:
        raise Http404("This food isn't exist")
    obj.delete()
    obj_list = list(Food.objects.all())
    for obj in obj_list:
        if obj.food_id > my_food_id:
            obj.food_id -= 1
            obj.save()
    return redirect('/food/detail')

@login_required(login_url='login')
def food_change_view(request,my_food_id,*args,**kargs):
    try:
        obj = Food.objects.get(food_id = my_food_id)
    except Food.DoesNotExist:
        raise Http404("This food isn't exist")
    form = FoodChangeForm(request.POST or None,instance=obj)
    if form.is_valid():
        form.save()
        form = FoodChangeForm(instance=obj)
    context = {
        'form':form
    }
    return render(request,'menu_pages/food_change_view.html',context)

@login_required(login_url='login')
def food_detail_view(request,*args,**kargs):
    user = User.objects.get(username=request.user)
    per = user.has_perm('menu.can_delete')
    obj_list = list(Food.objects.all())
    context = {
        'objlist':obj_list,
        'permition':per
    }
    return render(request,'menu_pages/food_detail_view.html',context)

@login_required(login_url='login')
def food_create_view(request,*args,**kargs):
    form = FoodCreateForm(request.POST or None)
    if form.is_valid():
        form.save()
        food_len = len(list(Food.objects.all()))
        food = Food.objects.get(food_id=0)
        food.food_id = food_len
        food.save()
        form = FoodCreateForm()
    context = {
        'form':form
    }
    return render(request,'menu_pages/food_create_view.html',context)