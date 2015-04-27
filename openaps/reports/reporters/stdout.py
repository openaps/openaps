import sys
def get_output_stream (reporter):
  return sys.stdout

def serialize (blob, reporter):
  return str(blob)
