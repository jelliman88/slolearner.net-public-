from django.contrib import admin
from django.conf import settings
from django.urls import path, include, re_path
from django.conf.urls import url
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext as _
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views



urlpatterns = [
   path("admin/", admin.site.urls),
    
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

urlpatterns += i18n_patterns ( 
    url('', include('homepage.urls', namespace='homepage')),
    url('user-dash', include('user_dash.urls', namespace='user-dash')),
    url('learn/', include('learn.urls', namespace='learn')),
    url('create/', include('create.urls', namespace='create')),
    url('audio/', include('audio.urls', namespace='audio')),
    path("reset-password-sent", auth_views.PasswordResetDoneView.as_view(template_name='password-reset-sent.html'), name='password_reset_done'),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(template_name='password-reset-form.html'), name='password_reset_confirm'),
    path("reset-password-complete", auth_views.PasswordResetCompleteView.as_view(template_name='password-reset-complete.html'), name='password_reset_complete'),
    
   

)

if 'rosetta' in settings.INSTALLED_APPS:
    urlpatterns += [
        re_path(r'^rosetta/', include('rosetta.urls'))
    ]
