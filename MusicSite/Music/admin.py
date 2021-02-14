from django.contrib import admin
from Music.models import AuthCodes, Counter, DocsRequest, Track, Scan, PaspInfo

admin.site.register(AuthCodes)
admin.site.register(Counter)
admin.site.register(DocsRequest)
admin.site.register(Track)
admin.site.register(Scan)
admin.site.register(PaspInfo)
