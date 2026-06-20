from django.contrib import admin
from django.utils.html import format_html
from .models import BusinessListing, Payment


def approve_business(modeladmin, request, queryset):
    """Admin action to approve businesses"""
    updated = queryset.update(status='approved')
    modeladmin.message_user(request, f'{updated} business(es) approved successfully!')

approve_business.short_description = "Approve selected businesses"


def reject_business(modeladmin, request, queryset):
    """Admin action to reject businesses"""
    updated = queryset.update(status='rejected')
    modeladmin.message_user(request, f'{updated} business(es) rejected!')

reject_business.short_description = "Reject selected businesses"


@admin.register(BusinessListing)
class BusinessListingAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'user', 'category', 'status', 'created_at', 'logo_preview')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('business_name', 'user__email', 'phone')
    readonly_fields = ('created_at', 'updated_at', 'logo_display')
    actions = [approve_business, reject_business]
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Business Information', {
            'fields': ('business_name', 'category', 'description', 'logo', 'logo_display')
        }),
        ('Contact Information', {
            'fields': ('phone', 'email', 'location', 'website')
        }),
        ('Pricing & Operations', {
            'fields': ('min_price', 'max_price', 'price_unit', 'operating_hours')
        }),
        ('Requirements & Qualifications', {
            'fields': ('requirements',)
        }),
        ('Status & Timestamps', {
            'fields': ('status', 'created_at', 'updated_at')
        }),
    )
    
    def logo_preview(self, obj):
        """Show whether business has a logo"""
        if obj.logo:
            return '✅ Has Logo'
        return '❌ No Logo'
    logo_preview.short_description = 'Logo'
    
    def logo_display(self, obj):
        """Display logo image in admin"""
        if obj.logo:
            return format_html('<img src="{}" width="200" height="auto" />', obj.logo.url)
        return '(No logo uploaded)'
    logo_display.short_description = 'Logo Preview'
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return self.readonly_fields + ('user', 'business_name', 'category')
        return self.readonly_fields


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('business', 'amount', 'status', 'transaction_id', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('business__business_name', 'transaction_id')
    readonly_fields = ('created_at', 'updated_at', 'transaction_id')
    
    fieldsets = (
        ('Payment Information', {
            'fields': ('business', 'amount', 'transaction_id')
        }),
        ('Status & Method', {
            'fields': ('status', 'payment_method')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )
