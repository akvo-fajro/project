from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User,Permission
from django.http import Http404

# import self define models and form
from .models import Food,Order
from .forms import FoodCreateForm,OrderCreateForm,PayMoneyForm,FoodChangeForm,ForgotOrderForm

# Create your views here.

# users
@login_required(login_url='login')
def pay_money_user_view(request,*args,**kargs):
    user = User.objects.get(username=request.user)
    form = PayMoneyForm()
    if request.method == 'POST':
        money = int(request.POST.get('money'))
        if (user.useradditionalinformation.money_to_pay - money) >= 0:
            user.useradditionalinformation.money_to_pay -= money
            user.useradditionalinformation.save()
        else:
            user.useradditionalinformation.money_pay_back = money - user.useradditionalinformation.money_to_pay
            user.useradditionalinformation.money_to_pay = 0
            user.useradditionalinformation.save()
        return redirect('/accounts/profile')
    context = {
        'form':form,
        'user':user,
        'user_is_manager':False
    }
    return render(request,'manager_pages/pay_money_view.html',context)


# manager
@login_required(login_url='login')
def change_new_menu(request,*args,**kargs):
    user = User.objects.get(username=request.user)
    if not user.has_perm('menu.is_manager'):
        return render(request,'manager_pages/no_permition_view.html',{})
    food_list = list(Food.objects.all())
    order_list = list(Order.objects.all())
    for i in range(len(food_list)-1,-1,-1):
        food_list[i].delete()
    for i in range(len(order_list)-1,-1,-1):
        order_list[i].delete()
    user_list = list(User.objects.all())
    perm = Permission.objects.get(codename='is_manager')
    perm_order = Permission.objects.get(codename='can_order')
    for user in user_list:
        if user.has_perm('menu.is_manager'):
            user.user_permissions.remove(perm)
        if not user.has_perm('menu.can_order'):
            user.user_permissions.add(perm_order)
    return redirect('/food/detail')

@login_required(login_url='login')
def user_no_be_manager(request,*args,**kargs):
    user = User.objects.get(username=request.user)
    if not user.has_perm('menu.is_manager'):
        return render(request,'manager_pages/no_permition_view.html',{})
    perm = Permission.objects.get(codename='is_manager')
    user.user_permissions.remove(perm)
    return redirect('/manager/change_permition')

@login_required(login_url='login')
def clear_all_user_money(request,*args,**kargs):
    user = User.objects.get(username=request.user)
    if not user.has_perm('menu.is_manager'):
        return render(request,'manager_pages/no_permition_view.html',{})
    user_list = User.objects.all()
    for user in user_list:
        user.useradditionalinformation.money_to_pay = 0
        user.useradditionalinformation.money_pay_back = 0
        user.useradditionalinformation.save()
    return redirect('/manager/change_permition')

@login_required(login_url='login')
def let_user_not_order(request,*args,**kargs):
    user = User.objects.get(username=request.user)
    if not user.has_perm('menu.is_manager'):
        return render(request,'manager_pages/no_permition_view.html',{})
    user_list = User.objects.all()
    for user in user_list:
        if user.has_perm('menu.can_order'):
            perm = Permission.objects.get(codename='can_order')
            user.user_permissions.remove(perm)
    return redirect('/manager/change_permition')

@login_required(login_url='login')
def let_user_order(request,*args,**kargs):
    user = User.objects.get(username=request.user)
    if not user.has_perm('menu.is_manager'):
        return render(request,'manager_pages/no_permition_view.html',{})
    user_list = User.objects.all()
    for user in user_list:
        if not user.has_perm('menu.can_order'):
            perm = Permission.objects.get(codename='can_order')
            user.user_permissions.add(perm)
    return redirect('/manager/change_permition')

@login_required(login_url='login')
def change_permition_view(request,*args,**kargs):
    user = User.objects.get(username=request.user)
    if not user.has_perm('menu.is_manager'):
        return render(request,'manager_pages/no_permition_view.html',{})
    return render(request,'manager_pages/change_permition_view.html',{})

@login_required(login_url='login')
def forgot_order_view(request,*args,**kargs):
    user = User.objects.get(username=request.user)
    if not user.has_perm('menu.is_manager'):
        return render(request,'manager_pages/no_permition_view.html',{})
    form = ForgotOrderForm()
    if (request.method == "POST") and (str(request.user) == str(request.POST.get('name'))):
        user_list = list(User.objects.all())
        for user in user_list:
            order_list = Order.objects.filter(order_sit_number=user.useradditionalinformation.sit_number)
            money_pay_back = 0
            for order in order_list:
                if order.number_of_ordering == 0:
                    continue
                order_food = Food.objects.get(food_id=order.food_id)
                money_pay_back += order_food.price*order.number_of_ordering
            for i in range(len(order_list)-1,-1,-1):
                order_list[i].delete()
            if money_pay_back == 0:
                continue
            money_pay_back = money_pay_back
            if user.useradditionalinformation.money_to_pay != 0:
                money_pay_back -= user.useradditionalinformation.money_to_pay
                user.useradditionalinformation.money_to_pay = 0
                user.useradditionalinformation.save()
            user.useradditionalinformation.money_pay_back += money_pay_back
            user.useradditionalinformation.save()
        return redirect('/manager/money_paying')
    context = {
        'form':form
    }
    return render(request,'manager_pages/forgot_order_view.html',context)

