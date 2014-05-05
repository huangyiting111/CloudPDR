# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: CloudPdrMessages.proto

from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import descriptor_pb2
# @@protoc_insertion_point(imports)




DESCRIPTOR = _descriptor.FileDescriptor(
  name='CloudPdrMessages.proto',
  package='',
  serialized_pb='\n\x16\x43loudPdrMessages.proto\"!\n\tPublicKey\x12\t\n\x01n\x18\x01 \x02(\t\x12\t\n\x01g\x18\x02 \x02(\t\"$\n\x05\x42lock\x12\r\n\x05index\x18\x01 \x02(\t\x12\x0c\n\x04\x64\x61ta\x18\x02 \x02(\x0c\"?\n\x0f\x42lockCollection\x12\x14\n\x0c\x62lockBitSize\x18\x01 \x02(\x05\x12\x16\n\x06\x62locks\x18\x02 \x03(\x0b\x32\x06.Block\"\x1d\n\rTagCollection\x12\x0c\n\x04tags\x18\x01 \x03(\t\"r\n\x04Init\x12\x16\n\x02pk\x18\x01 \x02(\x0b\x32\n.PublicKey\x12\x1c\n\x02\x62\x63\x18\x02 \x02(\x0b\x32\x10.BlockCollection\x12\x1a\n\x02tc\x18\x03 \x02(\x0b\x32\x0e.TagCollection\x12\r\n\x05\x64\x65lta\x18\x04 \x02(\x05\x12\t\n\x01k\x18\x05 \x02(\x05\"\x16\n\x07InitAck\x12\x0b\n\x03\x61\x63k\x18\x01 \x02(\x08\"\x1e\n\tChallenge\x12\x11\n\tchallenge\x18\x01 \x02(\t\"5\n\x04\x43\x65ll\x12\r\n\x05\x63ount\x18\x01 \x02(\x05\x12\x10\n\x08hashprod\x18\x02 \x02(\x05\x12\x0c\n\x04\x64\x61ta\x18\x03 \x02(\x0c\"\x19\n\x03Ibf\x12\x12\n\x03ibf\x18\x01 \x03(\x0b\x32\x05.Cell\"+\n\x13\x43ombinedLostTagPair\x12\t\n\x01k\x18\x01 \x02(\x05\x12\t\n\x01v\x18\x02 \x02(\t\"\x82\x01\n\x05Proof\x12\x13\n\x0b\x63ombinedSum\x18\x01 \x02(\t\x12\x13\n\x0b\x63ombinedTag\x18\x02 \x02(\t\x12\x19\n\x0bserverState\x18\x03 \x02(\x0b\x32\x04.Ibf\x12\x13\n\x0blostIndeces\x18\x04 \x03(\x05\x12\x1f\n\x01p\x18\x05 \x03(\x0b\x32\x14.CombinedLostTagPair\"\"\n\x04Lost\x12\t\n\x01L\x18\x01 \x03(\x05\x12\x0f\n\x07lossNum\x18\x02 \x01(\x05\"\x16\n\x07LostAck\x12\x0b\n\x03\x61\x63k\x18\x01 \x02(\x08\"\xa0\x02\n\x0b\x43loudPdrMsg\x12\"\n\x04type\x18\x01 \x02(\x0e\x32\x14.CloudPdrMsg.msgType\x12\x13\n\x04init\x18\x02 \x01(\x0b\x32\x05.Init\x12\x15\n\x03\x61\x63k\x18\x03 \x01(\x0b\x32\x08.InitAck\x12\x19\n\x05\x63hlng\x18\x04 \x01(\x0b\x32\n.Challenge\x12\x15\n\x05proof\x18\x05 \x01(\x0b\x32\x06.Proof\x12\x13\n\x04lost\x18\x06 \x01(\x0b\x32\x05.Lost\x12\x16\n\x04lack\x18\x07 \x01(\x0b\x32\x08.LostAck\x12\r\n\x05\x63ltId\x18\x08 \x01(\t\"S\n\x07msgType\x12\x08\n\x04INIT\x10\x00\x12\x0c\n\x08INIT_ACK\x10\x01\x12\r\n\tCHALLENGE\x10\x02\x12\t\n\x05PROOF\x10\x03\x12\x08\n\x04LOSS\x10\x04\x12\x0c\n\x08LOSS_ACK\x10\x05')



_CLOUDPDRMSG_MSGTYPE = _descriptor.EnumDescriptor(
  name='msgType',
  full_name='CloudPdrMsg.msgType',
  filename=None,
  file=DESCRIPTOR,
  values=[
    _descriptor.EnumValueDescriptor(
      name='INIT', index=0, number=0,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='INIT_ACK', index=1, number=1,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='CHALLENGE', index=2, number=2,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='PROOF', index=3, number=3,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='LOSS', index=4, number=4,
      options=None,
      type=None),
    _descriptor.EnumValueDescriptor(
      name='LOSS_ACK', index=5, number=5,
      options=None,
      type=None),
  ],
  containing_type=None,
  options=None,
  serialized_start=893,
  serialized_end=976,
)


