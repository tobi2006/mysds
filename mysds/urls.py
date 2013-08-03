from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout
import mysds
import database
admin.autodiscover()

urlpatterns = patterns('mysds.views',
    url(r'^$', 'default_page', name = 'home'),
    url(r'^na/$', 'na', name = 'na'),
    url(r'^admin/', include(admin.site.urls)),
    (r'^accounts/login/$',  login, {'template_name': 'login.html'}),
    (r'^accounts/logout/$', logout, {'template_name': 'logout.html'}),
)

urlpatterns += patterns('database.views',
    url(r'^search_student/$', 'search_student', name = 'search_student'),
    url(r'^student/(\w+)/$', 'student_view', name = 'student_view'),
    url(r'^add_student/$', 'add_student', name='add_student'),
    url(r'^edit_student/(\w+)/$', 'edit_student', name='edit_student'),
    url(r'^lsp_view/(\w+)/$', 'lsp_view', name='lsp_view'),
    url(r'^lsp_edit/(\w+)/$', 'lsp_edit', name='lsp_edit'),
    url(r'^notes_edit/(\w+)/$', 'notes_edit', name='notes_edit'),
    url(r'^add_module/$', 'add_module', name='add_module'),
    url(r'^edit_module/(\w+)/(\d{4})/$', 'edit_module', name='edit_module'),
    url(r'^add_students_to_module/(\w+)/(\d{4})/$', 'add_students_to_module', name='add_students_to_module'),
    url(r'^module/(\w+)/(\d{4})/$', 'module_view', name = 'module_view'),
    url(r'^module_overview/(\d{4})/$', 'module_overview', name = 'module_overview'),
    url(r'^mark/(\w+)/(\d{4})/(\w+)/$', 'mark', name = 'mark'),
    url(r'^seminar_groups/(\w+)/(\d{4})/$', 'seminar_groups', name = 'seminar_groups'),
    url(r'^attendance/(\w+)/(\d{4})/(\w+)/$', 'attendance', name = 'attendance'),
    url(r'^year/(\w+)/$', 'year_view', name = 'year_view'),
    url(r'^upload_csv/$', 'upload_csv', name = 'upload_csv'),
    url(r'^parse_csv/$', 'parse_csv', name = 'parse_csv'),
    url(r'^import_success/$', 'import_success', name = 'import_success'),
    url(r'^upload_anon_ids/$', 'upload_anon_ids', name = 'upload_anon_ids'),
    url(r'^edit_anon_ids/$', 'edit_anon_ids', name = 'edit_anon_ids')
)
