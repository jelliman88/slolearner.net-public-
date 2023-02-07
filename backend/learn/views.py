from re import M
from django.shortcuts import redirect, render, get_object_or_404
from create.models import Lesson, Entry, Level
from homepage.models import UserProfile
from audio.models import AudioClip
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import ast
import logging
import boto3
from botocore.exceptions import ClientError
import os
from django.core.paginator import Paginator
from dotenv import load_dotenv
load_dotenv()

def dash(request):
    if request.POST:
        language = request.POST.get('learning')
        current_user_obj = UserProfile.objects.get(id=request.user.id)
        current_user_obj.first_lang = language
        current_user_obj.save()
        return redirect('learn:dash')
    user = UserProfile.objects.get(email=request.user)
    if user.verification_code != 0:
        return redirect('homepage:verify-email')
    #last 5 entries, if needed. 
    #entries = get_most_recent_homework_entries(user)
    entries = Entry.objects.filter(id__in=user.homework_list)
    if user.is_staff:
        levels = Level.objects.all()
    else:
        levels = Level.objects.filter(is_live='true')
    max_level = user.progress - 1
    try:
        percent_completed = max_level  / len(levels) * 100
    except:
        percent_completed = 0
    context = {
        'entries': len(entries),
        'total_levels': len(levels) + 1,
        'last_avail_level': len(levels),
        'percent_complete': int(percent_completed)
    }
    return render(request, 'learn/dash.html', context)

def my_account(request):
    user = UserProfile.objects.get(email=request.user)
    if request.POST:
        new_username = request.POST.get('username')
        website_lang = request.POST.get('website_lang')
        first_lang = request.POST.get('first_lang')
        if new_username:
            user.username = new_username
        user.website_lang = website_lang
        user.first_lang = first_lang
        user.save()
        #request.path_info = 'sl/'
    context = {
        'user': user,
        'base_url': str(os.getenv('BASE_URL')),
        'required_url': '/' + user.website_lang + '/learn/my-account/'
    }
    return render(request, 'learn/my-account.html', context)

def no_cheating(request):
    return render(request, 'no-cheating.html')

def select_lesson(request, level):
    user = UserProfile.objects.get(email=request.user)
    types_translations = {'dialogue': 'dialog','news':'novice','verb':'glagolnik','keywords':'ključne besede'}
    if level > user.progress:
        return render(request, 'learn/no-cheating.html')
    try:
        results = user.results[str(level)]
    except:
        results = {}
    level_obj = Level.objects.get(level=level)
    lessons = Lesson.objects.filter(id__in=level_obj.order)
    lessons_in_order = []
    for id in level_obj.order:
        for lesson in lessons:
            if lesson.id == id:
                lessons_in_order.append(lesson)
    
    available = []
    
    if not results:
        available.append(lessons_in_order[0].id)
    else:
        for k, v in results.items():
            if v[0] == v[1]:
                available.append(int(k))
        if len(available) < len(lessons_in_order):
            available.append(lessons_in_order[len(available)].id)
    if user.website_lang == 'sl':
        for lesson in lessons:
            lesson.type = types_translations[lesson.type]
    if user.is_staff:
        levels = Level.objects.all()
    else:
        levels = Level.objects.filter(is_live='true')
    context = {
        'lessons': lessons_in_order,
        'levels':  levels,
        'level': level_obj,
        'results': results,
        'user': user,
        'available': available
    }
    return render(request, "learn/select-lesson.html", context)



def create_presigned_url(bucket_name, object_name, expiration=3600):
    # Generate a presigned URL for the S3 object
    s3_client = boto3.client('s3')
    try:
        response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': bucket_name,
                                                            'Key': object_name},
                                                    ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return None

    # The response contains the presigned URL
    return response

def lesson(request, level, id):
    level_obj = Level.objects.get(level=level)
    user = UserProfile.objects.get(email=request.user)
    
    homework_list = user.homework_list
    if id == 0: # 0 means homework
        lesson = 'homework'
        entries = Entry.objects.filter(id__in=homework_list).values()
    else:
        lesson = Lesson.objects.filter(id=id).values()
        entries = Entry.objects.filter(id__in=lesson[0].get('entries')).values()
    entries_arr = Entry.get_alts_data(entries, id)
    #audio = create_presigned_url('slolearner-audio-files', '1-eng.mp3', expiration=3600)
    #print(audio)
    
    # needed as django loves to place the entries in numerical order of their ID's, this also appears in Create.models called "get_entries_in_order"
    ordered_entries = []
    for id in lesson[0]['entries']:
        for entry in entries_arr:
            if id == entry['id']:
                ordered_entries.append(entry)


    context = {
        'format': lesson[0].get('type'),
        # lesson needs to be as a string (for JS) and object (for img)
        #'lesson_obj':Lesson.objects.get(id=id),
        'lesson': lesson[0],
        'entries': ordered_entries,
        'homework': homework_list,
        'level': level,
        'lessons_in_order': level_obj.order,
        'base_url': str(os.getenv('BASE_URL')),
        'aws_clips_base_url': str(os.getenv('AWS_CLIPS_BASE_URL'))
    }
    
    return render(request, "learn/lesson.html", context)

