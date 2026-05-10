from django.urls import path

from . import views

urlpatterns = [

    path('',views.HomeView.as_view(),name='home'),
    
    path('add-cake/',views.AddCakeView.as_view(),name='add-cake'),
    
    path('cake-details/<str:uuid>/',views.CakeDetailsView.as_view(),name='cake-details'),

    path('cake-edit/<str:uuid>/',views.CakeEditView.as_view(),name='cake-edit'),

    path('cake-delete/<str:uuid>/',views.CakeDeleteView.as_view(),name='cake-delete'),

    path('add-wishlist/<str:uuid>/',views.AddToWishList.as_view(),name='add-wishlist'),

    path('remove-wishlist/<str:uuid>/',views.RemoveFromWishList.as_view(),name='remove-wishlist'),

    path('wishlist/',views.WishListView.as_view(),name='wishlist'),

    path('add-cart/<str:uuid>/',views.AddToCart.as_view(),name='add-cart'),

    path('remove-cart/<str:uuid>/',views.RemoveFromCart.as_view(),name='remove-cart'),
    

    ]