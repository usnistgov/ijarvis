# -*- coding: utf-8 -*-
from django import forms

# from .models import Snippet
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

from jarvis.db.jsonutils import loadjson
import os

opts = loadjson(os.path.join(os.path.dirname(__file__), "het_options.json"))
choices = []
for i in opts:
    choices.append((i, i))
tmp_pos = "Mo1 Se2\n1.0\n1.661759 -2.878250 0.000000\n1.661759 2.878250 0.000000\n0.000000 0.000000 35.451423\nMo Se\n1 2\ndirect\n0.666667 0.333333 0.326886 Mo\n0.333333 0.666667 0.374080 Se\n0.333333 0.666667 0.279691 Se\n"


class ContactForm2(forms.Form):
    mat1 = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 14, "cols": 45})
    )
    mat2 = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 14, "cols": 45})
    )

    def __init__(self, *args, **kwargs):
        super(ContactForm2, self).__init__(*args, **kwargs)
        self.fields["mat1"].label = ""
        self.fields["mat2"].label = ""
        self.fields["mat1"].initial = tmp_pos
        self.fields["mat2"].initial = tmp_pos


class ContactForm(forms.Form):
    # def __init__(self,body='',results='',*args, **kwargs):
    #    self.body=body
    #    self.results=results
    # category =forms.ChoiceField(choices=[('question','Question'),('other','Other'),('ola','ola')])
    category1 = forms.ChoiceField(choices=sorted(choices))
    category2 = forms.ChoiceField(choices=sorted(choices))

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields["category1"].label = "Material 1"
        self.fields["category2"].label = "Material 2"

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
