from django.contrib import admin
from .models import UserProfile, Tasks,UserScore
from django.db import models

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Tasks)
#admin.site.register(UserScore);
#admin.site.register(UserScore, UserScoreAdmin)
# class UserScoreForm(forms.ModelForm):
#     class Meta:
#         model = UserScore
#         fields = '__all__'

#     def __init__(self, *args, **kwargs):
#         super(UserScoreForm, self).__init__(*args, **kwargs)
#         # Only show users without a score already
#         scored_users = UserScore.objects.values_list('user', flat=True)
#         self.fields['user'].queryset = User.objects.exclude(id__in=scored_users)

@admin.register(UserScore)
class UserScoreAdmin(admin.ModelAdmin):
    ##form = UserScoreForm
    list_display = ('user', 'daily_score', 'weekly_score', 'overall_score', 'last_updated_date')
    readonly_fields = ('last_updated_date',)
    

