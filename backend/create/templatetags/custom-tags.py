from django import template
from django.template.defaultfilters import stringfilter
import random
register = template.Library()

@register.filter(name='get_selected_eng_word')
def get_selected_eng_word(lesson, id):
    selected_word = lesson['missing_words']['eng_data'][str(id)]['word']
    return selected_word

@register.filter(name='get_selected_slo_word')
def get_selected_slo_word(lesson, id):
    selected_word = lesson['missing_words']['slo_data'][str(id)]['word']
    return selected_word

# eng and slo are reversed below so that each gets the info in their mother tounge
@register.filter(name='get_slo_info')
def get_slo_info(obj, level):
    if obj:
        return obj[str(level)]['eng']
    else:
        return ''
    

@register.filter(name='get_eng_info')
def get_eng_info(obj, level):
    if obj:
        return obj[str(level)]['slo']
    else:
        return ''


@register.filter(name='get_eng_options')
def get_eng_options(lesson, id):
    try:
        options = lesson['missing_words']['eng_data'][str(id)]['options']
    except:
        options = ['']
    if options[0] == '':
        data = None
    else:
        data = [options]
    return data

@register.filter(name='get_slo_options')
def get_slo_options(lesson, id):
    try:
        options = lesson['missing_words']['slo_data'][str(id)]['options']
    except:
        options = ['']
    if options[0] == '':
     data = None
    else:
        data = [options]
    return data

@register.filter
def attempted(results, id):
    if str(id) not in results:
        return False
    return f"{results[str(id)][0]}/{results[str(id)][1]}"

@register.filter
def get_grade_color(results, id):
    if str(id) not in results:
        return False
    score = results[str(id)][0]
    length = results[str(id)][1]
    if score == length:
        result = 'success'
    else:
        result = 'white'
    return result

@register.filter
def random_lang():
    return random.choice(['eng','slo'])



