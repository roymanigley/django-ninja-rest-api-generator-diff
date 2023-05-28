from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.views.generic import TemplateView

from dummy_app.views import api

urlpatterns = [
  path('admin/', admin.site.urls),
  path('api/', api.urls),
  path('', TemplateView.as_view(template_name='index.html')),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
