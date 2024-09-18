from django.contrib import admin
from red_book_server.models.models import Category, RedBookItem, RedBookLocation, RedBookItemRequest

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    model = Category


@admin.register(RedBookItem)
class RedBookItemAdmin(admin.ModelAdmin):
    model = RedBookItem


@admin.register(RedBookLocation)
class RedBookLocation(admin.ModelAdmin):
    model = RedBookLocation


class VerificationModelAdmin(admin.ModelAdmin):
    change_list_template = 'verification.html'

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)
            
        response.context_data.update({
            'red_book_item_requests': RedBookItemRequest.objects.all(),
        })
        
        return self.add_custom_changelist_view(response)

    def add_custom_changelist_view(self, response):
        return response

@admin.register(RedBookItemRequest)
class RedBookItemRequestAdmin(VerificationModelAdmin):
    model = RedBookItemRequest
