# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Marksheet'
        db.create_table(u'feedback_marksheet', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('module', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['database.Module'])),
            ('student', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['database.Student'])),
            ('assessment', self.gf('django.db.models.fields.IntegerField')()),
            ('marker', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='marker', null=True, to=orm['auth.User'])),
            ('second_first_marker', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='second_first_marker', null=True, to=orm['auth.User'])),
            ('second_marker', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='second_marker', null=True, to=orm['auth.User'])),
            ('marking_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('category_mark_1', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('category_mark_2', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('category_mark_3', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('category_mark_4', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('category_mark_5', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('category_mark_6', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('category_mark_7', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('category_mark_8', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('category_mark_1_free', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('category_mark_2_free', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('category_mark_3_free', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('category_mark_4_free', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('category_mark_5_free', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('category_mark_6_free', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('category_mark_7_free', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('category_mark_8_free', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('deduction', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('deduction_explanation', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('part_1_mark', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('part_2_mark', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('submission_date', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('comments', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('comments_2', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('group_component_mark', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('individual_component_mark', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('group_feedback', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'feedback', ['Marksheet'])

        # Adding unique constraint on 'Marksheet', fields ['student', 'module', 'assessment']
        db.create_unique(u'feedback_marksheet', ['student_id', 'module_id', 'assessment'])

        # Adding M2M table for field other_group_members on 'Marksheet'
        m2m_table_name = db.shorten_name(u'feedback_marksheet_other_group_members')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('marksheet', models.ForeignKey(orm[u'feedback.marksheet'], null=False)),
            ('student', models.ForeignKey(orm[u'database.student'], null=False))
        ))
        db.create_unique(m2m_table_name, ['marksheet_id', 'student_id'])

        # Adding model 'FeedbackCategories'
        db.create_table(u'feedback_feedbackcategories', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('assessment_type', self.gf('django.db.models.fields.CharField')(unique=True, max_length=30)),
            ('category_1', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('category_1_helptext', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('category_2', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('category_2_helptext', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('category_3', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('category_3_helptext', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('category_4', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('category_4_helptext', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('category_5', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('category_5_helptext', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('category_6', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('category_6_helptext', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('category_7', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('category_7_helptext', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('category_8', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('category_8_helptext', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('group_component', self.gf('django.db.models.fields.BooleanField')()),
            ('individual_weight', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('group_weight', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'feedback', ['FeedbackCategories'])


    def backwards(self, orm):
        # Removing unique constraint on 'Marksheet', fields ['student', 'module', 'assessment']
        db.delete_unique(u'feedback_marksheet', ['student_id', 'module_id', 'assessment'])

        # Deleting model 'Marksheet'
        db.delete_table(u'feedback_marksheet')

        # Removing M2M table for field other_group_members on 'Marksheet'
        db.delete_table(db.shorten_name(u'feedback_marksheet_other_group_members'))

        # Deleting model 'FeedbackCategories'
        db.delete_table(u'feedback_feedbackcategories')


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
        },
        u'feedback.marksheet': {
            'Meta': {'unique_together': "(('student', 'module', 'assessment'),)", 'object_name': 'Marksheet'},
            'assessment': ('django.db.models.fields.IntegerField', [], {}),
            'category_mark_1': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'category_mark_1_free': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'category_mark_2': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'category_mark_2_free': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'category_mark_3': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'category_mark_3_free': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'category_mark_4': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'category_mark_4_free': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'category_mark_5': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'category_mark_5_free': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'category_mark_6': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'category_mark_6_free': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'category_mark_7': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'category_mark_7_free': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'category_mark_8': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'category_mark_8_free': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'comments': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'comments_2': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'deduction': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'deduction_explanation': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'group_component_mark': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'group_feedback': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'individual_component_mark': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'marker': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'marker'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'marking_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'module': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['database.Module']"}),
            'other_group_members': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'group_marked_in'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['database.Student']"}),
            'part_1_mark': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'part_2_mark': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'second_first_marker': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'second_first_marker'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'second_marker': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'second_marker'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['database.Student']"}),
            'submission_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['feedback']