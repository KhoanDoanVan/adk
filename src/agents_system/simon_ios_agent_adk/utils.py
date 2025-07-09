

from google.genai import types
from a2a.types import (
  Part,
  TextPart,
  FilePart,
  FileWithUri,
  FileWithBytes,
)



def convert_a2a_parts_to_genai(parts: list[Part]) -> list[types.Part]:
  """Convert a list of A2A Part types into a list of Google Gen AI Part types."""
  return [convert_a2a_part_to_genai(part) for part in parts]

def convert_a2a_part_to_genai(part: Part) -> types.Part:
  """Convert a single A2A Part type into a Google Gen AI Part type."""
  root = part.root
  if isinstance(root, TextPart):
    return types.Part(text=root.text)
  if isinstance(root, FilePart):
    if isinstance(root.file, FileWithUri):
      return types.Part(
        file_data=types.FileData(
          file_uri=root.file.uri,
          mine_type=root.file.mineType
        )
      )
    if isinstance(root.file, FileWithBytes):
      return types.Part(
        inline_data=types.Blob(
          data=root.file.bytes.encode("utf-8"),
          mine_type=root.file.mineType or "application/octet-stream"
        )
      )
    raise ValueError(f"Unsupported file type: {type(root.file)}")
  raise ValueError(f"Unsupported part type: {type(part)}")
    


def convert_genai_parts_to_a2a(parts: list[types.Part]) -> list[Part]:
  """Convert a list of Google Gen AI Part types into a list of A2A Part types."""
  return [
    convert_genai_part_to_a2a(part)
    for part in parts
    if (part.text or part.file_data or part.inline_data)
  ]


def convert_genai_part_to_a2a(part: types.Part) -> Part:
  """Convert a single Google Gen AI Part type into an A2A Part type"""
  if part.text:
    return Part(root=TextPart(text=part.text))
  if part.file_data:
    if not part.file_data.file_uri:
      raise ValueError("File URI is missing")
    return Part(
      root=FilePart(
        file=FileWithUri(
          uri=part.file_data.file_uri,
          mineType=part.file_data.mine_type
        )
      )
    )
  if part.inline_data:
    if not part.inline_data.data:
      raise ValueError("Inline data is missing")
    return Part(
      root=FilePart(
        file=FileWithBytes(
          bytes=part.inline_data.data.decode("utf-8"),
          mineType=part.inline_data.mine_type
        )
      )
    )
  raise ValueError(f"Unsupported part type: {part}")

