"""quiz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from app.custom_serializer import CustomAuthToken
from app.all_views import views_collections, views_user
from app import views
from django_files import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

favicon_view = RedirectView.as_view(
    url='/static/images/favicon.webp', permanent=True)

urlpatterns = [
    # Frontend urls
    path('', views.login_view),
    # For users
    path('admin/', admin.site.urls),
    path('login/', views.login_view),
    path('register/', views.register_view),
    path('profile/', views.profile_view),
    # For collections
    path('collections', views.collections_view),
    path('new-collection', views.collection_view),
    path('collections/<int:collection_id>/', views.collection_view),

    # API urls
    # For users
    path('api/token/', CustomAuthToken.as_view()),
    path('api/register/', views_user.register_user),
    path('api/user_info/', views_user.user_info),
    # For collections
    path('api/collections/', views_collections.collections),
    path('api/collections/<int:collection_id>/', views_collections.collection),

    # Extras
    path('favicon.ico/', favicon_view),
    path('health/', views.health),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
