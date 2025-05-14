from pydantic import BaseModel, ConfigDict, NonNegativeFloat, NonNegativeInt


class MetricsEntity(BaseModel):
    """The metrics entity."""

    nolie: NonNegativeFloat
    mean: NonNegativeFloat
    median: NonNegativeFloat
    min: NonNegativeFloat
    max: NonNegativeFloat
    var: NonNegativeFloat
    std: NonNegativeFloat
    p75: NonNegativeFloat
    p90: NonNegativeFloat
    p95: NonNegativeFloat
    p99: NonNegativeFloat
    count: NonNegativeInt

    model_config = ConfigDict(from_attributes=True)
