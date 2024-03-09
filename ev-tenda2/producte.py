def product_schema(product) -> dict:
    return{
        "product_id":product[0],
        "name":product[1],
        "description":product[2],
        "company":product[3],
        "price":product[4],
        "units":product[5],
        "subcategory_id":product[6],
    }
def products_schema(prods)->dict:
    return [product_schema(prod) for prod in prods]

def allProducts_schema(data)->dict:
    return { "category_name": data[0],
              "subcategory_name" : data[1],
              "product_name":data[2],
              "product_brand": data[3],
              "product_price":data[4]
            }
    
def products_Allschema(data)-> dict:
    return[allProducts_schema(prod) for prod in data]  