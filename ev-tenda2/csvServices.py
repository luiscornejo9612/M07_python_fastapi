import pandas as pd

# *************************************************************************************************

def load_csv_category(file):
    categories = []
    data_csv = pd.read_csv(file, header=0)
    for _, row in data_csv.iterrows():
        category = {
            'category_id': row['id_categoria'],
            'name_category': row['nom_categoria']
        }
        categories.append(category)
    return categories

def load_csv_subcategory(file):
    subcategories = []
    data_csv = pd.read_csv(file, header=0)
    for _, row in data_csv.iterrows():
        subcategory = {
            'subcategory_id': row['id_subcategoria'],
            'category_id': row['id_categoria'],
            'name_subcategory': row['nom_subcategoria']
        }
        subcategories.append(subcategory)
    return subcategories

def load_csv_product(file):
    products = []
    data_csv = pd.read_csv(file, header=0)
    for _, row in data_csv.iterrows():
        product = {
            'product_id': row['id_producto'],
            'name_product': row['nom_producto'],
            'description': row['descripcion_producto'],
            'company': row['companyia'],
            'price': row['precio'],
            'units': row['unidades'],
            'subcategory_id': row['id_subcategoria']
        }
        products.append(product)
    return products

