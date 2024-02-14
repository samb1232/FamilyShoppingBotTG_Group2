from familybot.db.crud import *
from familybot.db.models import Person

create_tables()

me = Person(telegram_tag='gelbal', name='Gleb')

insert_persons([me])

print(get_person_by_tg('gelbal'))

chocolate = Purchase(product_name='Chcocolate', amount=2, unit_price=13)

me.add_purchase(chocolate)

print(me.added_purchases)
