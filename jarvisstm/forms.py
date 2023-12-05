# -*- coding: utf-8 -*-
from django import forms

# from .models import Snippet
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

from jarvis.db.jsonutils import loadjson
import os

opts = loadjson(os.path.join(os.path.dirname(__file__), "all_stm.json"))
choices = []
for i in opts:
    choices.append((i, i))


bias_types = ["Positive", "Negative"]
choices2 = []
for i in bias_types:
    choices2.append((i, i))

stm_types = ["Constant height", "Constant current"]
choices3 = []
for i in stm_types:
    choices3.append((i, i))


class ContactForm(forms.Form):
    # def __init__(self,body='',results='',*args, **kwargs):
    #    self.body=body
    #    self.results=results
    # category =forms.ChoiceField(choices=[('question','Question'),('other','Other'),('ola','ola')])
    material = forms.ChoiceField(choices=choices)
    bias_type = forms.ChoiceField(choices=choices2)
    stm_type = forms.ChoiceField(choices=choices3)
    min_size = forms.FloatField(required=False)
    zcut = forms.FloatField(required=False)
    ext = forms.FloatField(required=False)
    """
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields["min_size"].value = 50.0
        self.fields["ext"].value = 0.15
    """

    # print('category1',category1)
    # print('category2',category2)
    # def __init__(self, *args, **kwargs):
    #     super(ContactForm, self).__init__(*args, **kwargs)
    #     self.fields["category1"].label = "Select Material"
    #     self.fields["category2"].label = "Select Material"
    # def __init__(self, *args, **kwargs):
    #                super(ContactForm, self).__init__(*args, **kwargs)
    #                self.fields['category'].label = ""

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
               #'body',
               #'results',
               kpoints,
               category,
               Submit('submit','Submit', css_class='btn-success')
               )
    """
