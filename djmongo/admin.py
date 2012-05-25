from django.contrib import admin


class NoSqlModelAdmin(admin.ModelAdmin):
    form_change_template = 'admin/nosql/form_change.html'
