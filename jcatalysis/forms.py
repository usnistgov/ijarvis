# -*- coding: utf-8 -*-
from django import forms
#from .models import Snippet
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit

tmp_pos2 = "Catalyst,adsorbate_indices:[17,]\n1.0\n5.8815161295883795 0.0 0.0\n2.9407580647941898 5.093542380991464 0.0\n0.0 0.0 22.203356715720272\nAg Au O\n12 4 1\ndirect\n0.0 0.0 0.3377867133623019 \n0.4999996709684214 0.0 0.3377867133623019 \n-2.8137908399499664e-07 0.5000002337265894 0.3377867133623019 \n0.49999938958933743 0.5000002337265894 0.3377867133623019 \n0.16666646319644582 0.1666667445755298 0.4459288551480538 \n0.6666661341648672 0.1666667445755298 0.4459288551480538 \n0.1666661818173618 0.6666669783021192 0.4459288551480538 \n0.6666658527857833 0.6666669783021192 0.4459288551480538 \n-0.1666667445755298 0.3333334891510596 0.5540709969338058 \n0.33333292639289164 0.3333334891510596 0.5540709969338058 \n-0.16666702595461375 0.8333337228776488 0.5540709969338058 \n0.3333326450138077 0.8333337228776488 0.5540709969338058 \n0.0 0.0 0.6622131387195576 \n0.4999996709684214 0.0 0.6622131387195576 \n-2.8137908399499664e-07 0.5000002337265894 0.6622131387195576 \n0.49999938958933743 0.5000002337265894 0.6622131387195576 \n0.0 0.0 0.7432819499265101 \n"


tmp_pos1 = "Substrate\n1.0\n5.8815161295883795 0.0 0.0\n2.9407580647941898 5.093542380991464 0.0\n0.0 0.0 22.203356715720272\nAg Au\n12 4\ndirect\n0.0 0.0 0.3377867133623019 \n0.4999996709684214 0.0 0.3377867133623019 \n-2.8137908399499664e-07 0.5000002337265894 0.3377867133623019 \n0.49999938958933743 0.5000002337265894 0.3377867133623019 \n0.16666646319644582 0.1666667445755298 0.4459288551480538 \n0.6666661341648672 0.1666667445755298 0.4459288551480538 \n0.1666661818173618 0.6666669783021192 0.4459288551480538 \n0.6666658527857833 0.6666669783021192 0.4459288551480538 \n-0.1666667445755298 0.3333334891510596 0.5540709969338058 \n0.33333292639289164 0.3333334891510596 0.5540709969338058 \n-0.16666702595461375 0.8333337228776488 0.5540709969338058 \n0.3333326450138077 0.8333337228776488 0.5540709969338058 \n0.0 0.0 0.6622131387195576 \n0.4999996709684214 0.0 0.6622131387195576 \n-2.8137908399499664e-07 0.5000002337265894 0.6622131387195576 \n0.49999938958933743 0.5000002337265894 0.6622131387195576 \n"


class ContactForm(forms.Form):
    # def __init__(self,body='',results='',*args, **kwargs):
    #    self.body=body
    #    self.results=results
    substrate = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 15, "cols": 50, "class": "box1"})
    )
    catalyst = forms.CharField(
        widget=forms.Textarea(attrs={"rows": 15, "cols": 50, "class": "box1"})
    )
    def __init__(self, *args, **kwargs):
                    super(ContactForm, self).__init__(*args, **kwargs)
                    self.fields['substrate'].label = "" #"Substrate" 
                    self.fields['catalyst'].label = "" #"Catalyst" 
                    self.fields['substrate'].initial = tmp_pos1  
                    self.fields['catalyst'].initial = tmp_pos2

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
