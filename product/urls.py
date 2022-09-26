from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from product.views.API.product import *

urlpatterns = [
    path('', ProductListCreateAPIView.as_view()),
	path('<int:pk>', ProductRetrieveUpdateDestroyAPIView.as_view()), 
	path('search', SearchResultsView.as_view()),
    path('recommendation', ProductRecommendationView.as_view()),
]
