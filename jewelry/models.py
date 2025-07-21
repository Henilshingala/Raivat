from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from decimal import Decimal
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
import uuid


class UserProfile(models.Model):

    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True, verbose_name="Phone Number")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Birth Date")
    
    street_number = models.CharField(max_length=10, blank=True, verbose_name="Street Number")
    street_name = models.CharField(max_length=255, blank=True, verbose_name="Street Name")
    city = models.CharField(max_length=100, blank=True, verbose_name="City")
    state = models.CharField(max_length=100, blank=True, verbose_name="State/Province")
    zip_code = models.CharField(max_length=20, blank=True, verbose_name="Zip/Postal Code")
    country = models.CharField(max_length=100, blank=True, verbose_name="Country")
    

    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")
    
    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
    
    def __str__(self):
        return f"{self.user.email} - Profile"
    
    def get_full_address(self):

        address_parts = []
        if self.street_number and self.street_name:
            address_parts.append(f"{self.street_number} {self.street_name}")
        if self.city:
            address_parts.append(self.city)
        if self.state:
            address_parts.append(self.state)
        if self.zip_code:
            address_parts.append(self.zip_code)
        if self.country:
            address_parts.append(self.country)
        return ", ".join(address_parts) if address_parts else "No address provided"


class ProductCategory(models.Model):
    CATEGORY_CHOICES = [
        ('pendants', 'Pendants'),
        ('necklaces', 'Necklaces'),
        ('rings', 'Rings'),
        ('bangles', 'Bangles'),
        ('earrings', 'Earrings'),
        ('mangalsutra', 'Mangalsutra'),
        ('bracelets', 'Bracelets'),
        ('chains', 'Chains'),
        ('nose-pins', 'Nose Pins'),
        ('solitaires', 'Solitaires'),
        ('watch-jewelry', 'Watch jewelry'),
        ('kada', 'Kada'),
        ('mens', 'Mens'),
        ('women', 'Women'),
        ('kids', 'Kids'),
        ('couple', 'Couple'),
        ('engagement', 'Engagement'),
        ('daily-wear', 'Daily Wear'),
        ('party-wear', 'Party Wear'),
        ('traditional', 'Traditional'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=32, choices=CATEGORY_CHOICES, unique=True, verbose_name="Category Name")
    display_name = models.CharField(max_length=50, verbose_name="Display Name")
    description = models.TextField(blank=True, verbose_name="Category Description")
    icon = models.CharField(max_length=50, blank=True, verbose_name="Category Icon")
    sort_order = models.PositiveIntegerField(default=0, verbose_name="Sort Order")
    is_active = models.BooleanField(default=True, verbose_name="Active")
    
    class Meta:
        ordering = ['sort_order', 'display_name']
        verbose_name = "Product Category"
        verbose_name_plural = "Product Categories"
    
    def __str__(self):
        return self.display_name
    
    def save(self, *args, **kwargs):
        if not self.display_name:
            for choice_value, choice_label in self.CATEGORY_CHOICES:
                if choice_value == self.name:
                    self.display_name = choice_label
                    break
        super().save(*args, **kwargs)


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Product Name")
    description = models.TextField(verbose_name="Product Description")
    image = models.ImageField(upload_to='product_images/', verbose_name="Product Image")
    hover_video = models.FileField(upload_to='product_videos/', blank=True, null=True, verbose_name="Product Hover Video", help_text="Video to play on hover (autoplay, muted, no controls)")

    categories = models.ManyToManyField(
        ProductCategory, 
        verbose_name="Product Categories",
        help_text="Select one or more categories for this product"
    )

    carat = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Carat Weight", help_text="Diamond/Gemstone carat weight")
    weight = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Total Weight (grams)", help_text="Total stone weight in grams")

    METAL_TYPE_CHOICES = [
        ('white_gold', 'White Gold'),
        ('yellow_gold', 'Yellow Gold'),
        ('rose_gold', 'Rose Gold'),
    ]
    metal_type = models.CharField(max_length=20, choices=METAL_TYPE_CHOICES, verbose_name="Metal Type")
    metal_purity = models.CharField(max_length=10, verbose_name="Metal Purity", help_text="e.g., 18K, 22K, 24K")

    has_diamond = models.BooleanField(default=False, verbose_name="Has Diamond")
    has_ruby = models.BooleanField(default=False, verbose_name="Has Ruby")
    has_sapphire = models.BooleanField(default=False, verbose_name="Has Sapphire")
    has_emerald = models.BooleanField(default=False, verbose_name="Has Emerald")
    has_pearl = models.BooleanField(default=False, verbose_name="Has Pearl")
    has_topaz = models.BooleanField(default=False, verbose_name="Has Topaz")
    has_other_gemstone = models.BooleanField(default=False, verbose_name="Has Other Gemstone")
    other_gemstone_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Other Gemstone Name")

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('out_of_stock', 'Out of Stock'),
        ('discontinued', 'Discontinued'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name="Product Status")

    BADGE_CHOICES = [
        ('premium', 'Premium'),
        ('best_seller', 'Best Seller'),
        ('new', 'New'),
        ('popular', 'Popular'),
        ('trending', 'Trending'),
        ('limited', 'Limited'),
        ('exclusive', 'Exclusive'),
        ('classic', 'Classic'),
    ]
    badge = models.CharField(max_length=20, choices=BADGE_CHOICES, blank=True, null=True, verbose_name="Product Badge")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name

    def get_categories_display(self):
        return ', '.join([cat.display_name for cat in self.categories.all()])

    def get_materials_list(self):
        materials = []
        materials.append(self.get_metal_type_display())
        if self.has_diamond:
            materials.append('Diamond')
        if self.has_ruby:
            materials.append('Ruby')
        if self.has_sapphire:
            materials.append('Sapphire')
        if self.has_emerald:
            materials.append('Emerald')
        if self.has_pearl:
            materials.append('Pearl')
        if self.has_topaz:
            materials.append('Topaz')
        if self.has_other_gemstone and self.other_gemstone_name:
            materials.append(self.other_gemstone_name)
        return materials


class DiscountCode(models.Model):
    code = models.CharField(max_length=10, unique=True, verbose_name="Discount Code")
    percentage = models.IntegerField(verbose_name="Discount Percentage")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    
    class Meta:
        verbose_name = "Discount Code"
        verbose_name_plural = "Discount Codes"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.code} - {self.percentage}%"


