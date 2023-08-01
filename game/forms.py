from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100,widget=forms.TextInput(
        attrs={'class':'form-control bg-warning','placeholder':'Enter Username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class':'form-control bg-warning','placeholder':'Enter Password'}))

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100,widget=forms.TextInput(
        attrs={'class':'form-control bg-warning','placeholder':'Enter Username'}))
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class':'form-control bg-warning','placeholder':'Create Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'class':'form-control bg-warning','placeholder':'Confirm Password'}))
    email = forms.EmailField(max_length=100,required=False,widget=forms.EmailInput(
        attrs={'class':'form-control bg-warning','placeholder':'Enter E-mail (optional)'}))