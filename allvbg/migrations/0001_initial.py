# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'MapStyle'
        db.create_table('allvbg_mapstyle', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('value', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('allvbg', ['MapStyle'])

        # Adding model 'tst_r'
        db.create_table('allvbg_tst_r', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('rating_votes', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, blank=True)),
            ('rating_score', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
        ))
        db.send_create_signal('allvbg', ['tst_r'])

        # Adding model 'Firm'
        db.create_table('allvbg_firm', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('name_ru', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('name_en', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('alias', self.gf('django.db.models.fields.CharField')(max_length=50, unique=True)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(related_name='children', blank=True, null=True, to=orm['allvbg.Firm'])),
            ('container', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('short', self.gf('tinymce.models.HTMLField')(null=True, blank=True)),
            ('short_ru', self.gf('tinymce.models.HTMLField')(null=True, blank=True)),
            ('short_en', self.gf('tinymce.models.HTMLField')(null=True, blank=True)),
            ('description', self.gf('tinymce.models.HTMLField')(null=True, blank=True)),
            ('description_ru', self.gf('tinymce.models.HTMLField')(null=True, blank=True)),
            ('description_en', self.gf('tinymce.models.HTMLField')(null=True, blank=True)),
            ('image1', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('image2', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('image3', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('image4', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('meta_key', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=100, null=True, blank=True)),
            ('map_style', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['allvbg.MapStyle'], null=True, blank=True)),
            ('isstore', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('ecwid', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('totalvotes', self.gf('django.db.models.fields.BigIntegerField')(null=True)),
            ('raiting', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('rating_votes', self.gf('django.db.models.fields.PositiveIntegerField')(default=0, blank=True)),
            ('rating_score', self.gf('django.db.models.fields.IntegerField')(default=0, blank=True)),
            ('lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            ('level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal('allvbg', ['Firm'])

        # Adding model 'Event'
        db.create_table('allvbg_event', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50, unique=True)),
            ('name_ru', self.gf('django.db.models.fields.CharField')(max_length=50, unique=True, null=True, blank=True)),
            ('name_en', self.gf('django.db.models.fields.CharField')(max_length=50, unique=True, null=True, blank=True)),
            ('short', self.gf('tinymce.models.HTMLField')()),
            ('short_ru', self.gf('tinymce.models.HTMLField')(null=True, blank=True)),
            ('short_en', self.gf('tinymce.models.HTMLField')(null=True, blank=True)),
            ('description', self.gf('tinymce.models.HTMLField')()),
            ('description_ru', self.gf('tinymce.models.HTMLField')(null=True, blank=True)),
            ('description_en', self.gf('tinymce.models.HTMLField')(null=True, blank=True)),
            ('start_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('end_date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('allvbg', ['Event'])

        # Adding model 'Article'
        db.create_table('allvbg_article', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50, unique=True)),
            ('short', self.gf('tinymce.models.HTMLField')()),
            ('description', self.gf('tinymce.models.HTMLField')()),
            ('meta_key', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('pub_date', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('allvbg', ['Article'])


    def backwards(self, orm):
        
        # Deleting model 'MapStyle'
        db.delete_table('allvbg_mapstyle')

        # Deleting model 'tst_r'
        db.delete_table('allvbg_tst_r')

        # Deleting model 'Firm'
        db.delete_table('allvbg_firm')

        # Deleting model 'Event'
        db.delete_table('allvbg_event')

        # Deleting model 'Article'
        db.delete_table('allvbg_article')


    models = {
        'allvbg.article': {
            'Meta': {'object_name': 'Article'},
            'description': ('tinymce.models.HTMLField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meta_key': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'unique': 'True'}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {}),
            'short': ('tinymce.models.HTMLField', [], {})
        },
        'allvbg.event': {
            'Meta': {'object_name': 'Event'},
            'description': ('tinymce.models.HTMLField', [], {}),
            'description_en': ('tinymce.models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'description_ru': ('tinymce.models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'unique': 'True'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '50', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'name_ru': ('django.db.models.fields.CharField', [], {'max_length': '50', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'short': ('tinymce.models.HTMLField', [], {}),
            'short_en': ('tinymce.models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'short_ru': ('tinymce.models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {})
        },
        'allvbg.firm': {
            'Meta': {'object_name': 'Firm'},
            'alias': ('django.db.models.fields.CharField', [], {'max_length': '50', 'unique': 'True'}),
            'container': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('tinymce.models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'description_en': ('tinymce.models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'description_ru': ('tinymce.models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'ecwid': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image1': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'image2': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'image3': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'image4': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'isstore': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'map_style': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['allvbg.MapStyle']", 'null': 'True', 'blank': 'True'}),
            'meta_key': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'name_en': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'name_ru': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'related_name': "'children'", 'blank': 'True', 'null': 'True', 'to': "orm['allvbg.Firm']"}),
            'pub_date': ('django.db.models.fields.DateTimeField', [], {}),
            'raiting': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'rating_score': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'rating_votes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True'}),
            'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'short': ('tinymce.models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'short_en': ('tinymce.models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'short_ru': ('tinymce.models.HTMLField', [], {'null': 'True', 'blank': 'True'}),
            'totalvotes': ('django.db.models.fields.BigIntegerField', [], {'null': 'True'}),
            'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        'allvbg.mapstyle': {
            'Meta': {'object_name': 'MapStyle'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'value': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'allvbg.tst_r': {
            'Meta': {'object_name': 'tst_r'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'rating_score': ('django.db.models.fields.IntegerField', [], {'default': '0', 'blank': 'True'}),
            'rating_votes': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'blank': 'True'})
        }
    }

    complete_apps = ['allvbg']
