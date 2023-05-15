
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
from .views import accueil, pdf, word, defilement, extract_table, graphiqueW, graphiqueP
from extraction.views import index, affpdf, copie, formulaire

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", accueil),
    path("defilement.html", defilement),
    path("pdf.html", pdf),
    path("word.html", word),
    path("tableauWord.html", extract_table),
    path("graphiqueW.html", graphiqueW),
    path("success.html", index),
    path("formulaire.html", formulaire),
    path("graphiqueP.html", affpdf),
    path("mon_gabarit.html", copie),
]
