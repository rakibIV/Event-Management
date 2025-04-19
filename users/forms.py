from django import forms
from django.contrib.auth.models import Group
import re

from django.contrib.auth import get_user_model
User = get_user_model()

class StyledFormMixin:
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_styled_widgets()
        
    default_classes = "w-full p-3 border rounded border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 m-3 mb-5"
    
    def apply_styled_widgets(self):
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({
                    "class": self.default_classes,
                    "placeholder": f"{field.label}"
                })
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({
                    "class": self.default_classes,
                    "placeholder": f"{field.label}",
                    "rows": 5
                })
            elif isinstance(field.widget, forms.SelectDateWidget):
                field.widget.attrs.update({
                    "class": "border border-gray-300 p-3 rounded-lg shadow-md mb-5 focus:shadow-blue-300 focus:outline-blue-300 m-2 cursor-pointer"
                })
                
            elif isinstance(field.widget, forms.TimeInput):
                field.widget.attrs.update({
                    "type": "time",
                    "class": "border border-gray-300 w-18 p-2 rounded-lg shadow-md mb-5 focus:shadow-blue-300 focus:outline-blue-300 cursor-pointer"
                })
                
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({
                    "class": "space-y-2 mt-3"
                })
                
            elif isinstance(field.widget,forms.EmailInput):
                field.widget.attrs.update({
                    "class": self.default_classes,
                    "placeholder": f"{field.label}"
                })
            elif isinstance(field.widget,forms.PasswordInput):
                if field_name == "confirm_password":
                        field.widget.attrs.update({
                        "class": self.default_classes,
                        "placeholder": "Confirm Password",
                    })
                else:
                    field.widget.attrs.update({
                        "class": self.default_classes,
                        "placeholder": f"Password",
                    })
                
            else:
                field.widget.attrs.update({
                    "class": "border border-gray-300 p-3 rounded-lg shadow-md mb-5 focus:shadow-blue-300 focus:outline-blue-300 m-2"
                })

    
    
    
    
class CustomRegistrationForm(StyledFormMixin,forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username','first_name','last_name','password1','confirm_password','email']
        
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email is already exists')
        
        return email
        
        
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        errors = []
        
        if len(password1) < 8:
            errors.append('Password must be atleast 8 characters long')
        
        
        if not re.search(r'[A-Z]',password1):
            errors.append('Password must contain atleast one uppercase letter')
        
        if not re.search(r'[a-z]',password1):
            errors.append('Password must contain atleast one lowercase letter')
        
        if not re.search(r'[0-9]',password1):
            errors.append('Password must contain atleast one digit')
        
        if not re.search(r'[@#$%^&*]',password1):
            errors.append('Password must contain atleast one special character')
            
        if errors:
            raise forms.ValidationError(errors)
        
        return password1
        
        
    def clean(self):  #non field errors
        cleaned_data = super().clean()
        
        password1 = cleaned_data.get('password1')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password1 != confirm_password:
            raise forms.ValidationError("Password do not matched")
        
        return cleaned_data
    
    
class AssignRoleForm(forms.Form):
    role = forms.ModelChoiceField(queryset=Group.objects.all(), empty_label="Select Role")
    
    
    
    
from django import forms
from .models import CustomUser


class UserProfileForm(forms.ModelForm):
    """Form for updating user profile information."""
    
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 
                 'phone_number', 'address', 'bio', 'profile_image']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            'address': forms.Textarea(attrs={'rows': 3}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].required = True
        
    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        
        if not phone:
            return phone
            
        if phone.startswith('+880') and len(phone) == 14:
            return phone
            
        if not (phone.startswith('0') and len(phone) == 11):
            raise forms.ValidationError(
                "Phone number must be a valid Bangladeshi number starting with '01' and containing 11 digits."
            )
            
        return '+880' + phone[1:]