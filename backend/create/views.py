from shutil import move 
from turtle import update
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from .models import Lesson, Entry, Level
from .forms import LessonForm, LevelForm, EntryForm
from audio.models import AudioClip
import ast
import os
from django.http import JsonResponse
from django.urls import resolve
from django.views.decorators.csrf import csrf_exempt
import random
#from .verbs_archive import verbs


@user_passes_test(lambda u: u.is_superuser)
def dash(request):
    if request.POST:
        new_lesson = Lesson.objects.create()
        return redirect('create:lesson', new_lesson.id)
    return render(request, 'create/dash.html')


def lessons(request, level):
    try:
        level_obj = Level.objects.get(level=level)
        level_order = level_obj.order
    except:
        level_obj = []
        level_order = []

    if request.POST:
        level_obj.is_live = 'true'
        level_obj.save()
       
    lessons = Lesson.objects.values().filter(level=level)
    all_lessons = {}

    for lesson in lessons:
        lesson_has_audio = check_audio(lesson)
        
        if lesson_has_audio:
            lesson['has_audio'] = 'true'
        obj = Lesson.get_percentages(lesson)
        lesson['create_progress'] = obj
        all_lessons[str(lesson['id'])] = lesson
    
    
    context = {
        'lessons': all_lessons,
        'levels':  Level.objects.all(),
        'selected_level': level_obj,
        'level_order': level_order
        }

    return render(request, 'create/lessons.html', context)

def check_audio(lesson):
    entries = Entry.objects.filter(id__in=lesson.get('entries'))
    if not entries:
        return False
    for entry in entries:
        if entry.audio != 'true':
            return False
    return True
            

            
def create_edit_level(request, id):
    if request.POST:
        edit = int(request.POST.get('pk'))
        if edit:
            instance = get_object_or_404(Level, level=edit)
            filled_form = LevelForm(
                request.POST, request.FILES, instance=instance)
        else:
            filled_form = LevelForm(request.POST, request.FILES,)
        if filled_form.is_valid():
            filled_form.save()
        return redirect('create:dash')
    if id != 0:
        level = get_object_or_404(Level, id=id)
        form = LevelForm(instance=level)
    else:
        level = ""
        form = LevelForm()

    context = {
        'level': level,
        'form': form,
        'id': id
    }
    return render(request, 'create/create-edit-level.html', context)

def create_edit_lesson(request, id, level):
    level_obj = Level.objects.get(level=level)
    if request.POST:
        edit = int(request.POST.get('pk'))
        if edit:
            instance = get_object_or_404(Lesson, id=edit)
            filled_form = LessonForm(
                request.POST, request.FILES, instance=instance)
        else:
            filled_form = LessonForm(request.POST, request.FILES,)
        if filled_form.is_valid():
            filled_form.save()
        return redirect('create:lessons', level) 
    if id != 0:
        lesson = get_object_or_404(Lesson, id=id)
        form = LessonForm(instance=lesson)
    else:
        lesson = ""
        form = LessonForm()
    context = {
        'lesson': lesson,
        'level': level_obj,
        'form': form,
        'id': id,
    }
    return render(request, 'create/create-edit-lesson.html', context)


def get_words_and_options(request, entries, lang):
    data = {}
    counter = 0
    for entry in entries:
        word = request.POST.get(f'{lang}_word_{counter}')
        options = request.POST.getlist(f'{lang}_option_{counter}')
        data[entry.get('id')] = {'word': word, 'options': options}
        counter += 1
    return data

# lesson handles both create content and missing words
def lesson(request, id, level):
    current_url = resolve(request.path_info).url_name
    base_url = str(os.getenv('BASE_URL'))
    lesson, entries, ids = Lesson.get_entries_in_order(id)
    if request.POST:
        eng_data = get_words_and_options(request, entries, 'eng')
        slo_data = get_words_and_options(request, entries, 'slo')
        lesson_obj = Lesson.objects.get(id=id)
        lesson_obj.missing_words = {
            "eng_data": eng_data,
            "slo_data": slo_data
        }
        lesson_obj.save()
        return redirect('create:lessons', level)
    if entries:
        context = {
            'lesson': lesson,
            'entries': entries,
            'lesson_id': id,
            'ids': ids,
            'level': level,
            'base_url': base_url
        }
    else:
        context = {
            'lesson': lesson,
            'lesson_id': id,
            'level': level,
            'base_url': base_url
        }
 
    if current_url == 'missing-words':
        page = 'create/missing-words.html'
        eng_words = []
        slo_words = []
        
        for entry in entries:
            split_engs = entry['eng'].split(' ')
            split_slos = entry['slo'].split(' ')
            # removes commas and others from dialoge texts
            for i in range(len(split_engs)):
                for char in split_engs[i]:
                    if char in '.,:;?!\'"()[]{}<>\/|`~@#$%^&*-_=+':
                        split_engs[i] = split_engs[i].replace(char, '')
                        split_slos[i] = split_slos[i].replace(char, '')
            
            eng_words.append(split_engs)
            slo_words.append(split_slos)
            
        counter = 0
        for entry in entries:
            entry['eng_words'] = eng_words[counter]
            entry['slo_words'] = slo_words[counter]
            counter += 1
        
    else:
        page = 'create/content.html'

    return render(request, page, context)


