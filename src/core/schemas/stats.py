from pydantic import BaseModel


class AddStatisticsData(BaseModel):
    symbols_per_minute: int
    accuracy_percentage: float
    mode_type: str


class SymbolsPerMinuteStats(BaseModel):
    standard_mode: list[int]
    extended_mode: list[int]
    text_mode: list[int]
    english_mode: list[int]
    extreme_mode: list[int]
    user_mode: list[int]


class AverageAccuracyStats(BaseModel):
    standard_mode: float
    extended_mode: float
    text_mode: float
    english_mode: float
    extreme_mode: float
    user_mode: float


class NumberTrainingSessionsStats(BaseModel):
    standard_mode: int
    extended_mode: int
    text_mode: int
    english_mode: int
    extreme_mode: int
    user_mode: int


class GetModesStatsData(BaseModel):
    symbols_per_minute_stats: SymbolsPerMinuteStats
    average_accuracy_stats: AverageAccuracyStats
    number_training_sessions_stats: NumberTrainingSessionsStats


class LastSessionsSymbolsPerMinuteStats(BaseModel):
    the_best_result: int
    the_worst_result: int
    average_result: float


class LastSessionsAccuracyStats(BaseModel):
    the_best_result: float
    the_worst_result: float
    average_result: float


class GetLastSessionsStatsData(BaseModel):
    symbols_per_minute_stats: LastSessionsSymbolsPerMinuteStats
    accuracy_stats: LastSessionsAccuracyStats
    the_most_popular_mode: str
    mode_with_the_highest_symbols_per_minute_result: str
    mode_with_the_highest_accuracy_result: str
