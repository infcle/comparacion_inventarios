from datetime import date, datetime

class ItemMovimiento:
    def __init__(
        self, 
        descripcion, 
        cantidad, 
        unidad, 
        costo_unitario, 
        importe, 
        fecha, 
        codigo,
        movimiento,
        operacion
    ):
        # Movimientos
        self.cantidad = cantidad
        self.unidad = unidad
        self.costo_unitario = costo_unitario
        self.importe = importe
        self.fecha = fecha
        self.operacion = operacion
        self.movimiento = movimiento
        # datos item
        self.codigo = codigo
        self.descripcion = descripcion 

    def __str__(self):
        """ Retorna una cadena legible """
        return(
            f"Descripcion: '{self.descripcion}', "
            f"Cantidad: '{self.cantidad}', "
            f"Unidad: '{self.unidad}', "
            f"Costo Unitario: '{self.costo_unitario}', "
            f"Importe: '{self.importe}', "
            f"Fecha: '{self.fecha}', "
        )

    def getDescripcion(self):
        return self.descripcion

    def getCantidad(self):
        return self.cantidad

    def getFechaCorta(self):
        if isinstance(self.fecha, (datetime, date)):
            return self.fecha.strftime("%d/%m/%Y")    
        elif isinstance(self.fecha, str):
            return self.fecha.strip()        
        else:
            return str(self.fecha)

    def getImporteDosCifras(self):
        return round(self.importe, 2)

    def getCostoUnitarioDosCifras(self):
        return round(self.costo_unitario, 2)
    