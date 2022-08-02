from django.contrib import admin
from django.utils.text import Truncator
from schedule.models import Calendar , Event


class CalendarAdmin(admin.ModelAdmin): 
   list_display   = ('name', )
   list_filter    = ('name',)
   ordering       = ('name',)
   search_fields  = ('name',)


class EventAdmin(admin.ModelAdmin):
   list_display   = ('title', )
   list_filter    = ('title',)
   ordering       = ('title',)
   search_fields  = ('title',)


admin.site.register(Calendar, CalendarAdmin)
admin.site.register(Event, EventAdmin)