_PUBLICKEY = _descriptor.Descriptor(
  name='PublicKey',
  full_name='PublicKey',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='n', full_name='PublicKey.n', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='g', full_name='PublicKey.g', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=26,
  serialized_end=59,
)


_BLOCK = _descriptor.Descriptor(
  name='Block',
  full_name='Block',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='index', full_name='Block.index', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='data', full_name='Block.data', index=1,
      number=2, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=61,
  serialized_end=97,
)


_BLOCKCOLLECTION = _descriptor.Descriptor(
  name='BlockCollection',
  full_name='BlockCollection',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='blockBitSize', full_name='BlockCollection.blockBitSize', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='blocks', full_name='BlockCollection.blocks', index=1,
      number=2, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=99,
  serialized_end=162,
)


_TAGCOLLECTION = _descriptor.Descriptor(
  name='TagCollection',
  full_name='TagCollection',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='tags', full_name='TagCollection.tags', index=0,
      number=1, type=9, cpp_type=9, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=164,
  serialized_end=193,
)


_INIT = _descriptor.Descriptor(
  name='Init',
  full_name='Init',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='pk', full_name='Init.pk', index=0,
      number=1, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='bc', full_name='Init.bc', index=1,
      number=2, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='tc', full_name='Init.tc', index=2,
      number=3, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='delta', full_name='Init.delta', index=3,
      number=4, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='k', full_name='Init.k', index=4,
      number=5, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=195,
  serialized_end=309,
)


_INITACK = _descriptor.Descriptor(
  name='InitAck',
  full_name='InitAck',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='ack', full_name='InitAck.ack', index=0,
      number=1, type=8, cpp_type=7, label=2,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=311,
  serialized_end=333,
)


_CHALLENGE = _descriptor.Descriptor(
  name='Challenge',
  full_name='Challenge',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='challenge', full_name='Challenge.challenge', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=335,
  serialized_end=365,
)


_CELL = _descriptor.Descriptor(
  name='Cell',
  full_name='Cell',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='count', full_name='Cell.count', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='hashprod', full_name='Cell.hashprod', index=1,
      number=2, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='data', full_name='Cell.data', index=2,
      number=3, type=12, cpp_type=9, label=2,
      has_default_value=False, default_value="",
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=367,
  serialized_end=420,
)


_IBF = _descriptor.Descriptor(
  name='Ibf',
  full_name='Ibf',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='ibf', full_name='Ibf.ibf', index=0,
      number=1, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=422,
  serialized_end=447,
)


_COMBINEDLOSTTAGPAIR = _descriptor.Descriptor(
  name='CombinedLostTagPair',
  full_name='CombinedLostTagPair',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='k', full_name='CombinedLostTagPair.k', index=0,
      number=1, type=5, cpp_type=1, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='v', full_name='CombinedLostTagPair.v', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=449,
  serialized_end=492,
)


_PROOF = _descriptor.Descriptor(
  name='Proof',
  full_name='Proof',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='combinedSum', full_name='Proof.combinedSum', index=0,
      number=1, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='combinedTag', full_name='Proof.combinedTag', index=1,
      number=2, type=9, cpp_type=9, label=2,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='serverState', full_name='Proof.serverState', index=2,
      number=3, type=11, cpp_type=10, label=2,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='lostIndeces', full_name='Proof.lostIndeces', index=3,
      number=4, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='p', full_name='Proof.p', index=4,
      number=5, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=495,
  serialized_end=625,
)


_LOST = _descriptor.Descriptor(
  name='Lost',
  full_name='Lost',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='L', full_name='Lost.L', index=0,
      number=1, type=5, cpp_type=1, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='lossNum', full_name='Lost.lossNum', index=1,
      number=2, type=5, cpp_type=1, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=627,
  serialized_end=661,
)


_LOSTACK = _descriptor.Descriptor(
  name='LostAck',
  full_name='LostAck',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='ack', full_name='LostAck.ack', index=0,
      number=1, type=8, cpp_type=7, label=2,
      has_default_value=False, default_value=False,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=663,
  serialized_end=685,
)


