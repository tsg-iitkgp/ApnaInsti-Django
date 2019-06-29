from django.contrib import admin

from users.models import (UserFormerRole, UserProfile, UserTag,
                          UserTagCategory, WebPushSubscription)


class ProfileAdmin(admin.ModelAdmin):
    search_fields = ['name', 'roll_no']
    list_display = ('name', 'roll_no', 'department', 'degree')
    list_filter = ('join_year', 'department', 'degree')
    raw_id_fields = ('user',)

class UserFormerRoleAdmin(admin.ModelAdmin):
    list_display = ('user', 'role', 'year')
    raw_id_fields = ('user',)
    ordering = ('-year', 'role')

class WebPushSubscriptionAdmin(admin.ModelAdmin):
    raw_id_fields = ('user',)

class UserTagAdmin(admin.ModelAdmin):
    list_display = ('category', 'name', 'target', 'secondary_target')
    ordering = ('category', 'name')


admin.site.register(UserProfile, ProfileAdmin)
admin.site.register(UserFormerRole, UserFormerRoleAdmin)
admin.site.register(WebPushSubscription, WebPushSubscriptionAdmin)
admin.site.register(UserTagCategory)
admin.site.register(UserTag, UserTagAdmin)
