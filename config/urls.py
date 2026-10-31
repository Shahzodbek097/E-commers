from django.contrib import admin
from django.urls import path, re_path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView, TokenVerifyView)
from billing.views import TolovView


class JWTSchemaGenerator(OpenAPISchemaGenerator):
    def get_security_definitions(self):
        security_definitions=super().get_security_definitions()
        security_definitions['Bearer']={
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
        return security_definitions


schema_view=get_schema_view(
    openapi.Info(
        title='API',
        default_version='v1',
        description='E-commarce API',
        terms_of_service='http://www.google.com/policies/terms',
        contact=openapi.Contact(email='shahzodabdusattorov33@email.com'),
        license=openapi.License(name='BSD License'),
    ),
    public=True,
)

urlpatterns = [
    path('admin/', admin.site.urls),

    #API URLs
    path("api/v1/", include('products.urls')),

    #Djoser sxemai
    path('api/v1/auth/', include('djoser.urls')),
    path('api/v1/auth/token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('api/v1/auth/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('api/v1/auth/token/verify/', TokenVerifyView.as_view(), name='token-verify'),

    #Payment
    path('api/v1/pay/', TolovView.as_view(), name='create-payme'),

    #Swagger sxemasi JSON/YAML sxemasi
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),

    #Swagger interfeysi
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),

    #ReDoc interfeysi
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc')
]
