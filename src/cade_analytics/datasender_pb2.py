# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: datasender.proto
# Protobuf Python Version: 5.26.1
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x10\x64\x61tasender.proto\x12\ndataSender\"\x18\n\x08SendData\x12\x0c\n\x04\x64\x61ta\x18\x01 \x01(\t\"\x1c\n\x0b\x43onfirmData\x12\r\n\x05\x63heck\x18\x01 \x01(\x08\x32\x45\n\nDataSender\x12\x37\n\x06Sender\x12\x14.dataSender.SendData\x1a\x17.dataSender.ConfirmDatab\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'datasender_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_SENDDATA']._serialized_start=32
  _globals['_SENDDATA']._serialized_end=56
  _globals['_CONFIRMDATA']._serialized_start=58
  _globals['_CONFIRMDATA']._serialized_end=86
  _globals['_DATASENDER']._serialized_start=88
  _globals['_DATASENDER']._serialized_end=157
# @@protoc_insertion_point(module_scope)
