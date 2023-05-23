# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re


class BookscraperPipeline:
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)

        ## !Description ==> item.strip()
        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name != 'description':
                value = adapter.get(field_name)
                adapter[field_name] = value.strip()

        ##Category & Product ==> item.lowercase()
        lowercase_keys = ['category', 'product_type']
        for lowercase_key in lowercase_keys:
            value = adapter.get(lowercase_key)
            adapter[lowercase_key] = value.lower()

        ##Price ==> float(item)
        price_keys = ['price', 'price_excl_tax', 'price_incl_tax', 'tax']
        for price_key in price_keys:
            value = adapter.get(price_key)
            value = value.replace('£', '')
            adapter[price_key] = float(value)

        ##Availability ==> remove extra text from strings
        value = adapter.get('availability')
        value = re.findall('\d+', str(value))[0]
        adapter['availability'] = float(value)

        ##Reviews ==> int(item)
        value = adapter.get('num_reviews')
        adapter['num_reviews'] = int(value)

        ##Stars ==> converting to readable values
        value = adapter.get('stars')
        value = value.split(' ')
        value = value[1].lower()
        if value == "one":
            adapter['stars'] = 1
        elif value == 'two':
            adapter['stars'] = 2
        elif value == "three":
            adapter['stars'] = 3
        elif value == "four":
            adapter['stars'] = 4
        elif value == "five":
            adapter['stars'] = 5

        return item