_CLOUDPDRMSG = _descriptor.Descriptor(
  name='CloudPdrMsg',
  full_name='CloudPdrMsg',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='type', full_name='CloudPdrMsg.type', index=0,
      number=1, type=14, cpp_type=8, label=2,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='init', full_name='CloudPdrMsg.init', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='ack', full_name='CloudPdrMsg.ack', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='chlng', full_name='CloudPdrMsg.chlng', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='proof', full_name='CloudPdrMsg.proof', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='lost', full_name='CloudPdrMsg.lost', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='lack', full_name='CloudPdrMsg.lack', index=6,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
    _descriptor.FieldDescriptor(
      name='cltId', full_name='CloudPdrMsg.cltId', index=7,
      number=8, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=unicode("", "utf-8"),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      options=None),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
    _CLOUDPDRMSG_MSGTYPE,
  ],
  options=None,
  is_extendable=False,
  extension_ranges=[],
  serialized_start=688,
  serialized_end=976,
)

_BLOCKCOLLECTION.fields_by_name['blocks'].message_type = _BLOCK
_INIT.fields_by_name['pk'].message_type = _PUBLICKEY
_INIT.fields_by_name['bc'].message_type = _BLOCKCOLLECTION
_INIT.fields_by_name['tc'].message_type = _TAGCOLLECTION
_IBF.fields_by_name['ibf'].message_type = _CELL
_PROOF.fields_by_name['serverState'].message_type = _IBF
_PROOF.fields_by_name['p'].message_type = _COMBINEDLOSTTAGPAIR
_CLOUDPDRMSG.fields_by_name['type'].enum_type = _CLOUDPDRMSG_MSGTYPE
_CLOUDPDRMSG.fields_by_name['init'].message_type = _INIT
_CLOUDPDRMSG.fields_by_name['ack'].message_type = _INITACK
_CLOUDPDRMSG.fields_by_name['chlng'].message_type = _CHALLENGE
_CLOUDPDRMSG.fields_by_name['proof'].message_type = _PROOF
_CLOUDPDRMSG.fields_by_name['lost'].message_type = _LOST
_CLOUDPDRMSG.fields_by_name['lack'].message_type = _LOSTACK
_CLOUDPDRMSG_MSGTYPE.containing_type = _CLOUDPDRMSG;
DESCRIPTOR.message_types_by_name['PublicKey'] = _PUBLICKEY
DESCRIPTOR.message_types_by_name['Block'] = _BLOCK
DESCRIPTOR.message_types_by_name['BlockCollection'] = _BLOCKCOLLECTION
DESCRIPTOR.message_types_by_name['TagCollection'] = _TAGCOLLECTION
DESCRIPTOR.message_types_by_name['Init'] = _INIT
DESCRIPTOR.message_types_by_name['InitAck'] = _INITACK
DESCRIPTOR.message_types_by_name['Challenge'] = _CHALLENGE
DESCRIPTOR.message_types_by_name['Cell'] = _CELL
DESCRIPTOR.message_types_by_name['Ibf'] = _IBF
DESCRIPTOR.message_types_by_name['CombinedLostTagPair'] = _COMBINEDLOSTTAGPAIR
DESCRIPTOR.message_types_by_name['Proof'] = _PROOF
DESCRIPTOR.message_types_by_name['Lost'] = _LOST
DESCRIPTOR.message_types_by_name['LostAck'] = _LOSTACK
DESCRIPTOR.message_types_by_name['CloudPdrMsg'] = _CLOUDPDRMSG

class PublicKey(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _PUBLICKEY

  # @@protoc_insertion_point(class_scope:PublicKey)

class Block(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _BLOCK

  # @@protoc_insertion_point(class_scope:Block)

class BlockCollection(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _BLOCKCOLLECTION

  # @@protoc_insertion_point(class_scope:BlockCollection)

class TagCollection(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _TAGCOLLECTION

  # @@protoc_insertion_point(class_scope:TagCollection)

class Init(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _INIT

  # @@protoc_insertion_point(class_scope:Init)

class InitAck(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _INITACK

  # @@protoc_insertion_point(class_scope:InitAck)

class Challenge(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _CHALLENGE

  # @@protoc_insertion_point(class_scope:Challenge)

class Cell(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _CELL

  # @@protoc_insertion_point(class_scope:Cell)

class Ibf(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _IBF

  # @@protoc_insertion_point(class_scope:Ibf)

class CombinedLostTagPair(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _COMBINEDLOSTTAGPAIR

  # @@protoc_insertion_point(class_scope:CombinedLostTagPair)

class Proof(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _PROOF

  # @@protoc_insertion_point(class_scope:Proof)

class Lost(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _LOST

  # @@protoc_insertion_point(class_scope:Lost)

class LostAck(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _LOSTACK

  # @@protoc_insertion_point(class_scope:LostAck)

class CloudPdrMsg(_message.Message):
  __metaclass__ = _reflection.GeneratedProtocolMessageType
  DESCRIPTOR = _CLOUDPDRMSG

  # @@protoc_insertion_point(class_scope:CloudPdrMsg)


# @@protoc_insertion_point(module_scope)
