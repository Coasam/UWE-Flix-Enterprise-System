"""UWEflix URL Configuration

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
from django.conf import settings
from django.conf.urls.static import static
from crud import views as crud

urlpatterns = [
    path('auth', crud.login),
    path('auth/rep', crud.representative_login),
    path('auth/register', crud.register_customer),
    path('auth/club/register/', crud.register_club, name="register_club"),
    path('logout', crud.logout),
    path('', crud.home, name='home'),
    path('film-detail/<str:id>/', crud.filmDetailPage, name='filmDetailPage'),
    path('club-rep-detail/<str:id>/', crud.clubDetailPage, name='clubDetailPage'),
    path('admin/', admin.site.urls),
    path('showings/', crud.showings),
    path('delete-film-with-no-showings/<str:id>/', crud.deleteFilmWithNoShowings, name="deleteFilmWithNoShowings"),
    path('club_account/', crud.club_account),
    path('accounts', crud.account_manager),
    # REST API
    path('api/v1/film', crud.create_film),

    # Images
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# path('admin/', admin.site.urls),
# path('add/', crud.add_account, name='add'),
# path('', crud.show, name='show'),
# path('update/<int:id>', crud.update, name="update"),
# path('delete/<int:id>', crud.delete, name="delete"),
# path('/hub', hub.index, name='index'),
