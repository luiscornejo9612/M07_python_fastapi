from db import db_config
import csvServices



#******************************************************************************************************
# función get all de la tabla products
def getAll():
    data = None  # Definir data antes del bloque try-except
    try:
        conn = db_config.clent()  # Corrección: client en lugar de clent
        cur = conn.cursor()
        cur.execute("SELECT * FROM product")
        data = cur.fetchall()
    except Exception as e:
        print(f"Error de conexión: {e}")
    finally:
        if conn:  # Verificar si la conexión existe antes de cerrarla
            conn.close()
    return f"Consulta: {data}"  # Devolver falso incluso si hay una excepción




# *****************************************************************************************************
# fucion get by id:
def getbyID(id: int):
    data = None  # Definir data antes del bloque try-except
    try:
        conn = db_config.clent()
        cur = conn.cursor()
        cur.execute(f"select * from product where product_id = {id}")
        data = cur.fetchone()

    except Exception as e:
     print(f"error de coneccion {e}")
    finally:
        conn.close()
        return f"consulta {data}"
    



# ******************************************************************************************************
# Funcion post
def create_product(prod):
    try:
        conn = db_config.clent()
        cur = conn.cursor()

        sql = f"""
                INSERT INTO public.product(
	            product_id, name, description, company, price, units, subcategory_id, created_at, updated_at)
	            VALUES ({prod.product_id}, '{prod.name}', '{prod.description}', '{prod.company}', {prod.price}, 
                {prod.units}, {prod.subcategory_id}, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
                """
        cur.execute(sql)
        conn.commit()
        return {"message": f"Producto creado exitosamente con el nombre {prod.name}"}
    except Exception as e:
        return {"error": f"No se pudo crear el producto. Error: {e}"}
    finally:
        if conn:
            conn.close()




# ************************************************************************************************************
# Funcion put
def update_product(prod):
    try:
        conn = db_config.clent()
        cur = conn.cursor()

        sql = f"""
                UPDATE public.product
                SET name = '{prod.name}',
                    description = '{prod.description}',
                    company = '{prod.company}',
                    price = {prod.price},
                    units = {prod.units},
                    subcategory_id = {prod.subcategory_id},
                    updated_at = CURRENT_TIMESTAMP
                WHERE product_id = {prod.product_id};
                """
        cur.execute(sql)
        conn.commit()
        if cur.rowcount > 0:
            return {"message": f"Producto con ID {prod.product_id} actualizado exitosamente"}
        else:
            return {"message": f"No se encontró ningún producto con ID {prod.product_id}"}
    except Exception as e:
        return {"error": f"No se pudo actualizar el producto. Error: {e}"}
    finally:
        if conn:
            conn.close()
 

# *************************************************************************************************************
# Funcion delete
def delete_product(id: int):
    data = None  # Definir data antes del bloque try-except
    try:
        conn = db_config.clent()
        cur = conn.cursor()
        cur.execute(f"DELETE from product where product_id = {id}")
        conn.commit()
    except Exception as e:
     print(f"error de coneccion {e}")
    finally:
        conn.close()
        return "se ha elinimado"
    
# ********************************************************************************************************************

def read():
    try:
        conn = db_config.clent()
        cur = conn.cursor()
        cur.execute(f"select * from public.test")
        prod = cur.fetchall()
        data = {"status": 1, "data": prod}
    except Exception as e:
        data = {"status": 1, "data": prod}
    
    finally:
        conn.close()

    return data

def readById(id: int):
    try:
        conn = db_config.clent()
        cur = conn.cursor()
        cur.execute(f"select * from public.test where id={id}")

        result = cur.fetchone()
    except Exception as e:
        result = {"estado": 0, "mensaje": str(e)}
    finally:
        conn.close()

    return result



# *****************************************************************************************************
#InsercionesMasivas desde CSV a la BD
def insertCategory():
    clientDB = db_config.clent() 
    cur = clientDB.cursor()
    try:
        listaCategory = csvServices.load_csv_category('llista_productes.csv')
        for item in listaCategory:
            id_categoria=item['category_id']
            nombre_categoria=item['name_category']
          
            cur.execute(f"""SELECT * 
                        FROM category 
                        where category_id = {id_categoria}""")
            validationQuery = cur.fetchone()

            #Si no existe se hace un insert en la base de datos
            if not validationQuery:
                insert= (f"""INSERT INTO category
                         ( category_id, name, created_at, updated_at)
                        VALUES
                        ({id_categoria}, '{nombre_categoria}', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);""")   
                cur.execute(insert) 
            
                clientDB.commit()
    except Exception as e:
      clientDB.rollback()
      print('Error : ', e)    
    finally:
      cur.close()

