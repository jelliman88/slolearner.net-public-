from django.forms import ModelForm, Textarea, TextInput
from .models import Lesson, Level, Entry


class LessonForm(ModelForm):
   
   class Meta:
      model = Lesson
      widgets = {
               'description': Textarea(attrs={'cols': 30, 'rows': 10}),
               'slo_description': Textarea(attrs={'cols': 30, 'rows': 10}),

         }
      exclude = ('entries', 'missing_words', 'date','slo_date', 'image')
   def __init__(self, *args, **kwargs):
            super(LessonForm, self).__init__(*args, **kwargs)
            self.fields['title'].widget = TextInput(attrs={'class': 'form-control', 'placeholder': 'title'})
            self.fields['slo_title'].widget = TextInput(attrs={'class': 'form-control', 'placeholder': 'slo title'})
            self.fields['description'].widget = TextInput(attrs={'class': 'form-control', 'placeholder': 'description'})
            self.fields['slo_description'].widget = TextInput(attrs={'class': 'form-control', 'placeholder': 'slo description'})
            self.fields['level'].widget = TextInput(attrs={'id': 'level-field'})
            for fieldname in ['title','slo_title', 'description', 'slo_description']:
               self.fields[fieldname].label = ''


class LevelForm(ModelForm):
   
   class Meta:
      model = Level
      exclude = ('order',)

class EntryForm(ModelForm):
   
   class Meta:
      model = Entry
      fields = ('eng', 'slo')
   def __init__(self, *args, **kwargs):
      super(EntryForm, self).__init__(*args, **kwargs)
      self.fields['eng'].widget = TextInput(attrs={'class': 'form-control m-4', 'placeholder': 'eng'})
      self.fields['slo'].widget = TextInput(attrs={'class': 'form-control m-4', 'placeholder': 'slo'})
      for fieldname in ['eng', 'slo']:
         self.fields[fieldname].label = ''