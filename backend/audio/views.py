from django.shortcuts import redirect, render
from create.models import Level, Lesson, Entry
from .models import AudioClip
from create.models import Entry
from pydub import AudioSegment, playback
from pydub.silence import split_on_silence
from itertools import chain

def dash(request):
    selected_level = request.POST.get('level')
    
    entries = Entry.objects.all()
    
    for entry in entries:
        if entry.info:
            print(entry.eng) 
    print('done') 
    if request.POST:
        gap = request.POST.get('gap')
        volume = request.POST.get('volume')
        selected_lesson = request.POST.get('lesson')
        mp3 = request.FILES.get('mp3')
        if mp3:
            sound = AudioSegment.from_mp3(mp3)
            audio_chunks = split_on_silence(sound, min_silence_len=int(gap), silence_thresh=-int(volume))
            counter = 1
            for i, chunk in enumerate(audio_chunks):
                output_file = f"static/temp/chunk{counter}.mp3"
                print("Exporting file", output_file)
                chunk.export(output_file, format="mp3")
                counter += 1
            return redirect('audio:match-audio', level=selected_level, lesson=selected_lesson,chunks=counter)
        lessons = Lesson.objects.filter(level=selected_level)
        selected_level = int(selected_level)
            
    else:
        lessons = []

    levels = Level.objects.all()
    context = {
        'levels': levels,
        'lessons': lessons,
        'selected_level': selected_level
    }
    return render(request, 'audio/dash.html', context)



def match_audio(request, level, lesson, chunks):
    lesson_obj = Lesson.objects.get(pk=lesson)
    if request.POST:
        names = request.POST.getlist('file-name')
        files = request.FILES.getlist('clip')
        ids = []
        i = 0
        for clip in files:
            clip.name = names[i]
            AudioClip.objects.create(file=clip)
            split_name = names[i].split('-')
            entry_id = split_name[0]
            ids.append(int(entry_id))
            i += 1

        entries_with_audio = []
        for id in ids:
            total = ids.count(id)
            if total == 2:
                if id not in entries_with_audio:
                    entries_with_audio.append(id)
        for id in entries_with_audio:
            Entry.objects.filter(pk=id).update(audio='true')
        return redirect('audio:dash')
         
    urls = []
    num_of_chunks = list(range(1, chunks))
    
    for i in num_of_chunks:
        url = f'/static/temp/chunk{i}.mp3'
        urls.append(url)
        i += 1
    if lesson_obj.type == 'dialogue':
        entries = Entry.objects.filter(id__in=lesson_obj.entries)
    else:
        entries = Entry.objects.filter(id__in=lesson_obj.entries).filter(audio='false')
        for entry in entries:
            try: alt_ids = entry.alts[str(lesson)]
            except: alt_ids = []
            if alt_ids:
                alts = Entry.objects.filter(id__in=alt_ids).filter(audio='false')
                entries = list(chain(entries, alts))
            

    context = {
        'level': Level.objects.get(level=level),
        'lesson': lesson_obj,
        'entries': entries,
        'urls': urls,
        
    }
    return render(request, 'audio/match-audio.html', context)


def get_alts(entries):
    for id in entries:
        entry = Entry.objects.get(pk=id)
        print(entry.alts)

        