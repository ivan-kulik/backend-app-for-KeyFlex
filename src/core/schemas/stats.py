from pydantic import BaseModel


class AddStatisticsData(BaseModel):
    symbols_per_minute: int
    accuracy_percentage: int
    mode_type: str
