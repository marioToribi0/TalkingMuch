from email.policy import default
from .models import Reader
from django import forms


class ReaderForm(forms.ModelForm):
    class Meta:
        model = Reader
        fields = ['file']
        
class DataForm(forms.ModelForm):
    class Meta:
        model = Reader
        exclude = ['file', 'date_uploaded']
    CHOICES = (
        ('1', 'Generate document with word count'),
        ('2', 'Most used words'),
        ('3', 'Show message frequency by period'),
        ('4', 'Search for a phrase'),
        ('5', 'Messages per person'),
        ('6', 'Most common words per person'),
        ('7', 'Messages deleted by person')
    )
    SIZE = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7')
    )
    DATE = (
        ('1', 'Days'),
        ('2', 'Months'),
        ('3', 'Years'),
        ('4', 'Hours'),
    )
    size = forms.ChoiceField(label="How many options do yo want?", choices=SIZE)
    options_1 = forms.ChoiceField(label="Option 1", choices=CHOICES)
    options_2 = forms.ChoiceField(label="Option 2", choices=CHOICES)
    options_3 = forms.ChoiceField(label="Option 3", choices=CHOICES)
    options_4 = forms.ChoiceField(label="Option 4", choices=CHOICES)
    options_5 = forms.ChoiceField(label="Option 5", choices=CHOICES)
    options_6 = forms.ChoiceField(label="Option 6", choices=CHOICES)
    options_7 = forms.ChoiceField(label="Option 7", choices=CHOICES)
    
    # Option 2
    words = forms.IntegerField(label="Number of words", min_value=1)
    
    letters = forms.IntegerField(label="Number of letters", min_value=1) 
    
    # Option 3
    date = forms.ChoiceField(label='Show data per', choices=DATE)
    cant = forms.IntegerField(label='Data to show', min_value=1, max_value=100)

    # Option 4
    phrase = forms.CharField(label="Phrase to search", max_length=300)


    # Add initial values
    def __init__(self, *args, **kwargs):
        super(DataForm, self).__init__(*args, **kwargs)
        self.fields['words'].initial = 10
        self.fields['letters'].initial = 5
        self.fields['cant'].initial = 10
        self.fields['phrase'].initial = "Hello"
        
        for i in range(1,8):
            self.fields[f'options_{i}'].initial = f'{i}'
        
    