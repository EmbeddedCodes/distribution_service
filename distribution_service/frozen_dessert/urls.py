
from django.contrib import admin
from django.contrib.auth import views as auth_views
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from django.urls import path, include

urlpatterns = [
    path('', auth_views.LoginView.as_view(
        template_name='home.html'), name='home'),
    path('admin/', admin.site.urls),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='login/login.html'), name='login'),
    path("products/", include("ice_cream.urls")),
    path("orders/", include("order.urls")),
    path("django-rq/", include("django_rq.urls")),
    path('api/auth/', include('dj_rest_auth.urls')),
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
    path("api/products/", include("ice_cream.api.urls")),
    path("api/orders/", include("order.api.urls")),
    path("api/payments/", include("payment.api.urls")),
    path("api/statistics/", include("statistic.api.urls")),
    path('api/docs/swagger/',
         SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/docs/redoc/',
         SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
