from django.contrib import admin
from feedback.models import Marksheet, FeedbackCategories, GroupMarksheet

admin.site.register(Marksheet)
admin.site.register(GroupMarksheet)
admin.site.register(FeedbackCategories)
