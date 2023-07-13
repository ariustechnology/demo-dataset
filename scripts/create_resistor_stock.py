from arius.api import AriusAPI

from arius.part import Part, PartCategory
from arius.stock import StockItem, StockLocation
from arius.company import SupplierPart

import random
import sys

ARIUS_URL = "http://localhost:8000"
ARIUS_USERNAME = "admin"
ARIUS_PASSWORD = "arius"

api = AriusAPI(ARIUS_URL, username=ARIUS_USERNAME, password=ARIUS_PASSWORD)

resistors = Part.list(api, category=5)

storage = StockLocation(api, pk=8)

count = 0

for resistor in resistors:

    if random.random() > 0.65:
        continue

    q = random.random()

    quantity = 1000

    if q < 0.1:
        quantity = 2000

    elif q > 0.85:
        quantity = 4000

    # Get the first matching supplierpart
    sp_list = SupplierPart.list(api, part=resistor.pk)

    for sp in sp_list:
        if random.random() > 0.6:
            continue

        status = 10

        if random.random() > 0.95:
            status = 55  # Damaged
        elif random.random() > 0.95:
            status = 50  # Attention

        StockItem.create(api, data={
            'location': storage.pk,
            'part': resistor.pk,
            'quantity': quantity,
            'supplier_part': sp.pk,
            'packaging': 'reel',
            'status': status,
        })

        count += 1

print(f"Created {count} new stock items")
    
    
