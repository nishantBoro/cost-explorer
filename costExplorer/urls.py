"""costExplorer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, re_path
from main.views import CostExplorerView

# Examples for some accepted URL's: http://127.0.0.1:8000/cost-explorer ,
# http://127.0.0.1:8000/cost-explorer?cost_types[]=1&projects[]=2 ,
# http://127.0.0.1:8000/cost-explorer?cost_types[]=5&clients[]=1&projects[]=2 ....

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^cost-explorer$', CostExplorerView.as_view()),
    path('cost-explorer', CostExplorerView.as_view())
]
