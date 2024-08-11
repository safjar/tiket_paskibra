from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from bayar.models import Payment,Product,Order,OTS
# Register your models here.

admin.site.register(Payment)
admin.site.register(Product)
admin.site.register(OTS)

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'get_qr_code_link']

    def get_qr_code_url(self, obj):
        return obj.get_qr_code_url()
    
    def get_order_id(self, obj):
        return obj.order_id

    get_order_id.short_description = 'Order ID'

    def get_qr_code_link(self, obj):
        url = self.get_qr_code_url(obj)
        return mark_safe('<a href="{}" target="_blank">View QR Code</a>'.format(url))

    get_qr_code_link.short_description = 'QR Code'

admin.site.register(Order, OrderAdmin)