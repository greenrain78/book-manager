from dataclasses import dataclass


@dataclass
class Category:
    cat_id: str
    cat_name: str


datalist = [
    Category(cat_id="CAT01", cat_name="programming"),
    Category(cat_id="CAT11", cat_name="graphics"),
    Category(cat_id="CAT02", cat_name="database"),
    Category(cat_id="CAT03", cat_name="network"),
]

input_value = "!database"

result = []