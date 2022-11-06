from rest_framework import routers
from django.urls import path, include
from .views import ApiEvaluation, ApiSetEvaluation

router = routers.DefaultRouter()
router.register('evaluation/(?P<class_number>\d+)/(?P<slug_name>\w+)', ApiEvaluation, basename='user-evaluation')
router.register('evaluation', ApiSetEvaluation, basename='set-evaluation')

urlpatterns = [
    path('', include(router.urls)),
]
