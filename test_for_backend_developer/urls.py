"""test_for_backend_developer URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from myapp.views import StartPage, UploadImage, ResizeImage

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'', StartPage.as_view(), name='start page'),
    path(r'upload/', UploadImage.as_view(), name='upload image'),
    path(r'<image_id>/width-<width>height-<height>size-<size>', ResizeImage.as_view(), name='resize image'),
]
