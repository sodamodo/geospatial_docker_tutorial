"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from backend import settings
from django.views.generic import TemplateView
from backend.views import get_points, populate_routes, get_route_delay, create_fixtures, serve_delay_line_feature, serve_route_shp_json, get_predictions_for_route, average_delay, get_route_line, get_avg_delay_for_route

urlpatterns = [
	path(r'', TemplateView.as_view(template_name="index.html")),
    path('get_points/', get_points),
    path('populate_routes/', populate_routes),
    path('get_route_delay/', get_route_delay),
    path('create_fixtures/', create_fixtures),
    path('get_route_line/', serve_route_shp_json),
    path('serve_delay_line_feature/', serve_delay_line_feature),

    path('get_predictions_for_route/', get_predictions_for_route),
    path('average_delay/', average_delay),
    path('get_route_line/', get_route_line),
    path('get_avg_delay_for_route/', get_avg_delay_for_route)


	] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
