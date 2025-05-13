from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from . import views
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('catalog/', views.catalog_view, name='catalog'),
    path('cart/', views.cart_view, name='cart'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html', success_url='home'), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('reviews/', views.reviews_view, name='reviews'),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)