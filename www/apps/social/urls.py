from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',

    url(r'^(?P<provider>\w+)/enable/$',
        SocialAuthProviderEnableView.as_view(),
        name='social_provider_enable'
    ),    

    url(r'^(?P<provider>\w+)/disable/$',
        SocialAuthProviderDisableView.as_view(),
        name='social_provider_disable'
    ), 
    
    url(r'^(?P<provider>\w+)/login/$',
        SocialAuthProviderLoginView.as_view(),
        name='social_provider_login'
    ),
          
    url(r'^(?P<provider>\w+)/auth$',
        SocialAuthProviderCallbackView.as_view(),
        name='social_provider_callback'
    ),

    url(r'^site/del/(?P<pk>\d+)/$',
        SocialProfileProviderDeleteView.as_view(),
        name='social_provider_delete'
    ),
    
    url(r'^',
        SocialProviderAddListView.as_view(),
        name='social_provider_list'
    )
)