class UserDiscount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='discounts', verbose_name="User")
    discount_code = models.ForeignKey(DiscountCode, on_delete=models.CASCADE, verbose_name="Discount Code")
    percentage = models.IntegerField(verbose_name="Discount Percentage")
    is_used = models.BooleanField(default=False, verbose_name="Used")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    used_at = models.DateTimeField(null=True, blank=True, verbose_name="Used At")
    
    class Meta:
        verbose_name = "User Discount"
        verbose_name_plural = "User Discounts"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.discount_code.code} ({self.percentage}%)"
    
    def mark_as_used(self):
        self.is_used = True
        self.used_at = timezone.now()
        self.save()


class DiamondProduct(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='diamond_products')
    SHAPE_CHOICES = [
        ('round', 'Round'),
        ('oval', 'Oval'),
        ('princess', 'Princess'),
        ('cushion', 'Cushion'),
        ('emerald', 'Emerald'),
        ('marquise', 'Marquise'),
        ('pear', 'Pear'),
        ('heart', 'Heart'),
        ('asscher', 'Asscher'),
        ('radiant', 'Radiant'),
        ('trillion', 'Trillion'),
        ('baguette', 'Baguette'),
        ('hexagon', 'Hexagon'),
        ('lozenge', 'Lozenge'),
        ('shield', 'Shield'),
        ('tapered_baguette', 'Tapered Baguette'),
        ('briolette', 'Briolette'),
        ('half_moon', 'Half Moon'),
        ('square_caution', 'Square Caution'),
        ('coffin', 'Coffin'),
        ('square_radiant', 'Square Radiant'),
        ('bullet', 'Bullet'),
        ('trapezoid', 'Trapezoid'),
    ]
    COLOR_CHOICES = [
        ('D', 'D'), ('E', 'E'), ('F', 'F'), ('G', 'G'), ('H', 'H'), 
    ]
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('sold', 'Sold'),
        ('reserved', 'Reserved'),
        ('inactive', 'Inactive'),
    ]
    BADGE_CHOICES = [
        ('premium', 'Premium'),
        ('best_seller', 'Best Seller'),
        ('new', 'New'),
        ('exclusive', 'Exclusive'),
        ('limited', 'Limited'),
    ]
    CLARITY_CHOICES = [
        ('IF', 'IF (Internally Flawless)'),
        ('VVS1', 'VVS1 (Very Very Slightly Included 1)'),
        ('VVS2', 'VVS2 (Very Very Slightly Included 2)'),
        ('VS1', 'VS1 (Very Slightly Included 1)'),
        ('VS2', 'VS2 (Very Slightly Included 2)'),
        ('SI1', 'SI1 (Slightly Included 1)'),
      
    ]
    CUT_CHOICES = [
        ('ideal', 'Ideal'),
        ('excellent', 'Excellent'),
        ('very_good', 'Very Good'),
       
    ]
    CERTIFICATION_CHOICES = [
        ('GIA', 'GIA'),
        ('IGI', 'IGI'),
    ]
    name = models.CharField(max_length=255, verbose_name="Diamond Name")
    description = models.TextField(verbose_name="Description")
    image = models.ImageField(upload_to='product_images/', verbose_name="Diamond Image")
    origin = models.CharField(max_length=100, null=True, blank=True, verbose_name="Origin")
    carat = models.DecimalField(max_digits=6, decimal_places=3, verbose_name="Carat Weight")
    shape = models.CharField(max_length=30, choices=SHAPE_CHOICES, verbose_name="Shape")
    color = models.CharField(max_length=2, choices=COLOR_CHOICES, verbose_name="Color Grade")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available', verbose_name="Status")
    badge = models.CharField(max_length=20, choices=BADGE_CHOICES, blank=True, null=True, verbose_name="Badge")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Diamond Product"
        verbose_name_plural = "Diamond Products"

    def __str__(self):
        return f"{self.name} ({self.carat} ct, {self.get_shape_display()})"


