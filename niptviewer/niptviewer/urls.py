"""niptviewer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import include, path, re_path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    re_path('^(?P<time_selection>[0-9]+)m$', views.index, name='index'),
    path('index', views.index, name='index'),
    re_path('index/^(?P<time_selection>[0-9]+)m$', views.index, name='index'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('viewer/', include('reportvisualiser.urls')),
    path('api', include('dataprocessor.urls')),
    path('admin/', include('users.urls')),
]
