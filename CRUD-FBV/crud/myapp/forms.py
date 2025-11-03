from django import forms
from .models import User
from django.core import validators # built-in-validator import

class StudentRegistration(forms.ModelForm):
    # name = forms.CharField(max_length=200) # first prayoti  
    # confirm_password = forms.CharField(max_length=200) # you can also use extra filds note mention in models.py and this data dose not save in database
    class Meta:
        model = User
        fields = ['name', 'email', 'password']
        # fields = '__all__' 
        # exclude = ['name'] # if you dont use name. you can use exclude 
        labels = {'name' : 'Enter Name', 'email' : 'Enter Email'}
        error_messages = {
            'name' : {'required':'Name Is Required...'},
            'email' : {'required':'Email Is Required...'},
            'password' : {'required':'Password Is Required...'}
        }
        widgets = { 
            'name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter your name'}), 
            'email': forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Enter your email'}),
            'password': forms.PasswordInput(render_value=True, attrs={'class':'form-control', 'placeholder':'Enter your password'}),  
        }
        
    # custom validators
    # Name validation
    def clean_name(self):
        name_value = self.cleaned_data.get('name')
        if name_value and len(name_value) < 4:
            raise forms.ValidationError("Name must be at least 4 characters long.")
        return name_value

    # Email validation
    def clean_email(self):
        email_value = self.cleaned_data.get('email')
        if email_value and len(email_value) < 15:
            raise forms.ValidationError("Email must be at least 15 characters long.")
        # Check if email already exists
        if User.objects.filter(email=email_value).exists():
            raise forms.ValidationError("This email is already registered.")
        return email_value

    # Password validation
    def clean_password(self):
        password_value = self.cleaned_data.get('password')
        if password_value and len(password_value) < 6:
            raise forms.ValidationError("Password must be at least 6 characters long.")
        return password_value
    
    # another way to add validator
    # def clean(self):
    #     cleaned_data = super().clean()
    #     name_value = cleaned_data.get('name')
    #     email_value = cleaned_data.get('email')
    #     password_value = cleaned_data.get('password')
            
    #     if name_value and len(name_value) < 4:
    #         self.add_error('name', 'Enter more than or equal 4 char...')
                
    #     if email_value and len(email_value) < 10:
    #         self.add_error('email', 'Enter more than or equal 10 char...')
                
    #     return cleaned_data
    