class Payment(models.Model):
    
    PLATFORM_CHOICES = [
        ('razorpay', 'Razorpay'),
    ]
    
    STATUS_CHOICES = [
        ('created', 'Created'),
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]
    
    CURRENCY_CHOICES = [
        ('INR', 'Indian Rupee (INR)'),
        ('USD', 'US Dollar (USD)'),
        ('EUR', 'Euro (EUR)'),
        ('GBP', 'British Pound (GBP)'),
        ('CAD', 'Canadian Dollar (CAD)'),
        ('AUD', 'Australian Dollar (AUD)'),
        ('SGD', 'Singapore Dollar (SGD)'),
        ('AED', 'UAE Dirham (AED)'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments', verbose_name="User")
    email = models.EmailField(verbose_name="User Email")
    
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Amount Paid")
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='INR', verbose_name="Currency")
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES, default='razorpay', verbose_name="Payment Platform")
    
    payment_id = models.CharField(max_length=100, verbose_name="Payment ID")
    order_id = models.CharField(max_length=100, verbose_name="Order ID")
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True, verbose_name="Razorpay Payment ID")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created', verbose_name="Payment Status")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="Completed At")
    
    description = models.CharField(max_length=255, default="Custom Payment", verbose_name="Payment Description")
    notes = models.TextField(blank=True, verbose_name="Additional Notes")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Payment"
        verbose_name_plural = "Payments"

    def __str__(self):
        return f"{self.user.username} - {self.amount} {self.currency} via {self.get_platform_display()} - {self.status}"
    
    def get_formatted_amount(self):
        currency_symbols = {
            'INR': '₹',
            'USD': '$',
            'EUR': '€',
            'GBP': '£',
            'CAD': 'C$',
            'AUD': 'A$',
            'SGD': 'S$',
            'AED': 'د.إ',
        }
        symbol = currency_symbols.get(self.currency, self.currency)
        return f"{symbol}{self.amount}"
    
    def get_total_payment_amount(self):
        
        conversion_rates = {
            'INR': 1,
            'USD': 83,   
            'EUR': 90,
            'GBP': 105,
            'CAD': 61,
            'AUD': 54,
            'SGD': 61,
            'AED': 22.5,
        }
        rate = conversion_rates.get(self.currency, 1)
        return self.amount * rate

