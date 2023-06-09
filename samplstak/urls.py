"""samplstak URL Configuration

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
from rest_framework import routers
from django.conf.urls import include
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from samplstakapi.views import register_user, login_user, GenreView, InstrumentView, SampleView, CollectionView, DrumkitView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'genres', GenreView, 'genre')
router.register(r'instruments', InstrumentView, 'instrument')
router.register(r'samples', SampleView, 'sample')
router.register(r'collections', CollectionView, 'collection')
router.register(r'drumkits', DrumkitView, 'drumkit')


urlpatterns = [
    path('register', register_user),
    path('login', login_user),
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
