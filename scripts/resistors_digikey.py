from arius.api import AriusAPI
from arius.part import Part, PartCategory
from arius.base import Parameter
from arius.company import Company, ManufacturerPart, SupplierPart, ManufacturerPartParameter

import os
import sys
import digikey
from digikey.v3.productinformation import KeywordSearchRequest

os.environ['DIGIKEY_CLIENT_ID'] = 'DjV4w1v0ebNTiL7Nqvslw0GkNYuYdrLG'
os.environ['DIGIKEY_CLIENT_SECRET'] = 'dK0dTRimeq3aiPH1'
os.environ['DIGIKEY_CLIENT_SANDBOX'] = 'False'
os.environ['DIGIKEY_STORAGE_PATH'] = 'C:\\Users\\Oliver\\Desktop\\digikey\\'

ARIUS_URL = "http://localhost:8000"
ARIUS_USERNAME = "admin"
ARIUS_PASSWORD = "arius"

arius = AriusAPI(ARIUS_URL, username=ARIUS_USERNAME, password=ARIUS_PASSWORD)

resistors = Part.list(arius, category=5)

def getParameter(result, name):

    for param in result.parameters:
        if param.parameter.lower() == name.lower():
            return param

    return None


def getValue(result, name):

    param = getParameter(result, name)

    if param:
        return param.value
    else:
        return None

manufacturers = {}

DIGIKEY_PK = 1

for res in resistors:

    search_term = res.name.replace('_', ' ').replace('R ' , 'Resistor ')

    print(res.name, res.description)

    request = KeywordSearchRequest(search_term, record_count=25)

    result = digikey.keyword_search(body=request)

    # Set of manufacturer part numbers
    MPN = set()

    for product in result.products:

        mpn = product.manufacturer_part_number

        print(f"> {mpn}")

        if mpn in MPN or len(MPN) >= 5:
            continue

        MPN.add(mpn)

        sku = product.digi_key_part_number

        man_name = product.manufacturer.value

        if man_name in manufacturers.keys():
            manufacturer = manufacturers[man_name]
        else:

            # Search Arius for manufacturer name
            query = Company.list(arius, search=man_name)

            if len(query) == 0:

                print(f"Creating new manufacturer: '{man_name}'")
                
                manufacturer = Company.create(arius, data={
                    'is_supplier': False,
                    'is_manufacturer': True,
                    'name': man_name,
                })

            else:
                manufacturer = query[0]

            manufacturers[man_name] = manufacturer

        m_parts = ManufacturerPart.list(arius, MPN=mpn)

        print("Existing Manufacturer Parts:")

        for mp in m_parts:
            print(f" - {mp.MPN}, {mp.manufacturer}")

        if len(m_parts) == 0:
            print(f"Creating new part: {man_name} -> {mpn}")
            manufacturer_part = ManufacturerPart.create(arius, data={
                'part': res.pk,
                'manufacturer': manufacturer.pk,
                'MPN': mpn,
            })
        else:
            manufacturer_part = m_parts[0]

        # Check if a "supplier part" exists
        s_parts = SupplierPart.list(
            arius,
            manufacturer_part=manufacturer_part.pk,
            supplier=DIGIKEY_PK
        )

        if s_parts is None or len(s_parts) == 0:
            print(f"Creating new supplier part")

            SupplierPart.create(arius, data={
                'part': res.pk,
                'supplier': DIGIKEY_PK,
                'manufacturer_part': manufacturer_part.pk,
                'SKU': sku,
                'link': product.product_url,
                'description': product.product_description,
            })
                
