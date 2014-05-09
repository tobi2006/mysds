# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MetaData'
        db.create_table(u'database_metadata', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('data_id', self.gf('django.db.models.fields.IntegerField')(default=1, unique=True)),
            ('current_year', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'database', ['MetaData'])

        # Adding model 'Course'
        db.create_table(u'database_course', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
        ))
        db.send_create_signal(u'database', ['Course'])

        # Adding model 'Module'
        db.create_table(u'database_module', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('year', self.gf('django.db.models.fields.IntegerField')(default=2013)),
            ('successor_of', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['database.Module'], null=True, blank=True)),
            ('is_foundational', self.gf('django.db.models.fields.BooleanField')()),
            ('is_pg', self.gf('django.db.models.fields.BooleanField')()),
            ('is_nalp', self.gf('django.db.models.fields.BooleanField')()),
            ('credits', self.gf('django.db.models.fields.IntegerField')(default=20)),
            ('eligible', self.gf('django.db.models.fields.CharField')(default='1', max_length=3)),
            ('first_session', self.gf('django.db.models.fields.IntegerField')(default=5)),
            ('no_teaching_in', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('last_session', self.gf('django.db.models.fields.IntegerField')(default=15)),
            ('sessions_recorded', self.gf('django.db.models.fields.IntegerField')(default=0, null=True, blank=True)),
            ('assessment_1_title', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('assessment_1_value', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('assessment_1_type', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='assessment_1', null=True, to=orm['feedback.FeedbackCategories'])),
            ('assessment_1_available', self.gf('django.db.models.fields.BooleanField')()),
            ('assessment_1_submission_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('assessment_1_max_word_count', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('assessment_2_title', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('assessment_2_value', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('assessment_2_type', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='assessment_2', null=True, to=orm['feedback.FeedbackCategories'])),
            ('assessment_2_available', self.gf('django.db.models.fields.BooleanField')()),
            ('assessment_2_submission_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('assessment_2_max_word_count', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('assessment_3_title', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('assessment_3_value', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('assessment_3_type', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='assessment_3', null=True, to=orm['feedback.FeedbackCategories'])),
            ('assessment_3_available', self.gf('django.db.models.fields.BooleanField')()),
            ('assessment_3_submission_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('assessment_3_max_word_count', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('assessment_4_title', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('assessment_4_value', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('assessment_4_type', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='assessment_4', null=True, to=orm['feedback.FeedbackCategories'])),
            ('assessment_4_available', self.gf('django.db.models.fields.BooleanField')()),
            ('assessment_4_submission_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('assessment_4_max_word_count', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('assessment_5_title', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('assessment_5_value', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('assessment_5_type', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='assessment_5', null=True, to=orm['feedback.FeedbackCategories'])),
            ('assessment_5_available', self.gf('django.db.models.fields.BooleanField')()),
            ('assessment_5_submission_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('assessment_5_max_word_count', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('assessment_6_title', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('assessment_6_value', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('assessment_6_type', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='assessment_6', null=True, to=orm['feedback.FeedbackCategories'])),
            ('assessment_6_available', self.gf('django.db.models.fields.BooleanField')()),
            ('assessment_6_submission_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('assessment_6_max_word_count', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('exam_value', self.gf('django.db.models.fields.IntegerField')(default=60, null=True, blank=True)),
        ))
        db.send_create_signal(u'database', ['Module'])

        # Adding unique constraint on 'Module', fields ['code', 'year']
        db.create_unique(u'database_module', ['code', 'year'])

        # Adding M2M table for field instructors on 'Module'
        m2m_table_name = db.shorten_name(u'database_module_instructors')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('module', models.ForeignKey(orm[u'database.module'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['module_id', 'user_id'])

        # Adding model 'Student'
        db.create_table(u'database_student', (
            ('student_id', self.gf('django.db.models.fields.CharField')(max_length=25, primary_key=True)),
            ('exam_id', self.gf('django.db.models.fields.CharField')(default=None, max_length=25, unique=True, null=True, blank=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('belongs_to', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('since', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('year', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('is_part_time', self.gf('django.db.models.fields.BooleanField')()),
            ('second_part_time_year', self.gf('django.db.models.fields.BooleanField')()),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('course', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['database.Course'], null=True, blank=True)),
            ('qld', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('tutor', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='tutee', null=True, to=orm['auth.User'])),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('highlighted', self.gf('django.db.models.fields.BooleanField')()),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('lsp', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('permanent_email', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('address', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('phone_no', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('home_address', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('nalp', self.gf('django.db.models.fields.BooleanField')()),
            ('tier_4', self.gf('django.db.models.fields.BooleanField')()),
            ('achieved_degree', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('problems', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'database', ['Student'])

        # Adding M2M table for field modules on 'Student'
        m2m_table_name = db.shorten_name(u'database_student_modules')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('student', models.ForeignKey(orm[u'database.student'], null=False)),
            ('module', models.ForeignKey(orm[u'database.module'], null=False))
        ))
        db.create_unique(m2m_table_name, ['student_id', 'module_id'])

        # Adding model 'Performance'
        db.create_table(u'database_performance', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('student', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['database.Student'])),
            ('module', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['database.Module'])),
            ('seminar_group', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('group_assessment_group', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('assessment_1', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('assessment_2', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('assessment_3', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('assessment_4', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('assessment_5', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('assessment_6', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('exam', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('r_assessment_1', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('r_assessment_2', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('r_assessment_3', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('r_assessment_4', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('r_assessment_5', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('r_assessment_6', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('r_exam', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('assessment_1_is_sit', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('assessment_2_is_sit', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('assessment_3_is_sit', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('assessment_4_is_sit', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('assessment_5_is_sit', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('assessment_6_is_sit', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('exam_is_sit', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('q_assessment_1', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('q_assessment_2', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('q_assessment_3', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('q_assessment_4', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('q_assessment_5', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('q_assessment_6', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('q_exam', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('assessment_1_modified', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('assessment_2_modified', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('assessment_3_modified', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('assessment_4_modified', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('assessment_5_modified', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('assessment_6_modified', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('exam_modified', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('r_assessment_1_modified', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('r_assessment_2_modified', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('r_assessment_3_modified', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('r_assessment_4_modified', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('r_assessment_5_modified', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('r_assessment_6_modified', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('r_exam_modified', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('q_assessment_1_modified', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('q_assessment_2_modified', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('q_assessment_3_modified', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('q_assessment_4_modified', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('q_assessment_5_modified', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('q_assessment_6_modified', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('q_exam_modified', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('average', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('real_average', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('part_of_average', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('attendance', self.gf('django.db.models.fields.CharField')(max_length=50, blank=True)),
            ('notes', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'database', ['Performance'])

        # Adding unique constraint on 'Performance', fields ['student', 'module']
        db.create_unique(u'database_performance', ['student_id', 'module_id'])

        # Adding model 'Tutee_Session'
        db.create_table(u'database_tutee_session', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('tutee', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['database.Student'])),
            ('tutor', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('date_of_meet', self.gf('django.db.models.fields.DateField')()),
            ('notes', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'database', ['Tutee_Session'])


    def backwards(self, orm):
        # Removing unique constraint on 'Performance', fields ['student', 'module']
        db.delete_unique(u'database_performance', ['student_id', 'module_id'])

        # Removing unique constraint on 'Module', fields ['code', 'year']
        db.delete_unique(u'database_module', ['code', 'year'])

        # Deleting model 'MetaData'
        db.delete_table(u'database_metadata')

        # Deleting model 'Course'
        db.delete_table(u'database_course')

        # Deleting model 'Module'
        db.delete_table(u'database_module')

        # Removing M2M table for field instructors on 'Module'
        db.delete_table(db.shorten_name(u'database_module_instructors'))

        # Deleting model 'Student'
        db.delete_table(u'database_student')

        # Removing M2M table for field modules on 'Student'
        db.delete_table(db.shorten_name(u'database_student_modules'))

        # Deleting model 'Performance'
        db.delete_table(u'database_performance')

        # Deleting model 'Tutee_Session'
        db.delete_table(u'database_tutee_session')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'database.course': {
            'Meta': {'object_name': 'Course'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'database.metadata': {
            'Meta': {'object_name': 'MetaData'},
            'current_year': ('django.db.models.fields.IntegerField', [], {}),
            'data_id': ('django.db.models.fields.IntegerField', [], {'default': '1', 'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'database.module': {
            'Meta': {'unique_together': "(('code', 'year'),)", 'object_name': 'Module'},
            'assessment_1_available': ('django.db.models.fields.BooleanField', [], {}),
            'assessment_1_max_word_count': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'assessment_1_submission_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'assessment_1_title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'assessment_1_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'assessment_1'", 'null': 'True', 'to': u"orm['feedback.FeedbackCategories']"}),
            'assessment_1_value': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'assessment_2_available': ('django.db.models.fields.BooleanField', [], {}),
            'assessment_2_max_word_count': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'assessment_2_submission_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'assessment_2_title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'assessment_2_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'assessment_2'", 'null': 'True', 'to': u"orm['feedback.FeedbackCategories']"}),
            'assessment_2_value': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'assessment_3_available': ('django.db.models.fields.BooleanField', [], {}),
            'assessment_3_max_word_count': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'assessment_3_submission_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'assessment_3_title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'assessment_3_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'assessment_3'", 'null': 'True', 'to': u"orm['feedback.FeedbackCategories']"}),
            'assessment_3_value': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'assessment_4_available': ('django.db.models.fields.BooleanField', [], {}),
            'assessment_4_max_word_count': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'assessment_4_submission_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'assessment_4_title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'assessment_4_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'assessment_4'", 'null': 'True', 'to': u"orm['feedback.FeedbackCategories']"}),
            'assessment_4_value': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'assessment_5_available': ('django.db.models.fields.BooleanField', [], {}),
            'assessment_5_max_word_count': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'assessment_5_submission_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'assessment_5_title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'assessment_5_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'assessment_5'", 'null': 'True', 'to': u"orm['feedback.FeedbackCategories']"}),
            'assessment_5_value': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'assessment_6_available': ('django.db.models.fields.BooleanField', [], {}),
            'assessment_6_max_word_count': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'assessment_6_submission_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'assessment_6_title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'assessment_6_type': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'assessment_6'", 'null': 'True', 'to': u"orm['feedback.FeedbackCategories']"}),
            'assessment_6_value': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'credits': ('django.db.models.fields.IntegerField', [], {'default': '20'}),
            'eligible': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '3'}),
            'exam_value': ('django.db.models.fields.IntegerField', [], {'default': '60', 'null': 'True', 'blank': 'True'}),
            'first_session': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'instructors': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'is_foundational': ('django.db.models.fields.BooleanField', [], {}),
            'is_nalp': ('django.db.models.fields.BooleanField', [], {}),
            'is_pg': ('django.db.models.fields.BooleanField', [], {}),
            'last_session': ('django.db.models.fields.IntegerField', [], {'default': '15'}),
            'no_teaching_in': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'sessions_recorded': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'successor_of': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['database.Module']", 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'year': ('django.db.models.fields.IntegerField', [], {'default': '2013'})
        },
        u'database.performance': {
            'Meta': {'ordering': "['module', 'student']", 'unique_together': "(('student', 'module'),)", 'object_name': 'Performance'},
            'assessment_1': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'assessment_1_is_sit': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'assessment_1_modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'assessment_2': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'assessment_2_is_sit': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'assessment_2_modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'assessment_3': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'assessment_3_is_sit': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'assessment_3_modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'assessment_4': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'assessment_4_is_sit': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'assessment_4_modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'assessment_5': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'assessment_5_is_sit': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'assessment_5_modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'assessment_6': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'assessment_6_is_sit': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'assessment_6_modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'attendance': ('django.db.models.fields.CharField', [], {'max_length': '50', 'blank': 'True'}),
            'average': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'exam': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'exam_is_sit': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'exam_modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'group_assessment_group': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'module': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['database.Module']"}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'part_of_average': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'q_assessment_1': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'q_assessment_1_modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'q_assessment_2': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'q_assessment_2_modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'q_assessment_3': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'q_assessment_3_modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'q_assessment_4': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'q_assessment_4_modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'q_assessment_5': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'q_assessment_5_modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'q_assessment_6': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'q_assessment_6_modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'q_exam': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'q_exam_modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'r_assessment_1': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'r_assessment_1_modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'r_assessment_2': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'r_assessment_2_modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'r_assessment_3': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'r_assessment_3_modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'r_assessment_4': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'r_assessment_4_modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'r_assessment_5': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'r_assessment_5_modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'r_assessment_6': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'r_assessment_6_modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'r_exam': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'r_exam_modified': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'real_average': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'seminar_group': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['database.Student']"})
        },
        u'database.student': {
            'Meta': {'ordering': "['last_name', 'first_name', 'year']", 'object_name': 'Student'},
            'achieved_degree': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'address': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'belongs_to': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'course': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['database.Course']", 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'exam_id': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '25', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'highlighted': ('django.db.models.fields.BooleanField', [], {}),
            'home_address': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'is_part_time': ('django.db.models.fields.BooleanField', [], {}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'lsp': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'modules': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['database.Module']", 'symmetrical': 'False', 'blank': 'True'}),
            'nalp': ('django.db.models.fields.BooleanField', [], {}),
            'notes': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'permanent_email': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'phone_no': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'problems': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'qld': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'second_part_time_year': ('django.db.models.fields.BooleanField', [], {}),
            'since': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'student_id': ('django.db.models.fields.CharField', [], {'max_length': '25', 'primary_key': 'True'}),
            'tier_4': ('django.db.models.fields.BooleanField', [], {}),
            'tutor': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'tutee'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'year': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        u'database.tutee_session': {
            'Meta': {'ordering': "['date_of_meet', 'tutor']", 'object_name': 'Tutee_Session'},
            'date_of_meet': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'notes': ('django.db.models.fields.TextField', [], {}),
            'tutee': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['database.Student']"}),
            'tutor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'feedback.feedbackcategories': {
            'Meta': {'object_name': 'FeedbackCategories'},
            'assessment_type': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'}),
            'category_1': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'category_1_helptext': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'category_2': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'category_2_helptext': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'category_3': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'category_3_helptext': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'category_4': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'category_4_helptext': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'category_5': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'category_5_helptext': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'category_6': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'category_6_helptext': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'category_7': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'category_7_helptext': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'category_8': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'category_8_helptext': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'group_component': ('django.db.models.fields.BooleanField', [], {}),
            'group_weight': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'individual_weight': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['database']