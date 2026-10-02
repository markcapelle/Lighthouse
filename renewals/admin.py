from django.contrib import admin
from .models import Renewal, RenewalStatus, RenewalArchive

admin.site.register(Renewal)
admin.site.register(RenewalStatus)
admin.site.register(RenewalArchive)
