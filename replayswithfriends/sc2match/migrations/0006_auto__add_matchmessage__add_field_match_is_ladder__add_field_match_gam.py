# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MatchMessage'
        db.create_table('sc2match_matchmessage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('match', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sc2match.Match'])),
            ('player', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sc2match.PlayerResult'])),
            ('frame', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('flags', self.gf('django.db.models.fields.IntegerField')()),
            ('to_all', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('to_allies', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('message', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal('sc2match', ['MatchMessage'])

        # Adding field 'Match.is_ladder'
        db.add_column('sc2match_match', 'is_ladder',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'Match.game_played_on'
        db.add_column('sc2match_match', 'game_played_on',
                      self.gf('django.db.models.fields.DateTimeField')(null=True),
                      keep_default=False)

        # Adding field 'Match.game_type'
        db.add_column('sc2match_match', 'game_type',
                      self.gf('django.db.models.fields.CharField')(default=True, max_length=64, blank=True),
                      keep_default=False)

        # Adding field 'Match.game_speed'
        db.add_column('sc2match_match', 'game_speed',
                      self.gf('django.db.models.fields.CharField')(default=True, max_length=64, blank=True),
                      keep_default=False)

        # Adding field 'PlayerResult.pid'
        db.add_column('sc2match_playerresult', 'pid',
                      self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0),
                      keep_default=False)

        # Adding field 'PlayerResult.is_human'
        db.add_column('sc2match_playerresult', 'is_human',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'PlayerResult.difficulty'
        db.add_column('sc2match_playerresult', 'difficulty',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=64, blank=True),
                      keep_default=False)

        # Adding field 'PlayerResult.handicap'
        db.add_column('sc2match_playerresult', 'handicap',
                      self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=100),
                      keep_default=False)


        # Changing field 'PlayerResult.player'
        db.alter_column('sc2match_playerresult', 'player_id', self.gf('django.db.models.fields.related.ForeignKey')(null=True, to=orm['sc2match.Player']))
    def backwards(self, orm):
        # Deleting model 'MatchMessage'
        db.delete_table('sc2match_matchmessage')

        # Deleting field 'Match.is_ladder'
        db.delete_column('sc2match_match', 'is_ladder')

        # Deleting field 'Match.game_played_on'
        db.delete_column('sc2match_match', 'game_played_on')

        # Deleting field 'Match.game_type'
        db.delete_column('sc2match_match', 'game_type')

        # Deleting field 'Match.game_speed'
        db.delete_column('sc2match_match', 'game_speed')

        # Deleting field 'PlayerResult.pid'
        db.delete_column('sc2match_playerresult', 'pid')

        # Deleting field 'PlayerResult.is_human'
        db.delete_column('sc2match_playerresult', 'is_human')

        # Deleting field 'PlayerResult.difficulty'
        db.delete_column('sc2match_playerresult', 'difficulty')

        # Deleting field 'PlayerResult.handicap'
        db.delete_column('sc2match_playerresult', 'handicap')


        # User chose to not deal with backwards NULL issues for 'PlayerResult.player'
        raise RuntimeError("Cannot reverse this migration. 'PlayerResult.player' and its values cannot be restored.")
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
            'maphash': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'region': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'})
        },
        'sc2match.match': {
            'Meta': {'ordering': "['-modified']", 'unique_together': "(['owner', 'matchhash'],)", 'object_name': 'Match'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'duration': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True'}),
            'game_played_on': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'game_speed': ('django.db.models.fields.CharField', [], {'default': 'True', 'max_length': '64', 'blank': 'True'}),
            'game_type': ('django.db.models.fields.CharField', [], {'default': 'True', 'max_length': '64', 'blank': 'True'}),
            'gateway': ('django.db.models.fields.CharField', [], {'default': "'us'", 'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_ladder': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'mapfield': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sc2match.Map']", 'null': 'True'}),
            'match_share': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '1'}),
            'matchhash': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '512', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'process_error': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'processed': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'replay_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        },
        'sc2match.matchmessage': {
            'Meta': {'ordering': "['match', 'frame']", 'object_name': 'MatchMessage'},
            'flags': ('django.db.models.fields.IntegerField', [], {}),
            'frame': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'match': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sc2match.Match']"}),
            'message': ('django.db.models.fields.TextField', [], {}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sc2match.PlayerResult']"}),
            'to_all': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'to_allies': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
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
            'difficulty': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '64', 'blank': 'True'}),
            'handicap': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_human': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_observer': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'match': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'players'", 'to': "orm['sc2match.Match']"}),
            'pid': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0'}),
            'player': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'matches'", 'null': 'True', 'to': "orm['sc2match.Player']"}),
            'race': ('django.db.models.fields.CharField', [], {'max_length': '8', 'blank': 'True'}),
            'random': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'result': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['sc2match']