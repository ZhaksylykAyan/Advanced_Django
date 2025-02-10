from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
import core.views as views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/', include('core.urls')),
    path('', views.index, name='index'),
    path('contact/', views.contact_view, name='contact'),
    path('success/', views.success_view, name='success_page'),
    path('profile/', views.create_cv, name='create_cv'),
    path('cv/', views.cv_list, name='cv_list'),
    path('share/email/<int:cv_id>/', views.share_cv_email, name='share_cv_email'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)