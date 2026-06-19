from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List
import re

app = FastAPI(
    title="Donatón Match Service",
    description="Microservicio de IA y emparejamiento logístico para el proyecto humanitario DONATON.",
    version="1.0.0"
)

# ==========================================
# 1. ESQUEMAS DE DATOS (Pydantic Models)
# ==========================================

class Necesidad(BaseModel):
    id: int = Field(..., description="ID único de la necesidad")
    comuna: str = Field(..., description="Comuna donde se requiere la ayuda")
    tipoItem: str = Field(..., description="Tipo de ítem solicitado (ej: Agua, Frazadas)")
    cantidad: int = Field(..., gt=0, description="Cantidad solicitada")
    urgencia: str = Field(..., description="Nivel de urgencia: ALTA, MEDIA, BAJA")
    nombreOriginal: str = Field(default="", description="Nombre real del ítem")

class Stock(BaseModel):
    id: int = Field(..., description="ID único del registro de stock")
    comuna: str = Field(..., description="Comuna donde se encuentra el centro de acopio")
    tipoItem: str = Field(..., description="Tipo de ítem disponible")
    cantidadDisponible: int = Field(..., ge=0, description="Cantidad disponible en stock")
    estado: str = Field(..., description="Estado del stock, ej: DISPONIBLE")
    nombreOriginal: str = Field(default="", description="Nombre real del ítem")

class MatchRequest(BaseModel):
    necesidades: List[Necesidad] = Field(..., description="Lista de necesidades recopiladas")
    stocks: List[Stock] = Field(..., description="Lista de stocks disponibles")

class PropuestaMatch(BaseModel):
    necesidad_id: int
    stock_id: int
    comuna_destino: str
    tipoItem: str
    cantidad_asignada: int
    estado_match: str
    justificacion: str

class MatchResponse(BaseModel):
    propuestas_match: List[PropuestaMatch]


# ==========================================
# 2. CONFIGURACIÓN Y CONSTANTES
# ==========================================

# Ponderación para ordenar las prioridades (menor número = mayor prioridad)
URGENCIA_PESOS = {
    "ALTA": 1,
    "MEDIA": 2,
    "BAJA": 3
}

def extraer_palabras_clave(texto: str) -> set:
    if not texto: return set()
    texto = texto.lower()
    texto = re.sub(r'[^\w\s]', '', texto)
    palabras = texto.split()
    stop_words = {'de', 'para', 'en', 'el', 'la', 'los', 'las', 'un', 'una', 'unos', 'unas', 'y', 'o', 'kit', 'con', 'del', 'al'}
    return set([p for p in palabras if p not in stop_words and len(p) > 2])

def son_compatibles(nec: Necesidad, st: Stock) -> bool:
    # Deben ser de la misma categoría general
    if nec.tipoItem.strip().lower() != st.tipoItem.strip().lower():
        return False
        
    nec_kw = extraer_palabras_clave(nec.nombreOriginal)
    st_kw = extraer_palabras_clave(st.nombreOriginal)
    
    # Si alguno no tiene palabras clave válidas, hacemos fallback a la categoría
    if not nec_kw or not st_kw:
        return True
        
    # Match semántico básico: intersección de palabras clave
    return len(nec_kw & st_kw) > 0

# ==========================================
# 3. ENDPOINTS
# ==========================================

@app.post("/api/match/procesar", response_model=MatchResponse)
def procesar_match(request: MatchRequest):
    """
    Procesa las listas de necesidades y stocks para generar un plan de distribución logística.
    Prioriza:
    1. Urgencia (ALTA antes que MEDIA o BAJA).
    2. Cercanía geográfica (comuna origen == comuna destino).
    """
    
    # Validaciones iniciales
    if not request.necesidades:
        raise HTTPException(status_code=400, detail="La lista de necesidades está vacía.")
    if not request.stocks:
        raise HTTPException(status_code=400, detail="La lista de stocks está vacía.")

    # Clonar los stocks para poder descontar las cantidades sin afectar el objeto original de la request
    stocks_disponibles = [
        stock.model_copy() for stock in request.stocks 
        if stock.estado.upper() == "DISPONIBLE" and stock.cantidadDisponible > 0
    ]
    
    # Ordenar necesidades por urgencia (Prioridad 2: ALTA > MEDIA > BAJA)
    necesidades_ordenadas = sorted(
        request.necesidades, 
        key=lambda n: URGENCIA_PESOS.get(n.urgencia.upper(), 4) # 4 por defecto si el nivel es desconocido
    )

    propuestas = []

    # Procesar cada necesidad de acuerdo a su prioridad
    for necesidad in necesidades_ordenadas:
        cantidad_restante = necesidad.cantidad
        
        # Filtrar stocks que sean compatibles algorítmicamente y tengan disponibilidad
        stocks_compatibles = [
            s for s in stocks_disponibles 
            if son_compatibles(necesidad, s) and s.cantidadDisponible > 0
        ]
        
        # Ordenar stocks compatibles: primero los de la misma comuna (Prioridad 1: Cercanía Geográfica)
        stocks_compatibles = sorted(
            stocks_compatibles,
            key=lambda s: 0 if s.comuna.strip().lower() == necesidad.comuna.strip().lower() else 1
        )

        for stock in stocks_compatibles:
            if cantidad_restante <= 0:
                break # Necesidad cubierta totalmente
            
            # Determinar cuánto podemos asignar desde este stock
            asignacion = min(cantidad_restante, stock.cantidadDisponible)
            
            # Rebajar cantidades para futuras iteraciones
            stock.cantidadDisponible -= asignacion
            cantidad_restante -= asignacion
            
            # Determinar el estado de la cobertura
            estado_match = "TOTAL" if cantidad_restante == 0 else "PARCIAL"
            
            # Redactar justificación algorítmica para auditoría / trazabilidad
            misma_comuna = (stock.comuna.strip().lower() == necesidad.comuna.strip().lower())
            origen_str = f"coincidencia de comuna ({stock.comuna})" if misma_comuna else f"centro de acopio en {stock.comuna}"
            
            if estado_match == "TOTAL" and asignacion < necesidad.cantidad:
                justificacion = f"Remanente cubierto desde {origen_str} ante urgencia {necesidad.urgencia.upper()}."
            else:
                justificacion = f"Asignado por {origen_str} ante urgencia {necesidad.urgencia.upper()}."

            # Registrar la propuesta
            propuesta = PropuestaMatch(
                necesidad_id=necesidad.id,
                stock_id=stock.id,
                comuna_destino=necesidad.comuna,
                tipoItem=necesidad.tipoItem,
                cantidad_asignada=asignacion,
                estado_match=estado_match,
                justificacion=justificacion
            )
            propuestas.append(propuesta)

    return MatchResponse(propuestas_match=propuestas)

if __name__ == "__main__":
    import uvicorn
    # Inicia el servidor de desarrollo en el puerto 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
