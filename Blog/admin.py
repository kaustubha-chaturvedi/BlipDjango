from django.contrib import admin
from .models import *
from django import forms
from django.contrib.auth.admin import UserAdmin
from django.contrib.admin.widgets import FilteredSelectMultiple    
from django.contrib.auth.models import Group


admin.site.site_header = "Blip"
class GroupAdminForm(forms.ModelForm):
    class Meta:
        model = Group
        exclude = []
    users = forms.ModelMultipleChoiceField(
         queryset=User.objects.all(), 
         required=False,
         widget=FilteredSelectMultiple('users', False)
    )

    def __init__(self, *args, **kwargs):
        super(GroupAdminForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['users'].initial = self.instance.user_set.all()

    def save_m2m(self):
        self.instance.user_set.set(self.cleaned_data['users'])

    def save(self, *args, **kwargs):
        instance = super(GroupAdminForm, self).save()
        self.save_m2m()
        return instance

admin.site.unregister(Group)
class GroupAdmin(admin.ModelAdmin):
    form = GroupAdminForm
    filter_horizontal = ['permissions']
admin.site.register(Group, GroupAdmin)

class CustomUserAdmin(UserAdmin):
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email','first_name','last_name','date_joined','password','usergroup')}),
        ('Permissions', {'fields': ('is_staff', 'is_active','is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active','is_superuser')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
admin.site.register(User, CustomUserAdmin)

@admin.register(SiteDescription)
class SiteModelAdmin(admin.ModelAdmin):
    list_display=['title','description']

@admin.register(Post)
class PostModelAdmin(admin.ModelAdmin):
    list_filter=['tags']
    list_display=['title','description','content']

@admin.register(Author)
class AuthorModelAdmin(admin.ModelAdmin):
    list_display=['name']

@admin.register(Tag)
class TagModelAdmin(admin.ModelAdmin):
    list_display=['title','description']
