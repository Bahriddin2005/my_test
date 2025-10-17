from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils import timezone
from django import forms
from django.contrib.auth.forms import UserChangeForm

# Faqat mavjud modellarni import qilamiz
try:
    from .models import User, VerificationRequest
except ImportError:
    User = None
    VerificationRequest = None

# Agar User modeli mavjud bo'lsa va custom fieldlarga ega bo'lsa
if User and hasattr(User, 'role'):
    
    class CustomUserChangeForm(UserChangeForm):
        class Meta(UserChangeForm.Meta):
            model = User
            fields = '__all__'
    
    class CustomUserAdmin(UserAdmin):
        model = User
        form = CustomUserChangeForm
        
        list_display = ['username', 'email', 'role', 'is_verified', 'school_email_verified', 'student_id', 'is_active']
        list_filter = ['role', 'is_verified', 'school_email_verified', 'is_active', 'grade']
        search_fields = ['username', 'email', 'student_id', 'first_name', 'last_name']
        
        # To'liq qayta aniqlangan fieldsets
        fieldsets = (
            (None, {'fields': ('username', 'password')}),
            ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
            ('Permissions', {
                'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            }),
            ('Important dates', {'fields': ('last_login',)}),  # Faqat last_login
            ('School Info', {
                'fields': ('role', 'student_id', 'is_verified', 'school_email_verified', 
                          'phone_number', 'class_name', 'grade', 'subject')
            }),
        )
        
        add_fieldsets = (
            (None, {
                'classes': ('wide',),
                'fields': ('username', 'password1', 'password2'),
            }),
            ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
            ('School Info', {
                'fields': ('role', 'student_id', 'phone_number', 'class_name', 'grade', 'subject')
            }),
        )
        
        filter_horizontal = ('groups', 'user_permissions',)
    
    admin.site.register(User, CustomUserAdmin)

# VerificationRequest admin
if VerificationRequest:
    @admin.register(VerificationRequest)
    class VerificationRequestAdmin(admin.ModelAdmin):
        list_display = ['user', 'requested_at', 'is_approved', 'processed_by', 'processed_at']
        list_filter = ['is_approved', 'requested_at']
        search_fields = ['user__username', 'user__email']
        readonly_fields = ['requested_at']
        
        def approve_request(self, request, queryset):
            for verification_request in queryset:
                verification_request.user.is_verified = True
                verification_request.user.save()
                verification_request.is_approved = True
                verification_request.processed_by = request.user
                verification_request.processed_at = timezone.now()
                verification_request.save()
            self.message_user(request, f'{queryset.count()} requests approved.')
        
        def reject_request(self, request, queryset):
            for verification_request in queryset:
                verification_request.is_approved = False
                verification_request.processed_by = request.user
                verification_request.processed_at = timezone.now()
                verification_request.save()
            self.message_user(request, f'{queryset.count()} requests rejected.')
        
        approve_request.short_description = "Approve selected requests"
        reject_request.short_description = "Reject selected requests"
        actions = [approve_request, reject_request]