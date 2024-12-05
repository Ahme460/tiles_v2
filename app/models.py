from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
class CustomUserManager(BaseUserManager):
    
    def create_user(slef,email,password,**extra_fields):

        """
        create and save normal user

        """

        if not email:
            raise ValueError("The Email must be set")
        
        email=slef.normalize_email(email=email)
        user=slef.model(email=email,**extra_fields)
        user.set_password(password)
        user.save()
        return user
    

    def create_superuser(self,email,password,**extra_fields):
        
        " create superuser "

        extra_fields.setdefault("is_staff",True)
        extra_fields.setdefault("is_active",True)
        extra_fields.setdefault("is_superuser",True)
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        email=self.normalize_email(email)
        return self.create_user(email,password,**extra_fields)

class Users(AbstractUser):
    username=None
    name=models.CharField(max_length=50)
    email=models.EmailField(unique=True)
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]
    objects=CustomUserManager()

    def __str__(self) -> str:
        return self.username


class Category(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

class Type(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='types')
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.category.name})"
    

class Factory(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='factories/', blank=True, null=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    

class Color(models.Model):
    name = models.CharField(max_length=50)
    color_code = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    

class Size(models.Model):
    dimensions = models.CharField(max_length=50)

    def __str__(self):
        return self.dimensions


class Product(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='products/', blank=True, null=True, default='Decor_tiles_1.jpg') 
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discription = models.TextField(blank=True, null=True) 
    type = models.ForeignKey(Type, on_delete=models.CASCADE, related_name='products')
    factory = models.ForeignKey(Factory, on_delete=models.SET_NULL, null=True)
    color = models.ForeignKey(Color, on_delete=models.SET_NULL, null=True)
    size = models.ForeignKey(Size, on_delete=models.SET_NULL, null=True)
    code = models.CharField(max_length=100, unique=True)
    texture = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.code} - {self.type.name} ({self.size.dimensions} {self.color })"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(f"{self.name}-{self.code}")
            slug = base_slug
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)
        


