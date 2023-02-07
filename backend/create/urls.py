from django.urls import path
from . import views


app_name = 'create'
urlpatterns = [
    path('dash', views.dash, name='dash'),
    path('lessons/<int:level>', views.lessons, name='lessons'),
    path('lesson/<int:id>/<int:level>', views.lesson, name='lesson'),
    path('alts/<int:id>/<int:level>', views.alts, name='alts'),
    path('alt/<int:id>/<int:lesson_id>/<int:level>', views.alt, name='alt'),
    path('create-edit-level/<int:id>', views.create_edit_level, name='create-edit-level'), 
    path('create-edit-lesson/<int:id>/<int:level>', views.create_edit_lesson, name='create-edit-lesson'), 
    path('missing-words/<int:id>/<int:level>', views.lesson, name='missing-words'), 
    path('add-info/<int:lesson_id>/<int:level>', views.add_info, name='add-info'),
    path('edit-entries/', views.edit_entries, name='edit-entries'),
    path('edit-entry/<int:id>', views.edit_entry, name='edit-entry'),
    path('ajax-search-entry/', views.ajax_search_entry, name="ajax_search_entry"),
    path('ajax-save-entries/', views.ajax_save_entries, name="ajax_save_entries"),
    path('ajax-add-lesson-id/<int:lesson>/<int:level>', views.ajax_add_lesson_id, name="ajax_add_lesson_id"),
    path('ajax-delete-lesson-id/<int:lesson>/<int:level>', views.ajax_delete_lesson_id, name="ajax_delete_lesson_id"),
    path('ajax-set-level-order/<int:level>/<str:order>', views.ajax_set_level_order, name="ajax_set_level_order"),
    path('ajax-autofill-missing-words/', views.ajax_autofill_missing_words, name="ajax_autofill_missing_words"),
    # ajax call probably needs reghex to get url and append ajax-search-entry, working in lesson, but not alt
]