def alts(request, id, level):
    lesson, entries, ids = Lesson.get_entries_in_order(id)
    context = {
        'entries': entries,
        'lesson': lesson,
        'level': level,
        'lesson_id_as_string' : str(lesson.get('id'))   
    }
    return render(request, 'create/alts.html', context)


def alt(request, id, lesson_id, level):
    base_url = str(os.getenv('BASE_URL'))
    lesson = Lesson.objects.values().filter(pk=lesson_id)
    entry = Entry.objects.get(pk=id)
    
    try: alt_ids = entry.alts[str(lesson_id)]
    except: alt_ids = []
    alts = []
    for alt_id in alt_ids:
        altEntries = Entry.objects.values().filter(pk=alt_id)
        alts.append(altEntries[0])
    context = {
        # need be .values so that JSON can be read in react on the frontend
        'lesson': lesson[0],
        'entry': Entry.objects.filter(pk=id).values()[0],
        'alts': alts,
        'level': level,
        'base_url': base_url
    }

    return render(request, 'create/alt-content.html', context)


def add_info(request, lesson_id, level):
    lesson = Lesson.objects.get(id=lesson_id)
    entries = Entry.objects.filter(id__in=lesson.entries)
    if request.POST:
        in_slo = request.POST.getlist('text-in-slo')
        in_eng = request.POST.getlist('text-in-eng')
        
        #ids = request.POST.getlist('id')
        #infos = []
        counter = 0
        for entry in entries:
            obj = {'lesson': lesson_id, 'slo': in_eng[counter], 'eng': in_slo[counter]}
            entry.info[level] = obj
            entry.save()
            counter += 1
        return redirect('create:add-info', lesson_id, level)
    context = {
        'entries': entries,
        'lesson': lesson,
        'level': level,
    }
    return render(request, 'create/add-info.html', context)

def edit_entries(request):
    context = {
        'base_url': str(os.getenv('BASE_URL'))
    }
    return render(request, 'create/edit-entries.html', context)

def edit_entry(request, id):
    instance = get_object_or_404(Entry, pk=id)
    lessons = Lesson.objects.all()
    appears_in = []
    for lesson in lessons:
        if id in lesson.entries:
            obj = {'level': lesson.level, 'title': lesson.title}
            appears_in.append(obj)
            
    if request.POST:
        replacement = request.POST.get('replacement')
        if replacement:
            eng_rep = request.FILES.get('eng')
            slo_rep = request.FILES.get('slo')
            try:
                eng_rep.name = instance.eng_audio
            except:
                pass
            try:
                slo_rep.name = instance.slo_audio
            except:
                pass
            if eng_rep and slo_rep:
                eng_audio = AudioClip.objects.get(file=f'clips/{instance.eng_audio}')
                slo_audio = AudioClip.objects.get(file=f'clips/{instance.slo_audio}')
                eng_audio.file = eng_rep
                slo_audio.file = slo_rep
                eng_audio.save()
                slo_audio.save()
            elif eng_rep:
                eng_audio = AudioClip.objects.get(file=f'clips/{instance.eng_audio}')
                eng_audio.file = eng_rep
                eng_audio.save()
            else:
                slo_audio = AudioClip.objects.get(file=f'clips/{instance.slo_audio}')
                slo_audio.file = slo_rep
                slo_audio.save()
            return redirect('create:edit-entry', id)    
        else:
            form = EntryForm(request.POST, instance=instance)
            form.save()
            return redirect('create:edit-entry', id)
    context = {
        'form': EntryForm(instance=instance),
        'entry': instance,
        'appears_in': appears_in,
        'eng_url': str(os.getenv('AWS_CLIPS_BASE_URL')) + instance.eng_audio,
        'slo_url': str(os.getenv('AWS_CLIPS_BASE_URL')) + instance.slo_audio,
    }
    return render(request, 'create/edit-entry.html', context)

