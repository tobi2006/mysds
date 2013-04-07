from django.conf.urls import patterns, include, url
from django.contrib import admin
import mysds
import database
admin.autodiscover()

urlpatterns = patterns('mysds.views',
    url(r'^$', 'default_page', name = 'home'),
    url(r'^na/$', 'na', name = 'na'),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('database.views',
    url(r'^search_student/$', 'search_student', name = 'search_student'),
    url(r'^student/(\w+)/$', 'student_view', name = 'student_view'),
    url(r'^add_student/$', 'add_student', name='add_student'),
    url(r'^edit_student/(\w+)/$', 'edit_student', name='edit_student'),
    url(r'^add_module/$', 'add_module', name='add_module'),
    url(r'^edit_module/(\w+)/(\d{4})/$', 'edit_module', name='edit_module'),
    url(r'^add_students_to_module/(\w+)/(\d{4})/$', 'add_students_to_module', name='add_students_to_module'),
    url(r'^module/(\w+)/(\d{4})/$', 'module_view', name = 'module_view'),
    url(r'^module_overview/(\d{4})/$', 'module_overview', name = 'module_overview'),
    url(r'^mark/(\w+)/(\d{4})/(\w+)/$', 'mark', name = 'mark'),
    url(r'^seminar_groups/(\w+)/(\d{4})/$', 'seminar_groups', name = 'seminar_groups'),
    url(r'^absences/(\w+)/(\d{4})/(\w+)/$', 'absences', name = 'absences'),
    url(r'^year/(\d{1})/$', 'year_view', name = 'year_view'),
    url(r'^upload_csv/$', 'upload_csv', name = 'upload_csv'),
    url(r'^parse_csv/$', 'parse_csv', name = 'parse_csv'),
    url(r'^import_success/$', 'import_success', name = 'import_success')
)
