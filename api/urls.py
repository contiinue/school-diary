from rest_framework import routers
from django.urls import path, include
from .views import ApiEvaluation

router = routers.DefaultRouter()
router.register('', ApiEvaluation, basename='some')


urlpatterns = [
    # path('<int:class_number>/<slug:slug_name>/', include(router.urls))
    path('<int:class_number>/<slug:slug_name>/', ApiEvaluation.as_view())
]
