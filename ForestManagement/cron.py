from ForestManagement.models import Contract, Order
import datetime
from datetime import date
def mycronjob():
    contracts = Contract.objects.all()
    for row in contracts:
        frequency = row.frequency
        last_update = row.last_created_date
        present_date = date.today
        dl = present_date - last_update
        if frequency == 'Monthly':
            if(dl >30):
                Order.objects.create(item = row.item,
                ordered_quantity = row.ordered_quantity,
                ordered_date = present_date,
                delivery_date = present_date,
                user_name = row.user_name)
                Contract.objects.filter(pk = row.id).update(last_created_date = present_date)
        else:
            if(dl >365):
                Order.objects.create(item = row.item,
                ordered_quantity = row.ordered_quantity,
                ordered_date = present_date,
                delivery_date = present_date,
                user_name = row.user_name)
                Contract.objects.filter(pk = row.id).update(last_created_date = present_date)




            

