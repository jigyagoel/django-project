from django.urls import path

from .views import (
        ProductListView,
        #product_list_view ,
        #ProductDetailView,
        #product_detail_view ,
        #ProductFeaturedDetailView ,
        #ProductFeaturedListView,
        ProductDetailSlugView
        )
urlpatterns = [

    path('',ProductListView.as_view(),name="list"),
    path("<slug:slug>/",ProductDetailSlugView.as_view(),name="detail"),
]