def homework(request):
    user = UserProfile.objects.get(email=request.user)
    if request.POST:
        items_per_page = request.POST.get('items-per-page')
        items_per_page = int(items_per_page)
        side = request.POST.get('side')
        if side:
            hw_first_lang = request.POST.get('first-lang')
            if side == 'shuffle':
                hw_first_lang = 'shuffle'
            else:
                if hw_first_lang == 'eng':
                    hw_first_lang = 'slo'
                else:
                    hw_first_lang = 'eng'
            user.hw_first_lang = hw_first_lang
            user.save()
        else:
            hw_first_lang = user.hw_first_lang
    else: 
        hw_first_lang = user.hw_first_lang
        items_per_page = 4
    if hw_first_lang == 'shuffle':
        shuffle = True
    else: shuffle = False
    homework_list = user.homework_list
    queryset = Entry.objects.values().filter(id__in=homework_list)
    paginator = Paginator(queryset, items_per_page)
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    base_s3_url = 'https://slolearner-audio-files.s3.eu-central-1.amazonaws.com/clips/'
    audio = AudioClip.objects.all()
    # add full url to entry obj
    for entry in page_obj:
        if type(entry) == dict:
            eng_url = base_s3_url + entry.get('eng_audio')
            slo_url = base_s3_url + entry.get('slo_audio')
            entry['eng_audio'] = eng_url
            entry['slo_audio'] = slo_url
    context = {
        'user': user,
        'page_obj': page_obj,
        'first_lang': hw_first_lang,
        'page_options': [4, 8, 16, 24, len(queryset)],
        'items_per_page': items_per_page,
        'value': [0,1],
        'shuffle': shuffle,
        'base_url': str(os.getenv('BASE_URL')),
        'base_s3_url': base_s3_url,
        'audio': audio
    }
    return render(request, 'learn/homework.html', context)

@csrf_exempt
def add_remove_homework(request):
    user = UserProfile.objects.get(email=request.user)
    homework_list = user.homework_list
    obj = decodeJavaScript(request)
    id = int(obj.get('id'))
    
    if id in homework_list:
        homework_list.remove(id)
        user.homework_list = homework_list
        user.save()
    else:
        homework_list.append(id)
        user.homework_list = homework_list
        user.save()
    updated_user = UserProfile.objects.get(email=request.user)
    homework = updated_user.homework_list
    return JsonResponse(homework,safe=False)

@csrf_exempt
def adjust_progress(request):
    obj = decodeJavaScript(request)
    level = obj.get('level')
    lesson_id = obj.get('lesson_id')
    score = obj.get('score')
    lesson_len = obj.get('lesson_len')
    level_up, max_level = UserProfile.adjust_user_results(request,level, lesson_id, score, lesson_len)
    if level_up:
        next_level = Level.objects.filter(level=max_level).values()
        res = { 'level_up': 'true', 'next_level': next_level[0]}
    else:
        res = { 'level_up': 'false'}
    return JsonResponse(res,safe=False)

def ajax_check_username_exists(request):
    obj = decodeJavaScript(request)
    username_is_taken = UserProfile.objects.filter(username=obj.get('username')).exists()
    if username_is_taken:
        res = 'taken'
    else:
        res = 'available'
    return JsonResponse(res,safe=False)

def decodeJavaScript(request):
    obj_as_string = request.body.decode("utf-8")
    return ast.literal_eval(obj_as_string)

def get_most_recent_homework_entries(user):
    homework_list = user.homework_list
    if homework_list:
        if len(homework_list) < 4 :
            most_recent = homework_list[-5:]
        else:
            most_recent = homework_list[-5:]
    else:
        most_recent = []
    if most_recent:
        return Entry.objects.filter(id__in=most_recent)
    else:
        return []

