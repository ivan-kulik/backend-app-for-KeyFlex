from pydantic import BaseModel


class AddStatisticsData(BaseModel):
    symbols_per_minute: int
    accuracy_percentage: float
    mode_type: str
