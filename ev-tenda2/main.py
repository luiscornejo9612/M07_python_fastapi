from fastapi import FastAPI, File, UploadFile
from model import Product 
from db import productDB as pb
from producte import *


app = FastAPI()


@app.get("/product/")
def getAllproduct():
    return pb.getAll()


@app.get("/product/{id}")
def getproductByid(id:int):
    return pb.getbyID(id)


@app.post("/product/")
def createProduct(prod: Product.Product):
    return pb.create_product(prod)


@app.put("/product/")
def modificar(prod: Product.Product):
    return pb.update_product(prod)


@app.delete("/product/{id}")
def deleteproduct(id:int):
    return pb.delete_product(id)


# *********************************************************************************************************************
#CargaMasiva de Productos
@app.post("/loadProducts/")
async def insertItemsCSVToDB():
    try:
        pb.insertCategory()
        pb.insertSubCategory()
        pb.insertProducts()
        data = {"status":1,"message":"Inserción masiva realizada con éxito"}
    except Exception as e: 
        data = {"status":-1,"error":f'{e}', "message":"Los datos ya existían en la BD"}
    finally:
        return data
    





