"""ErpTAXE URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
#from django.urls import path
from django.conf.urls import include, url

handler404 = "ErpBackOffice.views.error_404"
handler500 = "ErpBackOffice.views.error_500"
handler403 = "ErpBackOffice.views.error_403"
handler400 = "ErpBackOffice.views.error_400"

admin.autodiscover()
admin.site.enable_nav_sidebar = False
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include('ErpBackOffice.urls')),
    url(r'^configuration/', include('ModuleConfiguration.urls')),
    url(r'^application/', include('ModuleApplication.urls')),
]


#urlpatterns.append(url(r'^conversation/', include('ModuleConversation.urls')))
urlpatterns.append(url(r'^archivage/', include('ModuleArchivage.urls')))
urlpatterns.append(url(r'^support/', include('ModuleSupport.urls')))
urlpatterns.append(url(r'^stock/', include('ModuleStock.urls')))