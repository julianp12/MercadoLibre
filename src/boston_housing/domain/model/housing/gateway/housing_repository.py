from abc import ABC, abstractmethod
from typing import List
from boston_housing.domain.model.housing.housing import Housing

class HousingRepository(ABC):
    """Gateway/Repositorio abstracto para acceso a datos de viviendas."""
    
    @abstractmethod
    def load(self) -> List[Housing]:
        """Carga todos los registros de vivienda."""
        pass

    @abstractmethod
    def load_as_dataframe(self):
        """Carga registros como DataFrame."""
        pass
