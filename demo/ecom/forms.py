from django import forms
from django.contrib.auth.models import User
from .models import Item,UserProfile,OrderItem

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'price']

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()
    address = forms.CharField(max_length=255)

    class Meta:
        model = User
        fields = ['username', 'email', 'address', 'password']

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
            # Create user profile with the email and address
            UserProfile.objects.create(user=user, email=self.cleaned_data.get('email'), address=self.cleaned_data.get('address'))
        return user

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['email', 'address']

class OrderForm(forms.Form):
    items = forms.ModelMultipleChoiceField(queryset=Item.objects.all(), widget=forms.CheckboxSelectMultiple)
    quantities = forms.IntegerField(min_value=1, initial=1)