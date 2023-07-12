from django import forms

class ComposeForm(forms.Form):
    recipient = forms.CharField(label="Destinataire", max_length=255)
    # subject = forms.CharField(label="Sujet", max_length=255)
    body = forms.CharField(label="Corps du message", widget=forms.Textarea)
