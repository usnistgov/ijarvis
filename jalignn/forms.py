# -*- coding: utf-8 -*-
from django import forms
#from .models import Snippet
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit


class ContactForm(forms.Form):
    # def __init__(self,body='',results='',*args, **kwargs):
    #    self.body=body
    #    self.results=results
    body = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 15, "cols": 50, "class": "box1"})
    )
    def __init__(self, *args, **kwargs):
                    super(ContactForm, self).__init__(*args, **kwargs)
                    self.fields['body'].label = "" 

    # results=forms.CharField(widget=forms.Textarea(attrs={'rows': 15, 'cols': 40}),required=False)
    # name=forms.CharField()
    # email=forms.EmailField(label='E-mail')
    # category =forms.ChoiceField(choices=[('question','Question'),('other','Other')])
    # subject =forms.CharField(required=False)
    """
   def __init__(self, *args, **kwargs):
       super().__init__(*args, **kwargs)
       self.helper = FormHelper
       self.helper.form_method = 'post'
       self.helper.layout = Layout(
               #'name',
               #'email',
               #'category',
               #'subject',
               'body',
               'results',
               Submit('submit','Submit', css_class='btn-success')
               )
   """
