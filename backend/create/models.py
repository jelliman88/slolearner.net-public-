from django.db import models

LESSON_TYPE_CHOICES = (
    ('dialogue', 'dialogue'),
    ('news', 'news'),
    ('verb', 'verb'),
    ('keywords', 'keywords'),
)


ACTOR_CHOICES = (
    ('none', 'none'),
    ('rok&nina', 'rok & nina'),
    ('gašper&špela', 'gašper & špela'),
)

class Level(models.Model):
    level = models.IntegerField(default=0, blank=False)
    order = models.JSONField(default=list, blank=True, null=True)
    title = models.CharField(max_length=200, blank=True)
    slo_title = models.CharField(max_length=200, blank=True)
    is_live = models.CharField(max_length=25, default='false')

class Lesson(models.Model):
    type = models.CharField(default='news', choices=LESSON_TYPE_CHOICES, max_length=25)
    # add slo type
    actors = models.CharField(default='', choices=ACTOR_CHOICES, max_length=25)
    image = models.ImageField(upload_to='images/lesson', blank=True)
    title = models.CharField(max_length=200, blank=True)
    date = models.CharField(max_length=200, blank=True)
    description = models.CharField(max_length=1000, blank=True)
    slo_title = models.CharField(max_length=200, blank=True)
    slo_description = models.CharField(max_length=1000, blank=True)
    slo_date = models.CharField(max_length=200, blank=True)
    entries = models.JSONField(default=list, blank=True, null=True)
    missing_words = models.JSONField(default=dict, blank=True, null=True)
    level = models.IntegerField(default=0, blank=False)
    


    def get_entries_in_order(id):
        lesson = Lesson.objects.values().filter(id=id)
        lesson = lesson[0]
        entries_ids = lesson.get('entries')
        entries_arr = []
        if(entries_ids):
            queryset = Entry.objects.filter(id__in=entries_ids).values()
            for entry in queryset:
                try:
                    entry['actor'] = entry['actor'][str(id)]
                except:
                    pass
            # following loop is required beacuse django automatically sorts the query set in to id numerical order
            for entry_id in entries_ids:
                for query in queryset:
                    
                    if query['id'] == entry_id:
                        entries_arr.append(query)
        return lesson, entries_arr, entries_ids

    def get_percentages(lesson):
        entries = Entry.objects.filter(id__in=lesson.get('entries')).values()
        mw = lesson.get('missing_words')
        alt_counter = 0
        mw_counter = 0
        for entry in entries:
            try: 
                entry['alts'][str(lesson.get('id'))]
                alt_counter += 1
            except:
                pass
            try:
                options =  mw['eng_data'][str(entry['id'])]['options'] +  mw['slo_data'][str(entry['id'])]['options']
                counter = 0
                for option in options:
                    if option:
                        counter += 1
                if counter == 6:
                    mw_counter += 1
            except:
                pass

        obj = {
            'alts': [alt_counter, len(entries) ],
            'missing_words': [mw_counter, len(entries)]
        }
        return obj
        
class Entry(models.Model):
    actor = models.JSONField(default=dict, blank=True, null=True)
    eng = models.CharField(max_length=250)
    slo = models.CharField(max_length=250)
    alts = models.JSONField(default=dict, blank=True, null=True)
    info = models.JSONField(default=dict, blank=True, null=True)
    eng_audio = models.CharField(max_length=25, blank=True, null=True)
    slo_audio = models.CharField(max_length=25, blank=True, null=True)
    audio = models.CharField(max_length=25,default='false')
    
    def get_alts_data(entries, lesson_id):
        entries_arr = []
        for entry in entries:
            alts = entry.get('alts')
            if alts:
                if entry.get('id') == 0:
                    alts_ids = []
                    for k, v in alts.items():
                        for id in v:
                            alts_ids.append(v)
                else:
                    alt_ids = alts[str(lesson_id)]
                alt_entries = Entry.objects.values().filter(id__in=alt_ids)
                alts_arr = []
                for alt in alt_entries:
                    alts_arr.append(alt)
                new_entry = {}
                for k, v in entry.items():
                    if k == 'alts':
                        new_entry[k] = alts_arr
                    else:
                        new_entry[k] = v

                entries_arr.append(new_entry)
            else:
                entries_arr.append(entry)
        return entries_arr


def check_if_eng_or_slo_exists(obj):
    eng = obj.get('eng')
    slo = obj.get('slo')
    if Entry.objects.filter(eng=eng) or Entry.objects.filter(slo=slo):
        return obj
    else:
        return None
