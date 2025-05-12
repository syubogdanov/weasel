from pydantic import BaseModel, NonNegativeFloat, NonNegativeInt


class RetriesSettings(BaseModel):
    """The retries settings."""

    # The number of attempts.
    attemps: NonNegativeInt = 3
    # The delay between attempts (seconds).
    delay: NonNegativeFloat = 2.5
