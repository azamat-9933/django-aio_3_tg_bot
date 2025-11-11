from django.contrib import admin
from django.urls import path, include

from django.conf.urls.static import static

from django.shortcuts import redirect

from rest_framework.permissions import IsAuthenticated
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings

schema_view = get_schema_view(
    openapi.Info(
        title="Nasim Kutub API",
        default_version='v1',
        description="OPENAPI for Nasim Kutub",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="azamat.yakhyayeff@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[IsAuthenticated]
)





urlpatterns = [
    path('admin/', admin.site.urls),

    # redirect to admin
    path('', lambda request: redirect('admin/', permanent=True)),

    # swagger
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    # tg_bot_app
    path('tg_bot/', include('tg_bot.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
