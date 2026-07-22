from django import forms
from django.contrib.auth import get_user_model
from .models import School

User = get_user_model()

class SchoolRegistrationForm(forms.ModelForm):
    # School Fields
    name = forms.CharField(label="School Name", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter school name'}))
    slug = forms.SlugField(label="URL Slug", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. oxford-international'}))
    
    # Admin User Fields
    admin_email = forms.EmailField(label="Admin Email", widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'admin@school.com'}))
    admin_password = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = School
        fields = ['name', 'slug', 'address', 'contact_phone']
        widgets = {
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'School address'}),
            'contact_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact phone'}),
        }

    def save(self, commit=True):
        school = super().save(commit=False)
        school.contact_email = self.cleaned_data['admin_email']
        if commit:
            school.save()
            # Create the Admin User
            user = User.objects.create_user(
                username=self.cleaned_data['admin_email'],
                email=self.cleaned_data['admin_email'],
                password=self.cleaned_data['admin_password'],
                role='admin',
                school=school
            )
            # Here we could link the user to the school if we had a many-to-many or profile link
            # For now, we'll assume the school admin is the one who created the school
        return school
