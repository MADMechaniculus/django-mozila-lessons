"""django_probe URL Configuration

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
from django.conf.urls.static import static
from django.conf import settings
from django.views.generic import RedirectView
from django.urls import include
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]

# include() - используется для управления файлами из каталога приложения

urlpatterns += [
    path('catalog/', include('catalog.urls'))
]

# Url соотношения для перенаправления с корневого url

urlpatterns += [
    path('', RedirectView.as_view(url='/catalog/', permanent=True)),
]

# Используйте static() чтобы добавить соотношения для статических файлов
# Только на период разработки

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Добавление в urlpatterns можно делать просто в один массив (статически). Тут для наглядности юзали +=

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]