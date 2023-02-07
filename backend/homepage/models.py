from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from create.models import Level

class UserProfileManager(BaseUserManager):
    """ Manager for user profiles """
    def create_user(self, email, username, password=None,):
        """ Create a new user profile """
        if not email:
            raise ValueError('User must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username)
        

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, password):
        """ Create a new superuser profile """
        user = self.create_user(email,username, password)
        user.is_superuser = True
        user.is_staff = True

        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    homework_list = models.JSONField(default=list, blank=True, null=True)
    website_lang = models.CharField(max_length=255, default='')
    results = models.JSONField(default=dict, blank=True, null=True)
    progress = models.IntegerField(default=1)
    first_lang = models.CharField(max_length=10, default='')
    hw_first_lang = models.CharField(max_length=10, default='eng')
    verification_code = models.IntegerField(default=0)
 

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        # return string representation of user
        return self.email

    def adjust_user_results(request,level, lesson_id, score, lesson_len):
        user = UserProfile.objects.get(email=request.user)
        results_obj = user.results
        lesson_id = str(lesson_id)
        try:
            level_res = results_obj[level]
        except:
            level_res = None
        if level_res:
            level_obj = results_obj[level]
            try:
                lesson_res = level_obj[lesson_id]
            except:
                lesson_res = None
            if lesson_res:
                prev_top_score = level_obj[lesson_id]
                if score > prev_top_score[0]:
                    level_obj[lesson_id][0] = score
            else:
                level_obj[lesson_id] = [score, lesson_len]
        else:
            level_obj = { lesson_id: [score, lesson_len] }
            results_obj[level] = level_obj
        user.results = results_obj
        user.save()
        queryset = Level.objects.get(level=level)
        level_length = len(queryset.order)
        max_level = set_level_progress(level_obj, level, level_length)
        level_up = False
        if int(max_level) > user.progress:
            user.progress = max_level
            user.save()
            level_up = True
        return level_up, max_level
    
def set_level_progress(results, current_level, level_length):
    if len(results.keys()) == level_length:
        for i in results.values():
            if i[0] != i[1]:
                return current_level
        return int(current_level) + 1
    else:
        return current_level
            
        

    

        