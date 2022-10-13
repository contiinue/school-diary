from rest_framework import routers
from django.urls import path, include
from .views import ApiSetEvaluation


router = routers.DefaultRouter()
# router.register('', ApiSetEvaluation, basename='some')


urlpatterns = [
    # path('<int:class_number>/<slug:slug_name>/', include(router.urls))
    path('<int:class_number>/<slug:slug_name>/', ApiSetEvaluation.as_view())
]
