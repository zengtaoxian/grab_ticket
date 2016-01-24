# -*- coding: utf-8 -*-
__author__ = 'zengtaoxian'

from django.contrib import admin
from models import Account, Passenger, Train, Seat, BackupDate, Ticket, IDCode


class AccountAdmin(admin.ModelAdmin):
    pass


class PassengerAdmin(admin.ModelAdmin):
    pass


class TrainAdmin(admin.ModelAdmin):
    pass


class SeatAdmin(admin.ModelAdmin):
    pass


class BackupDateAdmin(admin.ModelAdmin):
    pass


class TicketAdmin(admin.ModelAdmin):
    pass


class IDCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'result', 'index')
    search_fields = ('code',)


admin.site.register(Account, AccountAdmin)
admin.site.register(Passenger, PassengerAdmin)
admin.site.register(Train, TrainAdmin)
admin.site.register(Seat, SeatAdmin)
admin.site.register(BackupDate, BackupDateAdmin)
admin.site.register(Ticket, TicketAdmin)
admin.site.register(IDCode, IDCodeAdmin)