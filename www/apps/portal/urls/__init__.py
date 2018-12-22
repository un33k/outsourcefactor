from django.conf.urls.defaults import *
from ..views import *

urlpatterns = patterns('',

    url(r'^talent/$',
        TalentSearchView.as_view(),
        name='portal_talent_search'
    ),

    url(r'^talent/view/(?P<sp>\d+)/$',
        TalentSearchPaginateView.as_view(),
        name='portal_talent_search_paginate'
    ),
    
    url(r'^jobs/$',
        JobSearchView.as_view(),
        name='portal_job_search'
    ),

    url(r'^jobs/view/(?P<sk>\w+)/(?P<sp>\d+)/$',
        JobSearchPaginateView.as_view(),
        name='portal_job_search_paginate'
    ),

    url(r'^business/$',
        BusinessSearchView.as_view(),
        name='portal_business_search'
    ),

    url(r'^business/view/(?P<sk>\w+)/(?P<sp>\d+)/$',
        BusinessSearchPaginateView.as_view(),
        name='portal_business_search_paginate'
    ),
)
