from django.conf.urls import patterns, include, url
from django.contrib import admin
#from django.contrib.auth.views import login, logout
#from django.contrib import auth
import mysds
import database
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name='login'),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'template_name': 'logout.html'}, name='logout'),
    url(r'^accounts/change_password/$', 'django.contrib.auth.views.password_change', {'template_name': 'change_password.html'}, name='change_password'),
    url(r'^accounts/change_password_done/$', 'django.contrib.auth.views.password_change_done', {'template_name': 'password_change_done.html'}, name='change_password_done')
)

urlpatterns += patterns('announcer.views',
    url(r'^$', 'show_homepage', name = 'home')
)

urlpatterns += patterns('mysds.views',
    url(r'^na/$', 'na', name = 'na'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^mark/(\w+)/(\d{4})/$', 'na', name = 'mark_no'), #Dummy to enable get_mark_url method
    url(r'^mark_anonymously/(\w+)/(\d{4})/$', 'na', name = 'mark_anon'), #Dummy to enable get_mark_url method
    url(r'^attendance/(\w+)/(\d{4})/$', 'na', name = 'attendance_no'), #Dummy to enable get_mark_url method
    url(r'^delete_tutee_meeting/$', 'na', name='delete_tutee_meeting_no'), #Dummy to enable get_mark_url method
    url(r'^remove_student_from_module/(\w+)/(\d{4})/$', 'na', name = 'generic_remove_student_from_module'),
    url(r'^export_anonymous_exam_marks/$', 'na', name='export_anonymous_exam_marks_year') #Dummy to enable get_mark_url method
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
    url(r'^delete_module/(\w+)/(\d{4})/$', 'delete_module', name = 'delete_module'),
    url(r'^remove_student_from_module/(\w+)/(\d{4})/(\w+)/$', 'remove_student_from_module', name = 'remove_student_from_module'),
    url(r'^mark/(\w+)/(\d{4})/(\w+)/$', 'mark', name = 'mark'),
    url(r'^seminar_groups/(\w+)/(\d{4})/$', 'seminar_groups', name = 'seminar_groups'),
    url(r'^attendance/(\w+)/(\d{4})/(\w+)/$', 'attendance', name = 'attendance'),
    url(r'^year/(\w+)/$', 'year_view', name = 'year_view'),
    url(r'^upload_csv/$', 'upload_csv', name = 'upload_csv'),
    url(r'^parse_csv/$', 'parse_csv', name = 'parse_csv'),
    url(r'^import_success/$', 'import_success', name = 'import_success'),
    url(r'^tutee_list/$', 'tutee_list', name='tutee_list'),
    url(r'^tutee/(\w+)/$', 'tutee_edit', name='tutee_edit'),
    url(r'^tutee/(\w+)/(\d+)/$', 'tutee_edit', name='edit_tutee_meeting'),
    url(r'^delete_tutee_meeting/(\d+)/$', 'delete_tutee_meeting', name='delete_tutee_meeting'),
    url(r'^seminar_group_overview/(\w+)/(\d{4})/$', 'seminar_group_overview', name='seminar_group_overview'),
)

urlpatterns += patterns('export.views',
    url(r'^export_attendance_sheet/(\w+)/(\d+)/$', 'export_attendance_sheet', name = 'export_attendance_sheet'),
    url(r'^export_anonymous_exam_marks/(\d+)/$', 'export_anonymous_exam_marks', name = 'export_anonymous_exam_marks'),
    url(r'^export_marks/(\w+)/(\d+)/$', 'export_marks', name = 'export_marks'),
    url(r'^export_feedback_sheet/(\w+)/(\d{4})/(\d{1})/(\w+)$', 'export_feedback_sheet', name = 'export_feedback_sheet'),

)

urlpatterns += patterns('anonymous_marking.views',
    url(r'^upload_anon_ids/$', 'upload_anon_ids', name = 'upload_anon_ids'),
    url(r'^edit_anon_ids/$', 'edit_anon_ids', name = 'edit_anon_ids'),
    url(r'^mark_anonymously/(\w+)/(\d{4})/(\w+)/$', 'mark_anonymously', name = 'mark_anonymously'),
    url(r'^write_anonymous_marks_to_db/(\w+)/$', 'write_anonymous_marks_to_db', name = 'write_anonymous_marks_to_db'),
    url(r'^anonymous_marking_admin/$', 'anonymous_marking_admin', name = 'anonymous_marking_admin'),
)

urlpatterns += patterns('feedback.views',
    url(r'^essay_feedback/(\w+)/(\d{4})/(\d{1})/(\w+)$', 'edit_essay_feedback', name = 'edit_essay_feedback'),
    url(r'^essay_feedback/$', 'add_essay_feedback', name = 'add_essay_feedback')
)

