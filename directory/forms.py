from django import forms
from directory.models import User, Project, Cohort


class ProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'avatar',
            'looking_for_job',
            'specialities',
            'interests',
        ]


class NewStudentForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'avatar']
