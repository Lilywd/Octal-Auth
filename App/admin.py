from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
# Register your models here.

class CustomUserAdmin(UserAdmin):
   list_display = ('email', 'username', 'phone_number','is_staff','is_admin')
   search_fields = ('email', 'username','phone_number')

   
   fieldsets = ()
   filter_horizontal = ()
   list_filter = ()

# Now register the new UserAdmin...
admin.site.register(User, CustomUserAdmin)
