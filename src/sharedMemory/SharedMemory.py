import mmap
import time
import struct
from enum import Enum
from typing import NamedTuple

SHARED_MEM_NAME = "VolleyballLegendsProSharedMemory"

class ShmVariable(Enum):
   isInServeLoop = ("isInServeLoop", bool)
   isServing = ("isServing", bool)
   isServe = ("isServe", bool)
   isToss = ("isToss", bool)
   serveCommand = ("serveCommand", bool)
   serveMode = ("serveMode", int)

   def __init__(self, name: str, typ: type):
      self.field_name = name
      self.field_type = typ

type_to_format = {
   bool: "i",  # 4 bytes
   int: "i",   # 4 bytes
}

shared_data_fields = [(f.field_name, f.field_type) for f in ShmVariable]
SharedData = NamedTuple("SharedData", shared_data_fields)

fields = []
for field in ShmVariable:
   name = field.field_name
   typ = field.field_type
   if typ not in type_to_format:
      raise TypeError(f"Unsupported type {typ} for field {name}")
   fields.append((name, type_to_format[typ]))

format_string = "".join(fmt for _, fmt in fields)
total_size = struct.calcsize(format_string)

def try_open_shared_memory(retries=5, delay=1):
   for attempt in range(retries):
      try:
         shm_mmap = mmap.mmap(0, total_size, SHARED_MEM_NAME)
         print("Successfully opened shared memory!")
         return shm_mmap
      except (PermissionError, FileNotFoundError):
         print(f"Attempt {attempt + 1}: Waiting for shared memory...")
         time.sleep(delay)
   raise RuntimeError("Could not access shared memory. Ensure the C++ program is running.")

class SharedMemoryManager:
   def __init__(self, _shm, fields):
      self.shm = _shm
      self.fields = fields
      self.format_string = "".join(fmt for _, fmt in fields)
      self.total_size = struct.calcsize(self.format_string)
      if len(self.shm) < self.total_size:
         raise ValueError(
               f"Shared memory size ({len(self.shm)}) too small for layout ({self.total_size})"
         )
      self.offsets = {}
      offset = 0
      for name, fmt in fields:
         self.offsets[name] = offset
         offset += struct.calcsize(fmt)

   def get(self, field: ShmVariable):
      """Read a specific field using Field enum."""
      name = field.field_name
      fmt = next(fmt for n, fmt in self.fields if n == name)
      offset = self.offsets[name]
      value = struct.unpack_from(fmt, self.shm, offset)[0]
      return bool(value) if field.field_type == bool else value

   def set(self, field: ShmVariable, value):
      """Write a specific field using Field enum."""
      name = field.field_name
      fmt = next(fmt for n, fmt in self.fields if n == name)
      offset = self.offsets[name]
      if field.field_type == bool:
         value = int(bool(value))
      elif field.field_type == int:
         value = int(value)
      struct.pack_into(fmt, self.shm, offset, value)

   def read(self):
      """Read all fields into a SharedData object."""
      data = struct.unpack(self.format_string, self.shm[:self.total_size])
      converted_data = [
         bool(val) if field.field_type == bool else val
         for val, field in zip(data, ShmVariable)
      ]
      return SharedData(*converted_data)

   def write(self, shared_data):
      """Write all fields from a SharedData object."""
      packed_data = [
         int(val) if field.field_type == bool else val
         for val, field in zip(shared_data, ShmVariable)
      ]
      packed = struct.pack(self.format_string, *packed_data)
      self.shm[:self.total_size] = packed
      
   def close(self):
      """Close the shared memory."""
      self.shm.close()

try:
   shm = SharedMemoryManager(try_open_shared_memory(), fields)
   shm.set(ShmVariable.isInServeLoop, False)
   shm.set(ShmVariable.isServing, False)
   shm.set(ShmVariable.isServe, False)
   shm.set(ShmVariable.isToss, False)
   shm.set(ShmVariable.serveCommand, False)
   shm.set(ShmVariable.serveMode, 1)
except (RuntimeError, ValueError) as e:
   print(f"Error: {e}")
   exit(1)
