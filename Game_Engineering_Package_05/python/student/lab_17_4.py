"""Student exercise: deliberately unfinished. See LAB_WORKBOOK."""
class InjectedFailure(RuntimeError): pass

def validate_save(value):
    raise NotImplementedError("17.4: validate exact save schema")
def write_save(path, value, fail_at=None):
    raise NotImplementedError("17.4: private temporary file and replacement")
def read_save(path):
    raise NotImplementedError("17.4: bounded validated load")
