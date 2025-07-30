from pydantic import BaseModel


class SpeechPosition(BaseModel):
    start_s: float
    end_s: float

    def __str__(self):
        return f"SpeechPosition(start={self.start_s}, end={self.end_s})"

    def __repr__(self):
        return f"SpeechPosition(start={self.start_s}, end={self.end_s})"
