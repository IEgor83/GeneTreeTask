from django.urls import path
from django.views.generic import RedirectView

from relatives import views


urlpatterns = [
    path('', RedirectView.as_view(url='/people/', permanent=True)),
    path('people/', views.person_list, name='person_list'),
    path('people/<int:person_id>/', views.person_detail, name='person_detail'),
    path('person_add/', views.person_add, name='person_add'),
    path('delete_relationship/', views.delete_relationship, name='delete_relationship'),
    path('person/<int:person_id>/delete/', views.delete_person, name='delete_person'),
]