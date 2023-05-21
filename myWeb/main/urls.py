from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_view
from .forms import LoginForm
from django.views.generic import RedirectView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeDoneView
from .views import ChangePasswordView

urlpatterns = [
    path('', views.welcome, name='mainhome'),
    path('index/', views.index, name='index'),
    path('<int:pk>',views.detail, name='detail'),
    path('warning/', views.warning, name='warning'),
    path('about/',views.about,name='about'),
    
    path('login/',auth_view.LoginView.as_view(template_name='login.html',authentication_form=LoginForm),name='login'),
    
    path('logout/',auth_view.LogoutView.as_view(template_name='index.html'),name='logout'),
    
    path('signup/',views.signup,name='signup'),
    
    path('profile/',views.profile,name='profile'),

    path('passchange/', ChangePasswordView.as_view(), name='passchange'),
    path('passdone/', PasswordChangeDoneView.as_view(template_name='passdone.html'), name='passdone'),
    
    
    path('password-reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
    path('password-reset/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password-reset/complete/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    path('addtocart/<int:pk>/', views.addtocart, name='addtocart'),
    path('removefromcart/<int:pk>/', views.removefromcart, name='removefromcart'),
    path('cart/', views.cart, name='cart'),
    path('clearcart/', views.clearcart, name='clearcart'),
    path('review/<int:pk>/', views.review, name='review'),
    
    path('checkout/', views.checkout, name='checkout'),
    path('checkout/success/<int:pk>/', views.checkout_success, name='checkoutsucc'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
