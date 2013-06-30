from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'taskito.views.home', name='home'),
    # url(r'^taskito/', include('taskito.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^$',
        'base.views.home',
        name='home'),

    url(r'^login/$',
        'base.views.log_in',
        name='login'),

    url(r'^logout/$',
        'base.views.log_out',
        name='logout'),

    url(r'^tasks/list/$',
        'tasks.views.alltasks',
        name='alltasks'),

    url(r'^tasks/list/(?P<username>[a-zA-Z0-9_.-]+)$',
        'tasks.views.usertasks',
        name='usertasks'),

    url(r'^task/detail/(?P<year>\d+)/(?P<month>\d+)/(?P<day>\d+)/(?P<slug>[\w-]+)$',
        'tasks.views.taskdetail',
        name='taskdetail'),

    url(r'^task/create/$',
        'tasks.views.createtask',
        name='createtask'),

    url(r'^task/update/(?P<task_id>\d+)$',
        'tasks.views.updatetask',
        name='updatetask'),
)

urlpatterns += staticfiles_urlpatterns()