@login_required(login_url='login')
def pay_back_money_view(request,user_id,*args,**kargs):
    user = User.objects.get(username=request.user)
    if not user.has_perm('menu.is_manager'):
        return render(request,'manager_pages/no_permition_view.html',{})
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
def pay_money_manager_view(request,user_id,*args,**kargs):
    user = User.objects.get(username=request.user)
    if not user.has_perm('menu.is_manager'):
        return render(request,'manager_pages/no_permition_view.html',{})
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
        'user':user,
        'user_is_manager':True
    }
    return render(request,'manager_pages/pay_money_view.html',context)

@login_required(login_url='login')
def money_paying_condition_view(request,*args,**kargs):
    user = User.objects.get(username=request.user)
    if not user.has_perm('menu.is_manager'):
        return render(request,'manager_pages/no_permition_view.html',{})
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
    return render(request,'manager_pages/money_paying_condition_view.html',context)

@login_required(login_url='login')
def manager_view(request,*args,**kargs):
    user = User.objects.get(username=request.user)
    if not user.has_perm('menu.is_manager'):
        return render(request,'manager_pages/no_permition_view.html',{})
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
        return render(request,'manager_pages/no_permition_view.html',{})
    every_food = list(Food.objects.all())
    total_price = 0
    count = 1
    all_list = []
    for food in every_food:
        food_all_order = list(Order.objects.filter(food_id=food.food_id))
        order_number = 0
        for food_order in food_all_order:
            order_number += food_order.number_of_ordering
        if order_number != 0:
            total_price += order_number*food.price
            all_list.append([count,str(food.name),order_number,order_number*food.price])
            count += 1
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
    user_order_all_list = []
    total_price = 0
    for user_order in user_order_list:
        if user_order.number_of_ordering == 0:
            continue
        user_order_food = Food.objects.get(food_id=user_order.food_id)
        user_order_all_list.append([user_order_food.name,user_order_food.price,user_order.number_of_ordering,user_order_food.price*user_order.number_of_ordering,user_order_food.food_id])
        total_price += user_order_food.price*user_order.number_of_ordering
    context={
        'user_order_all_list':user_order_all_list,
        'total_price':total_price,
        'can_order':User.objects.get(username=request.user).has_perm('menu.can_order')
    }
    return render(request,'order_pages/cart_view.html',context)

@login_required(login_url='login')
def order_create_view(request,my_food_id,*args,**kargs):
    user = User.objects.get(username=request.user)
    if not user.has_perm('menu.can_order'):
        return redirect('/accounts/cart')
    my_food = Food.objects.get(food_id = my_food_id)
    try:
        old_order = Order.objects.get(food_id=my_food.food_id,order_sit_number=request.user.useradditionalinformation.sit_number)
        orderform = OrderCreateForm(instance=old_order)
        old_order_number = old_order.number_of_ordering
    except Order.DoesNotExist:
        old_order = False
        orderform = OrderCreateForm()
    if request.method == "POST":
        number_of_order = int(request.POST.get('number_of_ordering'))
        if old_order != False:
            old_money = my_food.price*old_order_number
            old_order.number_of_ordering = number_of_order
            old_order.save()
            my_food.popular = my_food.popular - old_order_number + number_of_order
            my_food.save()
            user.useradditionalinformation.money_to_pay += my_food.price*number_of_order - old_money
            user.useradditionalinformation.save()
            return redirect('/food/detail')
        else:
            new_order = Order(order_sit_number=request.user.useradditionalinformation.sit_number,number_of_ordering=number_of_order,food_id=my_food.food_id)
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
def food_change_view(request,my_food_id,*args,**kargs):
    my_food = Food.objects.get(food_id = my_food_id)
    original_price = my_food.price
    form = FoodChangeForm(instance=my_food)
    if request.method == "POST":
        new_name = request.POST.get('name')
        new_price = int(request.POST.get('price'))
        order_list = list(Order.objects.filter(food_id=my_food_id))
        all_user_list = list(User.objects.all())
        for order in order_list:
            for user in all_user_list:
                if user.useradditionalinformation.sit_number != order.order_sit_number:
                    continue
                if new_price > original_price:
                    if user.useradditionalinformation.money_pay_back > (new_price - original_price):
                        user.useradditionalinformation.money_pay_back -= (new_price - original_price)
                    else:
                        user.useradditionalinformation.money_to_pay += (new_price - original_price) - user.useradditionalinformation.money_pay_back
                        user.useradditionalinformation.money_pay_back = 0
                    user.useradditionalinformation.save()
                    break
                elif new_price < original_price:
                    if user.useradditionalinformation.money_to_pay < (original_price - new_price):
                        user.useradditionalinformation.money_pay_back += (original_price - new_price) - user.useradditionalinformation.money_to_pay
                        user.useradditionalinformation.money_to_pay = 0
                    else:
                        user.useradditionalinformation.money_to_pay -= (original_price - new_price)
                    user.useradditionalinformation.save()
                    break
                else:
                    pass
        my_food.name = new_name
        my_food.price = new_price
        my_food.save()
        return redirect('/food/detail')
    context = {
        'form':form
    }
    return render(request,'menu_pages/food_change_view.html',context)


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
def food_detail_view(request,*args,**kargs):
    user = User.objects.get(username=request.user)
    per = user.has_perm('menu.can_delete')
    obj_list = list(Food.objects.all())
    context = {
        'objlist':obj_list,
        'permition':per,
        'can_order':user.has_perm('menu.can_order')
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
