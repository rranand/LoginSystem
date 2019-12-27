from django import forms
from LoginPortal.models import info, file_handler
from django.contrib.auth.models import User
import re


class basic_detail(forms.ModelForm, forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(), min_length=6,
                               help_text='<ul><li>Password must be between 6 and 20</l1><li>Password should not '
                                         'contain =, :, ^, %, \', \"</l1></ul> ')
    v_password = forms.CharField(widget=forms.PasswordInput(), min_length=6, label='Verify Password')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')

    def clean(self):
        all_clean = super().clean()
        password = all_clean['password']
        verify = all_clean['v_password']

        if bool(re.search('[=:^%]{1,}', str(password))):
            raise forms.ValidationError('Password is invalid')
        elif bool(re.search('[=:^%]{1,}', str(verify))):
            raise forms.ValidationError('Password is invalid')
        elif str(password) != (verify):
            raise forms.ValidationError('Password doesn\'t matched')


class more_detail(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(), help_text='Write about yourself', empty_value=True)

    class Meta:
        model = info
        fields = ('mobile', 'profile_pic', 'description', 'city', 'state', 'country')

    def clean(self):
        all_clean = super().clean()
        number = all_clean['mobile']

        if not bool(re.search('[\d]{10}', str(number))):
            raise forms.ValidationError('Mobile number is not valid')
        else:
            if bool(info.objects.filter(mobile=number).exists()):
                raise forms.ValidationError('Mobile number is already registered')


class login_form(forms.Form):
    username = forms.CharField(max_length=150, label='Username: ', empty_value=False)
    password = forms.CharField(widget=forms.PasswordInput(), label='Password: ', empty_value=False)


class change_password(forms.Form):
    current = forms.CharField(widget=forms.PasswordInput(), label='Enter Current Password:', empty_value=True)
    new_password = forms.CharField(widget=forms.PasswordInput(), label='Enter New Password:',
                                   help_text='<p align="center">Password must be between 6 and '
                                             '20<br>Password should not '
                                             'contain =, :, ^, %, \', \"</p> ',
                                   empty_value=True)
    v_new_password = forms.CharField(widget=forms.PasswordInput(), label='Re-enter New Password:', empty_value=True)

    def clean(self):
        all_clean = super().clean()

        cur = all_clean['current']
        pass1 = all_clean['new_password']
        pass2 = all_clean['v_new_password']

        for i in [cur, pass1, pass2]:
            if bool(re.search('[=:^%]{1,}', str(i))):
                raise forms.ValidationError('Password is invalid')


class search(forms.Form):
    search_profile = forms.CharField(label='Enter:', min_length=4, max_length=150, help_text='<p>Search by '
                                                                                             'Email id, Mobile Number, '
                                                                                             'or Name</p> ')


class otp_authentication(forms.Form):
    key = forms.CharField(max_length=6, min_length=6, label='Enter OTP:', empty_value=True)


class files_handler(forms.ModelForm):
    class Meta:
        model = file_handler
        fields = ('files',)
        widgets = {
            'files': forms.FileInput(attrs={'multiple': True}),
        }


class recover_password(forms.Form):
    username = forms.CharField(max_length=150, label='Enter your username:')
    mobile = forms.CharField(max_length=10, label='Enter your mobile number:')
    email = forms.EmailField(label='Enter your email id:')
