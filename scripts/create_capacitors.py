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

category = 6

packages = [
    '0402',
    '0603',
    '0805',
]

values = [
    # '100pF',
    '100nF',
    '1uF',
    '10uF',
]

for package in packages:
    for value in values:
        name = f"C_{value}_{package}"
        description = f"{value} in {package} SMD package"
        keywords = "cap smd ceramic"

        Part.create(api, data={
            'name': name,
            'category': category,
            'description': description,
            'keywords': keywords,
            'purchaseable': True,
        })
