"""Clases de condición de soldadura (protocolo, sección 6.2)."""

ACEPTABLE = "aceptable"

CLASES: tuple[str, ...] = (
    ACEPTABLE,
    "insuficiente",
    "puente",
    "sin_soldar",
    "exceso",
    "fria",
)

NOMBRES: dict[str, str] = {
    "aceptable": "Unión aceptable",
    "insuficiente": "Soldadura insuficiente",
    "puente": "Puente entre pines",
    "sin_soldar": "Pin sin soldar u omitido",
    "exceso": "Exceso de soldadura",
    "fria": "Unión fría o deslustrada",
}


def es_defecto(clase: str) -> bool:
    """Toda clase distinta de 'aceptable' cuenta como defecto en las metas M1 y M2."""
    validar(clase)
    return clase != ACEPTABLE


def validar(clase: str) -> str:
    if clase not in CLASES:
        raise ValueError(f"Clase desconocida: {clase!r}. Válidas: {', '.join(CLASES)}")
    return clase
