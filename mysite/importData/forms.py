from django import forms
from inspection.models import IDCPostion,userAdmin

class DataForm(forms.Form):
    IDCPostionlist = IDCPostion.objects.order_by('id')
    choices = []
    # userAdminlist = userAdmin.objects.order_by('id')
    for IDCPostion in IDCPostionlist:
        choices.append((IDCPostion.id , IDCPostion.IDCPostionName))

    IDCPostionChoice = forms.ChoiceField(choices=choices)
    # userAdminChoice = forms.MultipleChoiceField(label='userAdminChoice')

    # MultipleChoiceField

