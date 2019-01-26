from django.contrib import admin
from .models import Admin, Medicine, Transaction, User

# Register your models here.
admin.site.register(Admin)
admin.site.register(Medicine)
admin.site.register(Transaction)
admin.site.register(User)