def insertSubCategory():
    clientDB = db_config.clent()
    cur = clientDB.cursor()
    try:
        listaSubCategory = csvServices.load_csv_subcategory ('llista_productes.csv')
        for item in listaSubCategory:
            id_categoria= item['category_id']
            id_subcategoria= item['subcategory_id']
            nombre_subcategoria= item['name_subcategory']

            #Comprobación de si existe este item en la BD
            cur.execute(f"""SELECT * FROM subcategory where subcategory_id = {id_subcategoria}""")
            validationQuery = cur.fetchone()

            #Si no existe se hace un insert
            if not validationQuery:
                insert= (f"""INSERT INTO subcategory( subcategory_id, name,category_id, created_at, updated_at)
                    VALUES ({id_subcategoria}, '{nombre_subcategoria}','{id_categoria}', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);""")   
                cur.execute(insert)
                clientDB.commit()
    except Exception as e:
      clientDB.rollback()
      print('Error : ', e)    
    finally:
      cur.close()

def insertProducts():
    clientDB = db_config.clent() 
    cur = clientDB.cursor()
    try:
        listaProductos = csvServices.load_csv_product('llista_productes.csv')
        for item in listaProductos:
            id_prod= item['product_id']
            nom_prod= item['name_product']
            descripcion= item['description']
            company = item["company"]
            precio= item["price"]
            unid = item["units"]
            subcategory_id = item["subcategory_id"]
            #Comprobación de si existe este en la BD
            cur.execute(f"""SELECT * FROM product where product_id  = {id_prod}""")
            validationQuery = cur.fetchone()
            #Si existe actualizamos
            if(validationQuery):
                update_product(id_prod,nom_prod,descripcion,company,precio,unid,subcategory_id)
            #Si no existe insertamos
            else:
                insert= (f"""INSERT INTO product(
	                         product_id, name, description, company, price, units, subcategory_id, created_at, updated_at)
	                         VALUES ({id_prod}, '{nom_prod}', '{descripcion}', '{company}', {precio}, {unid}, {subcategory_id}, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);""")
                cur.execute(insert)     
                clientDB.commit()
    except Exception as e:
      clientDB.rollback()
      print('Error : ', e)    
    finally:
      cur.close()





































# def insert_update(id,name):
#     try:
#         if (not(get_product_ById(id) is None)):
#             try:
#                 conn = db_config.clent()
#                 cur = conn.cursor()
#                 cur.execute(f"UPDATE public.category SET category_id={id}, name='{name}', created_at=CURRENT_TIMESTAMP, updated_at=CURRENT_TIMESTAMP WHERE category_id={id};")
#                 conn.commit()

#             except Exception as e:
#                 return f'Error conexión {e}'
            
#             finally:
#                 conn.close()
#         else:
#             try:
#                 conn = db_config.clent()
#                 cur = conn.cursor()
#                 sql = f"INSERT INTO public.category(category_id, name, created_at, updated_at) VALUES ({id}, '{name}', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);"
#                 cur.execute(sql)
#                 conn.commit()

#             except Exception as e:
#                 return f'Error conexión {e}'
            
#             finally:
#                 conn.close()
                
#     except Exception as e:
#         return f'Error conexión {e}'
    
#     finally:
#         return f"Producto añadido o actualizado"



# def crear_registro(prod):
#     try:
#         conn = db_config.clent()
#         cur = conn.cursor()
#         sql = f"""
#                 INSERT INTO public.product(
# 	            product_id, name, description, company, price, units, subcategory_id, created_at, updated_at)
# 	            VALUES ({prod.product_id}, '{prod.name}', '{prod.description}', '{prod.company}', {prod.price}, 
#                 {prod.units}, {prod.subcategory_id}, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
#                 """
#         cur.execute(sql)
#         conn.commit()
#         return {"mensaje": "Registro creado exitosamente"}
#     except Exception as e:
#         return {"error": str(e)}
#     finally:
#         conn.close()

def getAll_category():
    try:
        conn = db_config.clent()
        cur = conn.cursor()
        cur.execute("SELECT * FROM category")
        registros = cur.fetchall()
        return registros
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()

def get_category_Byid(id):
    try:
        conn = db_config.clent()
        cur = conn.cursor()
        cur.execute(f"select * from category where category_id = {id}")
        registro = cur.fetchone()
        if registro:
            return registro
        else:
            return {"mensaje": "Registro no encontrado"}
    except Exception as e:
        return {"error": str(e)}
    finally:
        conn.close()

# def actualizar_registro(id, prod):
#     try:
#         conn = db_config.clent()
#         cur = conn.cursor()
#         sql = f"""
#                 UPDATE public.product
#                 SET name = '{prod.name}',
#                     description = '{prod.description}',
#                     company = '{prod.company}',
#                     price = {prod.price},
#                     units = {prod.units},
#                     subcategory_id = {prod.subcategory_id},
#                     updated_at = CURRENT_TIMESTAMP
#                 WHERE product_id = {prod.product_id};
#                 """
#         cur.execute(sql)
#         conn.commit()
#         return {"mensaje": "Registro actualizado exitosamente"}
#     except Exception as e:
#         return {"error": str(e)}
#     finally:
#         conn.close()

# def eliminar_registro(id):
#     try:
#         conn = db_config.clent()
#         cur = conn.cursor()
#         cur.execute(f"DELETE from product where product_id = {id}")
#         conn.commit()
#         return {"mensaje": "Registro eliminado exitosamente"}
#     except Exception as e:
#         return {"error": str(e)}
#     finally:
#         conn.close()