def ajax_search_entry(request):
    obj = decodeJavaScript(request)
    query = obj.get('query')
    single_word = obj.get('single')
    res = []
    if single_word:
        queryset = Entry.objects.values().filter(eng=query)
    else:
        queryset = Entry.objects.values().filter(eng__contains=query)
    
    for entry in queryset:
        if entry not in res:
            res.append(entry)
    return JsonResponse(res, safe=False)

@csrf_exempt
def ajax_save_entries(request):
    obj = decodeJavaScript(request)
    alts = obj.get('alts')
    entries = obj.get('entries')
    lesson = obj.get('lesson')
    lesson_id = lesson['id']
    updated_lesson_entries = []
   
    for entry in entries:
        if entry['id'] == 0:
            try:
                eng_exists = Entry.objects.get(eng=entry['eng'])
            except:
                eng_exists = False
            if eng_exists:
                # checks if id is 0 but entry is the same
                if entry['slo'] == eng_exists.slo or not entry['actor'][str[lesson_id]]:
                    # only exception to the rule of create new entry on any changes is when only the actor for specific lesson has changed, as this only effects this lesson
                    eng_exists.actor[lesson_id] = entry['actor']
                    eng_exists.save()
                    updated_lesson_entries.append(eng_exists.id)

                else:
                    new_entry = create_new_entry(entry, lesson_id)
                    updated_lesson_entries.append(new_entry)
                    

            else:
                new_entry = create_new_entry(entry, lesson_id)
                updated_lesson_entries.append(new_entry)

        else:
            updated_lesson_entries.append(entry['id'])
    
    if alts == 'True':
        alt_entry = obj.get('altEntry')
        entry = get_object_or_404(Entry, pk=int(alt_entry['id']))
        if entries:
            entry.alts[lesson_id] = updated_lesson_entries
            entry.save()
            res = 'alts saved'
    else:
        lesson = get_object_or_404(Lesson, pk=lesson_id)
        lesson.entries = updated_lesson_entries
        lesson.save()
        res = 'lesson saved'

    return JsonResponse(res, safe=False)

@csrf_exempt
def ajax_add_lesson_id(request, lesson, level):
    level_obj = Level.objects.get(level=level)
    level_order = level_obj.order
    level_order.append(lesson)
    level_obj.order = level_order
    level_obj.save()
    res = level_order
    return JsonResponse(res, safe=False)

@csrf_exempt
def ajax_delete_lesson_id(request, lesson, level):
    level_obj = Level.objects.get(level=level)
    level_order = level_obj.order
    updated_order = []
    for id in level_order:
        if id == lesson:
            pass
        else:
            updated_order.append(id)
    level_obj.order = updated_order
    level_obj.save()
    res = updated_order
    return JsonResponse(res, safe=False)

@csrf_exempt
def ajax_set_level_order(request, level, order):
    level_obj = Level.objects.get(level=level)
    level_obj.order = ast.literal_eval(order)
    level_obj.save()
    res = 'saved order'
    return JsonResponse(res, safe=False)

def ajax_autofill_missing_words(request):
    obj = decodeJavaScript(request)
    eng = obj.get('eng')
    slo = obj.get('slo')
    lessons = Lesson.objects.all()
    eng_options = []
    slo_options = []
    
    for lesson in lessons:
        for lang, obj in lesson.missing_words.items():
            if lang == 'eng_data':
                for d in obj.values():
                    if d.get('word') == eng:
                        for option in d.get('options'):
                            if option:
                                if len(eng_options) == 3:
                                    heads = bool(random.getrandbits(1))
                                    i = random.randint(0, 2)
                                    if heads:
                                        eng_options.pop(i)
                                        eng_options.append(option)
                                else:
                                    eng_options.append(option)
                                

            else:
                for d in obj.values():
                    if d.get('word') == slo:
                        for option in d.get('options'):
                            if option: 
                                if len(slo_options) == 3:
                                    heads = bool(random.getrandbits(1))
                                    i = random.randint(0, 2)
                                    if heads:
                                        slo_options.pop(i)
                                        slo_options.append(option)
                                else:
                                    slo_options.append(option)

    
    options = {'eng': eng_options,
    'slo': slo_options}
            
    
    return JsonResponse(options, safe=False)




def decodeJavaScript(request):
    obj_as_string = request.body.decode("utf-8")
    return ast.literal_eval(obj_as_string)


def create_new_entry(entry, lesson_id):
    actor = {int(lesson_id): entry['actor']}
    new_entry = Entry.objects.create(
        eng=entry['eng'], slo=entry['slo'], actor=actor)
    Entry.objects.filter(pk=new_entry.id).update(eng_audio=f'{new_entry.id}-en.mp3', slo_audio=f'{new_entry.id}-sl.mp3')
    return new_entry.id
