from django.urls import path

from . import views

urlpatterns = [
    #user panel
    path("admin/", views.admin, name="admin"),
    path('logout/',views.logout_view ,name='logout'),
    path('login/',views.login_view ,name='login'),
    path('register/',views.register_view ,name='register'),
    path('verify_user/<int:user_id>/', views.verify_user, name='verify_user'),
    

    #product panel
    path("product/", views.product, name="product"),
    path('product/add/', views.add_product, name='add_product'),
    path('product/<int:id>/edit/', views.edit_product, name='update_product'),
    path('product/<int:id>/delete/', views.delete_product, name='delete_product'),
    path('available/<int:product_id>/', views.available, name='available'),

    #orders panel
    path("orders/", views.orders_dashboard, name="orders"),
    path("orders/<int:order_id>/", views.order_detail, name="order_detail"),
    path("orders/<int:order_id>/toggle/", views.order_toggle, name="order_toggle"),
    path("admin/sales/", views.sales_list, name="sales_list"),


    #sales panel
    path("sales/", views.sales_list, name="sales"),
    path("sales/add/", views.sales_create, name="sales_create"),
    path("sales/<int:sale_id>/edit/", views.sales_update, name="sales_update"),
    path("sales/<int:sale_id>/delete/", views.sales_delete, name="sales_delete"),
    path("sales/<int:sale_id>/toggle/", views.sales_toggle, name="sales_toggle"),

]