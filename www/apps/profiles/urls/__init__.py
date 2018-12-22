from django.conf.urls.defaults import *
from ..views import *

urlpatterns = patterns('',

    url(r'^$',
        ProfileDetialView.as_view(),
        name='profile_view_details'
    ),

    url(r'^profile/del/(?P<pk>\d+)/$',
        ProfileDeleteAccountView.as_view(),
        name='profile_delete_account'
    ),
    
    url(r'^edit/$',
        ProfileUpdateView.as_view(),
        name='profile_edit_details'
    ),
    
    url(r'^type/edit/$',
        ProfileTypeUpdateView.as_view(),
        name='profile_type_edit'
    ),
    
    url(r'^employee/edit/$',
        ProfileEmployeeUpdateView.as_view(),
        name='employee_profile_edit_details'
    ),

    url(r'^skill/$',
        EmployeeAddSkillView.as_view(),
        name='employee_skill_list'
    ),

    url(r'^skill/del/(?P<pk>\d+)/$',
        EmployeeDeleteSkillView.as_view(),
        name='employee_delete_skill'
    ),

    url(r'^skill/update/(?P<pk>\d+)/$',
        EmployeeUpdateSkillView.as_view(),
        name='employee_update_skill'
    ),
    
    url(r'^skill/subcat/$',
        EmployeeGetSkillSubcategoryView.as_view(),
        name='skill_add_get_subcat'
    ),

    url(r'^skill/search/subcat/$',
        SearchGetSkillSubcategoryView.as_view(),
        name='skill_search_get_subcat'
    ),

    url(r'^contact/info/$',
        ProfileFetchContactInfo.as_view(),
        name='profile_get_contact_info'
    ),
       
    url(r'^job/$',
        EmployerJobAddView.as_view(),
        name='employer_jobpost_list'
    ),

    url(r'^job/del/(?P<pk>\d+)/$',
        EmployerJobDeleteView.as_view(),
        name='employer_delete_jobpost'
    ),

    url(r'^job/update/(?P<pk>\d+)/$',
        EmployerJobUpdateView.as_view(),
        name='employer_update_jobpost'
    ),
    
    url(r'^job/contact/info/$',
        EmployerJobsFetchContactInfo.as_view(),
        name='employer_get_job_contact_info'
    ),

    url(r'^password/change/$',
        ProfileChangePassword.as_view(),
        name='profile_change_password'
    ),

    url(r'^bookmarks/$',
        ProfileBookmarkView.as_view(),
        name='bookmark_list'
    ),

    # remove profiles from within the bookmark list
    url(r'^bookmarks/del/profile/(?P<pk>\d+)/$',
        ProfileDelBookmarkView.as_view(),
        name='bookmark_del_profile'
    ),

    # add profiles from profile view ajax
    url(r'^bookmarks/add/profile/$',
        ProfileAddBookmarkAjaxView.as_view(),
        name='bookmark_add_profile_ajax'
    ),

    # remove profiles from profile view ajax
    url(r'^bookmarks/del/profile/$',
        ProfileDelBookmarkAjaxView.as_view(),
        name='bookmark_del_profile_ajax'
    ),

    # remove job from within the bookmark list
    url(r'^bookmarks/del/job/(?P<pk>\d+)/$',
        EmployerJobDelBookmarkView.as_view(),
        name='bookmark_del_job'
    ),
    
    # add job from job view ajax
    url(r'^bookmarks/add/job/$',
        EmployerJobAddBookmarkAjaxView.as_view(),
        name='bookmark_add_job_ajax'
    ),

    # remove job from job view ajax
    url(r'^bookmarks/del/job/$',
        EmployerJobDelBookmarkAjaxView.as_view(),
        name='bookmark_del_job_ajax'
    ),

    url(r'^training/$',
        ProfileTrainingView.as_view(),
        name='training_list'
    ),
    
    (r'^social/', include('www.apps.social.urls')),

    (r'^', include('www.contrib.emailmgr.urls')),
)
