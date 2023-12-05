# -*- coding: utf-8 -*-
from django import forms
#from .models import Snippet
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit


class ContactForm1(forms.Form):
    # def __init__(self,body='',results='',*args, **kwargs):
    #    self.body=body
    #    self.results=results
    body = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 15, "cols": 50, "class": "box1"})
    )
    def __init__(self, *args, **kwargs):
                    super(ContactForm1, self).__init__(*args, **kwargs)
                    self.fields['body'].label = "" 

class ContactForm2(forms.Form):
    # def __init__(self,body='',results='',*args, **kwargs):
    #    self.body=body
    #    self.results=results
    body = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 15, "cols": 50, "class": "box1"})
    )
    def __init__(self, *args, **kwargs):
                    super(ContactForm2, self).__init__(*args, **kwargs)
                    self.fields['body'].label = "" 

class ContactForm3(forms.Form):
    # def __init__(self,body='',results='',*args, **kwargs):
    #    self.body=body
    #    self.results=results
    body = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 15, "cols": 50, "class": "box1"})
    )
    def __init__(self, *args, **kwargs):
                    super(ContactForm3, self).__init__(*args, **kwargs)
                    self.fields['body'].label = "" 

class ContactForm4(forms.Form):
    # def __init__(self,body='',results='',*args, **kwargs):
    #    self.body=body
    #    self.results=results
    body = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 15, "cols": 50, "class": "box1"})
    )
    def __init__(self, *args, **kwargs):
                    super(ContactForm4, self).__init__(*args, **kwargs)
                    self.fields['body'].label = "" 

