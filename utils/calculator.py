def get_average(precio_min: float, precio_max: float) -> float:
    """
    Calcula el precio promedio entre un precio mínimo y un precio máximo.
    :param precio_min: Precio mínimo
    :param precio_max: Precio máximo
    :return: Precio promedio
    """
    return (precio_min + precio_max) / 2

def get_total(productos: list) -> float:
    total = 0
    for producto in productos:
        total += get_average(producto["precio_min"], producto["precio_max"])
    return total if productos else 0

def get_total_min(productos: list)->float:
    
    total = 0
    
    for producto in productos:
        total += producto["precio_min"]
    
    return total if productos else 0

def get_total_max(productos: list)->float:
    total = 0
    
    for producto in productos:
        total += producto["precio_max"]
        
    return total if productos else 0