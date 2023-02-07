from django.contrib import admin
from .models import  Entry, Lesson, Level


class LessonAdmin(admin.ModelAdmin):
    list_display = ('id',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Lesson, LessonAdmin)

class EntryAdmin(admin.ModelAdmin):
    list_display = ('eng',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Entry, EntryAdmin)

class LevelAdmin(admin.ModelAdmin):
    list_display = ('level',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Level, LevelAdmin)