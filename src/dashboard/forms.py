from django import forms
from guilds.models import Roles


class RoleFilterForm(forms.Form):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False,
        label="Начальная дата")
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False,
        label="Конечная дата")
    roles = forms.ModelMultipleChoiceField(
        queryset=Roles.objects.filter(name__in=['Diablo 2', 'Diablo IV']),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Роли"
    )
