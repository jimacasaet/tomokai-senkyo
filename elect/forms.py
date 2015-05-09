from django import forms
from elect.models import Position, Candidate, Vote
class VoteForm(forms.ModelForm):
    candidate = forms.IntegerField(widget=
    authstring = forms.CharField(max_length=128, help_text="Authenticate!")
    class Meta:
        model = Vote
        fields = ('authstring','candidate')