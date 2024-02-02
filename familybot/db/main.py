from familybot.db.crud import *
from familybot.db.models import Person

create_tables()

# TODO
#
me = Person(telegram_tag='gelbal', name='Gleb')

insert_persons([me])

print(get_person_by_tg('gelbal'))

me.added_purchases. Purchase(product_name='test', amount=12, unit_price=13)
