from django.forms import *
from tasklist.models import *
from django.forms import ModelForm


#new email authenticated user creation form
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    email = EmailField(label='Email address', max_length = 75)
    password1 = CharField(label='Password', widget=PasswordInput()) 
    
    class Meta:
        model = User
        fields = ('username', 'email',)
    
    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            user = User.objects.get(email=email)
            raise forms.ValidationError("This email address already exists. Did you forget your password?")
        except User.DoesNotExist:
            return email
        
    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["email"]
        user.is_active = True # change to false if using email activation
        if commit:
            user.save()
            
        return user




class TasklistForm(ModelForm):
  class Meta:
    model = Tasklist
    exclude = ('user',)




class ListitemForm(ModelForm):
  class Meta:
    model = Listitem
    exclude = ('tasklist','complete','completed_on', 'deleted', 'deleted_on')