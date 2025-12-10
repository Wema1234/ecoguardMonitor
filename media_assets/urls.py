from django.urls import path
from . import views

app_name = 'media_assets'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('my-media/', views.my_media_view, name='my_media'),
    path('upload/', views.upload_media_view, name='upload_media'),
    path('media/<int:pk>/', views.media_detail_view, name='media_detail'),
    path('media/<int:pk>/edit/', views.edit_media_view, name='edit_media'),
    path('media/<int:pk>/delete/', views.delete_media_view, name='delete_media'),
    path('submit-data/', views.submit_data_view, name='submit_data'),
    path('reports/', views.reports_view, name='reports'),
    path('charts/', views.charts_view, name='charts'),
    path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
]
