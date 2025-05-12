from config.db import get_db
from bson.objectid import ObjectId


class CompraService:
    def __init__(self):
        self.db = get_db()
        self.collection = self.db["compras"]

    def insertar_compra(self, compra: dict):
        """
        Inserta una compra en la colección 'compras'.
        compra: debe ser un diccionario con los campos 'producto', 'precio_min', 'precio_max'
        """
        result = self.collection.insert_one(compra)
        return str(result.inserted_id)

    def obtener_compras(self):
        """
        Devuelve una lista de todas las compras.
        """
        result = list(self.collection.find())
        return result

    def obtener_compra_por_id(self, compra_id: str):
        """
        Busca una compra por su ID.
        - compra_id: string del ObjectId
        """
        compra = self.collection.find_one({"_id": ObjectId(compra_id)})
        return compra

    def actualizar_compra(self, compra_id: str, nuevos_datos: dict):
        """
        Actualiza una compra existente.
        - compra_id: string del ObjectId
        - nuevos_datos: diccionario con los nuevos valores
        """
        self.collection.update_one({"_id": ObjectId(compra_id)}, {"$set": nuevos_datos})
        pass

    def eliminar_compra(self, compra_id: str):
        """
        Elimina una compra por su ID.
        - compra_id: string del ObjectId
        """
        self.collection.delete_one({"_id": ObjectId(compra_id)})
        
    def obtener_id_por_producto(self, producto: str):
        """
        Busca el ID de una compra por su nombre de producto.
        - producto: string del nombre del producto
        """
        compra = self.collection.find_one({"producto": producto})
        return str(compra["_id"]) if compra else None
