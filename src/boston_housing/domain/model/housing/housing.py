from dataclasses import dataclass
from typing import Optional

@dataclass
class Housing:
    """Entidad de dominio: registro de vivienda."""
    crim: float
    zn: float
    indus: float
    chas: float
    nox: float
    rm: float
    age: float
    dis: float
    rad: float
    tax: float
    ptratio: float
    b: float              # Índice de proporción de población
    lstat: float
    price: Optional[float] = None
