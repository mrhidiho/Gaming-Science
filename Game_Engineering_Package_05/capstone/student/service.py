"""Student capstone: design first, implement independently, retain evidence."""
class StudentService:
    def submit(self, payload: bytes):
        raise NotImplementedError("validate, admit within bound, execute, persist, report")

    def shutdown(self, cancel: bool = False):
        raise NotImplementedError("stop admission; drain/cancel; wake; join; preserve committed results")
