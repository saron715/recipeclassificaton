from django.urls import path
from . import views
urlpatterns = [
    path("",views.index,name="index"),
    path("login",views.login_view,name="login"),
    path("logout",views.logout_view,name="logout"),
    path("profile",views.profile,name="profile"),
    path("signup",views.signup_view,name="signup"),
    path("settings",views.settings_view,name="settings"),
    path("recipe_post",views.recipe_post,name="recipe_post"),
    path("recipe_list",views.recipe_list_view,name="recipe_list"),

    

    

]
