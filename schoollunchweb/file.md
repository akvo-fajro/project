# schoollunchweb project

## environment
`ubuntu 20.04`<br>
`python 3.8.10`<br>
`pip 22.0.4`<br>
`django 4.0.3`<br>
`docker 20.10.7`<br>
`docker-compose 1.29.2`<br>
> the installation of this project is in setup.md


## file of project
```
site
├── mysqldb_docker.yml
├── new_day.py
├── schoollunchweb
│   ├── accounts_pages
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── forms.py
│   │   ├── __init__.py
│   │   ├── migrations
│   │   │   └── __init__.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   ├── urls.py
│   │   ├── users_pages
│   │   │   ├── change_password.html
│   │   │   ├── home.html
│   │   │   ├── login.html
│   │   │   └── profile.html
│   │   └── views.py
│   ├── foods_and_orders
│   │   ├── admin_pages
│   │   │   └── admin_over_view.html
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── food_pages
│   │   │   ├── food_change_view.html
│   │   │   ├── food_create_view.html
│   │   │   └── food_menu_view.html
│   │   ├── forms.py
│   │   ├── __init__.py
│   │   ├── manager_pages
│   │   │   ├── manager_over_view.html
│   │   │   ├── not_manager_view.html
│   │   │   └── pay_back_money_view.html
│   │   ├── migrations
│   │   │   └── __init__.py
│   │   ├── models.py
│   │   ├── order_pages
│   │   │   ├── cart_view.html
│   │   │   ├── order_create_view.html
│   │   │   └── pay_money_view.html
│   │   ├── state_pages
│   │   │   ├── money_state_view.html
│   │   │   ├── order_state_view.html
│   │   │   └── state_over_view.html
│   │   ├── tests.py
│   │   ├── timejob.py
│   │   ├── urls.py
│   │   └── views.py
│   ├── manage.py
│   ├── schoollunchweb
│   │   ├── asgi.py
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   │   ├── __init__.cpython-38.pyc
│   │   │   └── settings.cpython-38.pyc
│   │   ├── settings.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── static
│   │   └── admin
│   │       ├── [There's no important file here]
│   ├── templates
│   │   └── base.html
│   ├── users_additional_information
│   │   ├── admin.py
│   │   ├── apps.py
│   │   ├── __init__.py
│   │   ├── migrations
│   │   │   └── __init__.py
│   │   ├── models.py
│   │   ├── tests.py
│   │   └── views.py
│   └── uwsgi.ini
├── schoollunchweb_init
├── schoollunchweb_init.py
├── stop_ordering.py
└── timejob.py
```