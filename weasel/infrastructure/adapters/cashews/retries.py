from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_fixed

from weasel.settings.retries import RetriesSettings


settings = RetriesSettings()

retry_cashews = retry(
    reraise=True,
    retry=retry_if_exception_type(OSError),
    stop=stop_after_attempt(settings.attemps),
    wait=wait_fixed(settings.delay),
)
