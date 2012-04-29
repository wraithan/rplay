from django.forms import ModelForm
from .models import Match


class MatchUploadForm(ModelForm):

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(MatchUploadForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        commit = kwargs.get('commit', True)
        match = super(MatchUploadForm, self).save(commit=False)
        match.owner = self.user
        if commit:
            match.save()
        print "werp"
        return match

    class Meta:
        model = Match
        fields = ['replay_file']

