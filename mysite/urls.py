
"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from .views import accueil, pdf, word, defilement, formulaire, table_view, display_table, extract_table, graph_view, graphiqueW, graphiqueP, home
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", accueil),
    path("defilement.html", defilement),
    path("formulaire.html", formulaire),
    path("affiche.html", table_view, name='table'),
    path("pdf.html", pdf),
    path("word.html", word),
    path("tableauPDF.html", display_table),
    path("tableauWord.html", extract_table),
    path("graph.html", graph_view),
    path("graphiqueW.html", graphiqueW),
    path("graphiqueP.html", graphiqueP),
    path("home.html", home),

]
