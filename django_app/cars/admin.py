from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django import forms
from django.forms.widgets import HiddenInput
from django.db import models
from .models import Car, Brand, Model, CarImage
from adminsortable2.admin import SortableAdminBase, SortableInlineAdminMixin

def icon_brand(obj):
    return format_html('<i class="fas fa-car"></i> {}'.format(obj.brand.name))
icon_brand.short_description = 'Brand'

def remove_image(modeladmin, request, queryset):
    queryset.update(image=None)
remove_image.short_description = "Remover imagem principal"

class CarAdminForm(forms.ModelForm):
    class Meta:
        model = Car
        fields = '__all__'

    def save(self, commit=True):
        car = super().save(commit=False)
        if self.cleaned_data.get('remove_image') and car.image:
            car.image.delete(save=False)
            car.image = None
        if commit:
            car.save()
        return car

class CarImageInline(SortableInlineAdminMixin, admin.TabularInline):
    model = CarImage
    extra = 1
    fields = ['order', 'image', 'image_preview']
    readonly_fields = ['image_preview']
    ordering = ('order',)
    formfield_overrides = {
        models.PositiveIntegerField: {'widget': HiddenInput()},
    }

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="100" height="100" style="object-fit:cover;" />'.format(obj.image.url)
            )
        return "Sem imagem"
    image_preview.short_description = "Pré-visualização"

    class Media:
        js = (
            'admin/js/jquery.init.js',
            'adminsortable2/js/libs/jquery.ui.core-1.11.4.min.js',
            'adminsortable2/js/libs/jquery.ui.widget-1.11.4.min.js',
            'adminsortable2/js/libs/jquery.ui.mouse-1.11.4.min.js',
            'adminsortable2/js/libs/jquery.ui.sortable-1.11.4.min.js',
            'adminsortable2/js/inline-sortable.js',
        )

class CarAdmin(SortableAdminBase, admin.ModelAdmin):
    form = CarAdminForm
    inlines = [CarImageInline]

    list_display = (
        'id', 'model', 'brand', 'factory_year', 'model_year',
        'price', 'status', 'mileage', 'image_display',
        'created_at', 'updated_at'
    )
    list_display_links = ('id', 'model')
    list_editable = ('price', 'status', 'mileage', 'factory_year', 'model_year')
    search_fields = ('model__name', 'brand__name', 'factory_year', 'model_year', 'price')
    list_per_page = 25
    list_filter = ('status', 'fuel_type', 'factory_year')
    actions = [remove_image]

    def image_display(self, obj):
        if obj.images.exists():
            main_image = obj.images.order_by('order').first()
            return format_html(
                '<img src="{}" width="350" height="350" style="object-fit:cover;" />'.format(main_image.image.url)
            )
        return "Sem imagem"
    image_display.short_description = "Imagem Principal"

admin.site.register(Car, CarAdmin)

class BrandAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at', 'updated_at')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    list_per_page = 25

admin.site.register(Brand, BrandAdmin)

class ModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', icon_brand, 'created_at', 'updated_at')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'brand__name')
    list_per_page = 25

admin.site.register(Model, ModelAdmin)
