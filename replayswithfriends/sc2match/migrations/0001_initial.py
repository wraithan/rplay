# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Player'
        db.create_table('sc2match_player', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
            ('username', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('battle_net_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('region', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
        ))
        db.send_create_signal('sc2match', ['Player'])

        # Adding unique constraint on 'Player', fields ['username', 'battle_net_url']
        db.create_unique('sc2match_player', ['username', 'battle_net_url'])

        # Adding model 'PlayerResult'
        db.create_table('sc2match_playerresult', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(related_name='matches', to=orm['sc2match.Player'])),
            ('match', self.gf('django.db.models.fields.related.ForeignKey')(related_name='players', to=orm['sc2match.Match'])),
            ('result', self.gf('django.db.models.fields.NullBooleanField')(default=None, null=True, blank=True)),
            ('color', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('random', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('race', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('is_observer', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('sc2match', ['PlayerResult'])

        # Adding model 'Map'
        db.create_table('sc2match_map', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('map_file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('region', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0)),
        ))
        db.send_create_signal('sc2match', ['Map'])

        # Adding model 'Match'
        db.create_table('sc2match_match', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')()),
            ('replay_file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('mapfield', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sc2match.Map'], null=True)),
            ('duration', self.gf('django.db.models.fields.PositiveIntegerField')(null=True)),
            ('gateway', self.gf('django.db.models.fields.CharField')(default='us', max_length=32)),
            ('processed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('match_share', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=1)),
        ))
        db.send_create_signal('sc2match', ['Match'])

    def backwards(self, orm):
        # Removing unique constraint on 'Player', fields ['username', 'battle_net_url']
        db.delete_unique('sc2match_player', ['username', 'battle_net_url'])

        # Deleting model 'Player'
        db.delete_table('sc2match_player')

        # Deleting model 'PlayerResult'
        db.delete_table('sc2match_playerresult')

        # Deleting model 'Map'
        db.delete_table('sc2match_map')

        # Deleting model 'Match'
        db.delete_table('sc2match_match')

    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'sc2match.map': {
            'Meta': {'object_name': 'Map'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'map_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'region': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'})
        },
        'sc2match.match': {
            'Meta': {'ordering': "['-modified']", 'object_name': 'Match'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'duration': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'gateway': ('django.db.models.fields.CharField', [], {'default': "'us'", 'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'mapfield': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sc2match.Map']", 'null': 'True'}),
            'match_share': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'processed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'replay_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        },
        'sc2match.player': {
            'Meta': {'unique_together': "(['username', 'battle_net_url'],)", 'object_name': 'Player'},
            'battle_net_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'region': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        'sc2match.playerresult': {
            'Meta': {'object_name': 'PlayerResult'},
            'color': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_observer': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'match': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'players'", 'to': "orm['sc2match.Match']"}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'matches'", 'to': "orm['sc2match.Player']"}),
            'race': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'random': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'result': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['sc2match']