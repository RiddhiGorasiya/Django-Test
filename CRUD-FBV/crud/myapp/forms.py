from django import forms
from .models import User

class StudentRegistration(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'password']
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control'}),
            'email': forms.EmailInput(attrs={'class':'form-control'}),
            'password': forms.PasswordInput(render_value=True, attrs={'class':'form-control'}),  
        }
        # def clean_name(self):
        #     name_value = self.changed_data['name']
        #     if len(name_value) < 4:
        #         raise forms.ValidationError('Enter more than or equal 4 char')
        #     return name_value
        def clean(self):
            cleaned_data = super().clean()
            name_value = cleaned_data.get('name')
            email_value = cleaned_data.get('email')
            password_value = cleaned_data.get('password')
            
            if name_value and len(name_value) < 4:
                self.add_error('name', 'Enter more than or equal 4 char...')
                
            if email_value and len(email_value) < 10:
                self.add_error('email', 'Enter more than or equal 10 char...')
                
            return cleaned_data