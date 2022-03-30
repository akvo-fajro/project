# SchoolLunchWeb Setup

## environment
`Python 3.8.10`<br>
`Pip 20.0.4`<br>
`Django 4.0.3`<br>
`django-apscheduler 0.6.2`<br>

## set up django
`$ django-admin stratproject SchoolLunchWeb`<br>
`$ cd SchoolLunchWeb`<br>
`$ python3 manage.py migrate`<br>
`$ python3 manage.py startapp users_additional_information`<br>
`$ python3 manage.py startapp pages`<br>
`$ python3 manage.py startapp menu`<br>
`$ python3 manage.py startapp daily_routine`<br>
- set up users_additional_information
    - models.py
    - admin.py
- set up pages
    - views.py
    - forms.py
    - users_pages
        - users_change_password.html
        - users_home.html
        - users_login.html
        - users_profile.html
- set up menu
    - views.py
    - models.py
    - forms.py
    - admin.py
    - menu_pages
        - food_change_view.html
        - food_create_view.html
        - food_detail_view.html
    - order_pages
        - cart_view.html
        - order_create_view.html
    - manager_pages
        - all_order_view.html
        - forgot_order_view.html
        - manager_view.html
        - money_paying_condition_view.html
        - no_permition_view.html
        - pay_back_money_view.html
        - pay_money_view.html
- set a directory 'templates'
    - base.html
- set up SchoolLunchWeb
    - settings.py
        - import os
        - set INSTALLED_APPS
        - set TEMPLATES.DIRS
        - set STATIC_ROOT
    - urls.py
        - set pages' url
        - set menu's url

`$ python3 manage.py makemigrations`<br>
`$ python3 manage.py migrate`<br>
`$ python3 manage.py createsuperuser`<br>
`$ python3 manage.py shell`<br>
``` python =
>>> from menu.models import Order
>>> from django.contrib.auth.models import Permission
>>> from django.contrib.contenttypes.models import ContentType
>>> content_type = ContentType.objects.get_for_model(Order)
>>> permission1 = Permission.objects.create(codename='is_manager',name='is manager',content_type=content_type)
>>> permission2 = Permission.objects.create(codename='can_order',name='can order',content_type=content_type)
```
`$ python3 manage.py migrate`<br>
`$ python3 manage.py collectstatic`<br>
`$ python3 manage.py runserver`<br>

## set up uwsgi and nginx
[reference](https://orcahmlee.github.io/devops/nginx-uwsgi-django-root/)

## get a domain name
[no-ip web](https://www.noip.com/)

## get cert of ssl
[cerbot reference](https://certbot.eff.org/instructions?ws=nginx&os=ubuntufocal)

## set up daily_routine
[reference](https://cloud.tencent.com/developer/article/1585026)
