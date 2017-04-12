from django.contrib import admin

from . import models


@admin.register(models.ProgrammingLanguage)
class ProgrammingLanguageAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order')
    list_editable = ('order',)
    search_fields = ('name',)
    save_on_top = True


@admin.register(models.Technology)
class TechnologyAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order')
    list_editable = ('order',)
    search_fields = ('name',)
    save_on_top = True


@admin.register(models.TechnologyMasteringLevel)
class TechnologyMasteringLevelAdmin(admin.ModelAdmin):
    list_display = ('user', 'technology', 'self_rate', 'activity', 'removed')
    raw_id_fields = ('user',)
    list_filter = ('removed', 'activity')
    search_fields = ('user__username',)


@admin.register(models.Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order')
    list_editable = ('order',)
    search_fields = ('name',)
    save_on_top = True


@admin.register(models.Software)
class SoftwareAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    list_editable = ('order',)
    search_fields = ('name',)
    save_on_top = True


@admin.register(models.Hardware)
class HardwareAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    list_editable = ('order',)
    search_fields = ('name',)
    save_on_top = True


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'location', 'rate', 'is_available', 'birth_year', 'total_points', 'is_ready')
    search_fields = ('user__username', 'name', 'location')
    list_filter = ('sex', 'is_available', 'banned', 'is_ready', 'english_level')
    raw_id_fields = ('user',)
    readonly_fields = ('created_at',)
    save_on_top = True


