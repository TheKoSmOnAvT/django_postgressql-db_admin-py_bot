from django import forms
 
class UserForm(forms.Form):
    Query = forms.CharField()
    
   