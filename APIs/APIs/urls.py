"""APIs URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from django.urls import include  #原本已经引入一些包了, 这时候再引入一个include
urlpatterns = [
    path('admin/', admin.site.urls),
    # 固定写法
    path('bishe/', include('bishe.urls'))  # 添加bishe路由  就是127.0.0.1:8001/bishe/   就是一个定向功能
]
