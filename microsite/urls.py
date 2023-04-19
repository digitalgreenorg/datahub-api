from django.urls import include, path
from rest_framework.routers import DefaultRouter

from datahub.views import PolicyDetailAPIView, PolicyListAPIView
from microsite.views import (
    ContactFormViewSet,
    DatahubThemeMicrositeViewSet,
    DatasetsMicrositeViewSet,
    DocumentsMicrositeViewSet,
    OrganizationMicrositeViewSet,
    ParticipantMicrositeViewSet,
)

router = DefaultRouter()
router.register(r"", OrganizationMicrositeViewSet, basename="o")
router.register(r"contact_form", ContactFormViewSet, basename="contact_form")
router.register(r"datasets", DatasetsMicrositeViewSet, basename="datasets")
router.register(r"", DocumentsMicrositeViewSet, basename="d")
router.register(r"", DatahubThemeMicrositeViewSet, basename="t")
router.register(r"participant", ParticipantMicrositeViewSet, basename="participant_microsite")

urlpatterns = [
    path("", include(router.urls)),
    path('policy/', PolicyListAPIView.as_view(), name='microsite-policy-list'),
    path('policy/<uuid:pk>/', PolicyDetailAPIView.as_view(), name='microsite-policy-detail'),

]
