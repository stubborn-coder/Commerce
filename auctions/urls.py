from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("category",views.category, name="category"),
    path("category/<str:filter>",views.filter, name="filter"),
    path("listing/<int:listing_id>/closelisting",views.closelisting, name="closelisting"),
    path("create_auction", views.create_auction, name="create_auction"),
    path("listing/<int:listing_id>/", views.listing, name="listing"),
    path("listing/<int:listing_id>/addcomment", views.addcomment, name="addcomment"),
    path("listing/<int:listing_id>/placebid", views.placebid, name="placebid"),
    path("listing/<int:listing_id>/addtowatchlist", views.addtowatchlist, name="addtowatchlist"),
    path("listing/<int:listing_id>/removefromwatchlist", views.removefromwatchlist, name="removefromwatchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)