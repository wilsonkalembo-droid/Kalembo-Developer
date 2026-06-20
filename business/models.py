from django.db import models
from django.contrib.auth.models import User

# Business Categories
CATEGORY_CHOICES = [
    ('retail', 'Retail'),
    ('food', 'Food & Beverage'),
    ('tech', 'Technology'),
    ('services', 'Services'),
    ('manufacturing', 'Manufacturing'),
    ('agriculture', 'Agriculture'),
    ('transport', 'Transport & Logistics'),
    ('fashion', 'Fashion & Textiles'),
    ('other', 'Other'),
]

# Business Status
STATUS_CHOICES = [
    ('draft', 'Draft'),
    ('pending_payment', 'Pending Payment'),
    ('payment_done', 'Payment Done - Pending Review'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
]


class BusinessListing(models.Model):
    """Model for storing business/shop information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='business')
    business_name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField(blank=True)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    location = models.CharField(max_length=300, blank=True)
    website = models.URLField(blank=True)
    logo = models.ImageField(upload_to='business_logos/', blank=True, null=True)
    
    # Pricing Information
    min_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Minimum price/cost in local currency")
    max_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Maximum price/cost in local currency")
    price_unit = models.CharField(max_length=100, blank=True, default="per item", help_text="Price unit (e.g., per item, per hour, per kg)")
    
    # Business Requirements
    requirements = models.TextField(blank=True, help_text="List business requirements, qualifications, or specifications")
    operating_hours = models.CharField(max_length=300, blank=True, help_text="Operating hours (e.g., Mon-Fri 9AM-5PM)")
    
    # Status & Timestamps
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Business Listings"
    
    def __str__(self):
        return self.business_name


class Payment(models.Model):
    """Model for payment tracking"""
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    business = models.ForeignKey(BusinessListing, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    payment_method = models.CharField(max_length=50, blank=True)
    transaction_id = models.CharField(max_length=100, blank=True, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Payments"
    
    def __str__(self):
        return f"{self.business.business_name} - {self.amount} ({self.status})"
