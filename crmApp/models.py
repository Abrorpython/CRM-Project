from django.db import models
from django.contrib.auth.models import AbstractUser


# for user
class User(AbstractUser):

    CHOICES = [

        ("Rahbar", "Rahbar"),
        ("Menejer", "Menejer"),
        ("Agent", "Agent")

    ]

    role = models.CharField(choices=CHOICES, max_length=20)
    tel = models.CharField(max_length=32)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} | {self.username}"


# Category
class Category(models.Model):
    name = models.CharField('Kategoriya', max_length=255)
    date = models.CharField(max_length=32)
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-data']
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"


# Mahsulotlar uchun
class Product(models.Model):

    PARAMETR_CHOICE = [

        ("metr", "metr"),
        ("dona", "dona"),
        ("kg", "kg")

    ]

    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Kategoriya nomi')
    name = models.CharField(verbose_name='Mahsulot nomi', max_length=255)
    parametr = models.CharField(verbose_name='Mahuslot birligi', choices=PARAMETR_CHOICE, max_length=32)
    image = models.ImageField(verbose_name='Mahsulot rasmi')
    qr = models.CharField(verbose_name='Q/R', max_length=255, unique=True)
    amount = models.FloatField(verbose_name='Mahsulot miqdori')
    sel_price = models.FloatField(verbose_name='Olingan narx')
    finish_price = models.FloatField(verbose_name='Sotiladigan oxirgi narx')
    date = models.CharField(verbose_name="Mahsulot qo'shilgan vaqt", max_length=32)
    descriptions = models.TextField(verbose_name="Mahsulot haqida ma'lumot")
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{str(self.id)} | {self.name}"

    class Meta:
        ordering = ['-data']
        verbose_name = 'Mahsulot'
        verbose_name_plural = 'Mahsulotlar'


# Mijozlar
class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(verbose_name='F.I.Sh', max_length=255)
    number = models.CharField(verbose_name='Tel Number', max_length=32)
    descriptions = models.TextField(verbose_name="Mijoz haqida ma'lumot")
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{str(self.id)} | {self.name}"

    class Meta:
        ordering = ['-create_at']
        verbose_name = 'Mijoz'
        verbose_name_plural = 'Mijozlar'


# Kirimlar uchun
class Income(models.Model):
    income = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Kirim summasi')
    descriptions = models.TextField(verbose_name="Ma'lumot")
    data = models.CharField(max_length=32)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{str(self.data)} sanada {self.income} kirim bo'lgan"

    class Meta:
        ordering = ['-date']
        verbose_name = 'Kirimlar'
        verbose_name_plural = 'Kirim'


#Chiqimlar uchun
class Expense(models.Model):
    expense = models.DecimalField(max_digits=12, decimal_places=2, verbose_name='Chiqim summasi')
    descriptions = models.TextField(verbose_name="Ma'lumot")
    data = models.CharField(max_length=32)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{str(self.data)} sanada {self.expense} chiqim bo'lgan"

    class Meta:
        ordering = ['-date']
        verbose_name = 'Chiqimlar'
        verbose_name_plural = 'Chiqim'


# har bir agent sotayotgan producti uchun
class AgentSalesProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, db_column='user')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, db_column='product')
    quantity = models.FloatField()
    data = models.CharField(max_length=100)
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} | {self.user.username} | sotdi: {self.product} dona: {self.quantity}"

    class Meta:
        verbose_name = "Agent sotgan mahsulotlar"
        verbose_name_plural = "Agent sotgan mahsulotlar"
