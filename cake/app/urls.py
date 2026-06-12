from django.urls import path

from .import views

urlpatterns = [

    path('',views.HomeView.as_view(),name='home'),

    path('add-cake/',views.AddCakeView.as_view(),name='add-cake'),

    path('cake-details/<str:uuid>/',views.CakeDetailsView.as_view(),name='cake-details'),

    path('cake-edit/<str:uuid>/',views.CakeEditedView.as_view(),name='cake-edit'),

    path('cake-delete/<str:uuid>/',views.CakeDeleteView.as_view(),name='cake-delete'),

    path('add-wishlist/<str:uuid>/',views.AddToWishList.as_view(),name='add-wishlist'),

    path('remove-wishlist/<str:uuid>/',views.RemoveFromWishList.as_view(),name='remove-wishlist'),
    
    path('wishlist/',views.WishlistView.as_view(),name='wishlist'),

    path('add-cart/<str:uuid>/',views.AddToCart.as_view(),name='add-cart'),

    path('remove-cart/<str:uuid>/',views.RemoveFromCart.as_view(),name='remove-cart'),

    path('checkout/',views.CheckoutView.as_view(),name='checkout'),

    path('place-order/<str:uuid>/',views.PlaceOrderView.as_view(),name='place-order'),

    path('address-list/',views.DeliveryAddressListView.as_view(),name='address-list'),

    path('add-address/', views.AddDeliveryAddressView.as_view(), name='add-address'),

    path('edit-address/<str:uuid>/',views.UpdateDeliveryAddressView.as_view(),name='edit-address'),

    path('delete-address/<str:uuid>/',views.DeleteDeliveryAddressView.as_view(),name='delete-address'),


    

]