from django.contrib import admin
from .models import User, Account, Location, Cleaner, Booking, Contractor, Clean, Selector, AccountUser, Comment

# Register your models here.
admin.site.register(User)
admin.site.register(Account)
admin.site.register(AccountUser)
admin.site.register(Location)
admin.site.register(Cleaner)
admin.site.register(Booking)
admin.site.register(Contractor)
admin.site.register(Clean)
admin.site.register(Comment)
admin.site.register(Selector)






