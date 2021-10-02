from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import *
from .forms import *


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'category', 'content', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'created_on')
    prepopulated_fields = {'slug': ('title',)}


class MyUserAdmin(UserAdmin):
    add_form = MyUserCreationForm
    form = MyUserChangeForm
    fieldsets = (
        (None, {'fields': ('username', 'password', 'first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Other', {'fields': ('is_notified', )}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'first_name',
                       'last_name', 'is_staff', 'is_active', 'is_notified')}
         ),
    )
    list_display = ('id', 'username', 'first_name', 'last_name', 'is_staff', 'is_notified')
    list_filter = ('id', 'username')
    list_editable = ('is_notified',)
    list_display_links = ('id', 'username')
    ordering = ('id', )


admin.site.register(MyUser, MyUserAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
admin.site.register(Category)
