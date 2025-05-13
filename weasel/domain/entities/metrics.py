from pydantic import BaseModel, ConfigDict, PositiveFloat, PositiveInt


class MetricsEntity(BaseModel):
    """The metrics entity."""

    nolie: PositiveFloat
    mean: PositiveFloat
    gmean: PositiveFloat
    median: PositiveFloat
    min: PositiveFloat
    max: PositiveFloat
    var: PositiveFloat
    std: PositiveFloat
    p75: PositiveFloat
    p90: PositiveFloat
    p95: PositiveFloat
    p99: PositiveFloat
    count: PositiveInt

    model_config = ConfigDict(from_attributes=True)
