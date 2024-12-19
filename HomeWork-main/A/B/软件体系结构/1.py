import base64
import json
import yaml
import struct
from xml.etree import ElementTree
import msgpack
from google.protobuf.internal.decoder import _DecodeVarint32  # Protocol Buffers

# 解码base64数据
data = """
    ACLCAAAAAAAbgPJnbwMAAAAAAAAknon/iO4OjSQOEiszQ3RaACLCAAAAAAAbgPJncAMAAAAAAABH
    DcqfGZsqAit0s6vYOVgoACLCAAAAAAAbgPJncQMAAAAAAAAxX8onRDKkcIKVb0ADdhqgACLCAAAA
    AAAbgPJncgMAAAAAAABceddtb3GwIVrNDEVuSNsPACLCAAAAAAAbgPJncwMAAAAAAAB05f2kt7Gg
    kHxhm/pY2Nw0ACLCAAAAAAAbgPJndAMAAAAAAAC34JmXWmKFSm6to5DmRgt/ACLCAAAAAAAbgPJn
    dQMAAAAAAAAIuG+bdepyM9GPsmys4WZaACLCAAAAAAAbgPJndgMAAAAAAABy96sXUlN3vSFCJR7M
    6QdaACLCAAAAAAAbgPJndwMAAAAAAABxWijLCw9I0pBHvHPqlzQhACLCAAAAAAAbgPJneAMAAAAA
    AADQKG59oYuRl2UA6aOM0HIMACLCAAAAAAAbgPJneQMAAAAAAABswWC8VUWFAlJqMC1Ohq9iACLC
    AAAAAAAbgPJnegMAAAAAAACRAg5hieUpDBH4+yEke1D0ACLCAAAAAAAbgPJnewMAAAAAAAD8c+5r
    rdHkRP817VAU50B1ACLCAAAAAAAbgPJnfAMAAAAAAACbDgx66ZI3Vb3tYF1GubxjACLCAAAAAAAb
    gPJnfQMAAAAAAACS+gn+Jih9G9trwSJrqd3fACLCAAAAAAAbgPJnfgMAAAAAAABMqEraqnxt2fHQ
    e9S5XCmyACLCAAAAAAAbgPJnfwMAAAAAAACz9Yqjit0J7fVtp30uqZshACLCAAAAAAAbgPJngAMA
    AAAAAAA9BSqEPpP1aYGb4iVlRnW6ACLCAAAAAAAbgPJngQMAAAAAAAD64mXReBSd4I7rMr9GNgOr
    ACLCAAAAAAAbgPJnggMAAAAAAADbd9S9nPpEDSc5pVn2TbB3ACLCAAAAAAAbgPJngwMAAAAAAACz
    FUmyuAqWoF5keldtbzB+ACLCAAAAAAAbgPJnhAMAAAAAAACZfiRuPVi5ehRt8QwMklN9ACLCAAAA
    AAAbgPJnhQMAAAAAAABcyjF9Lcluyt9HQqZKY8esACLCAAAAAAAbgPJnhgMAAAAAAABr9X+s3huL
    PWA36zGcW/N4ACLCAAAAAAAbgPJnhwMAAAAAAADjxtlt+4AjXnSAZ82JsDwRACLCAAAAAAAbgPJn
    iAMAAAAAAAB+pt1qAeVXrQpoS1W/Nn/9ACLCAAAAAAAbgPJniQMAAAAAAAD5M5Nt1G1TxP0rG+1k
    F2OvACLCAAAAAAAbgPJnigMAAAAAAABy36NPfx5p/x0ykoek7jIhACLCAAAAAAAbgPJniwMAAAAA
    AACZkysxFKX/8cGocQm1+GuBACLCAAAAAAAbgPJnjAMAAAAAAABuly9XFb2E4EbtQTo0xJM+ACLC
    AAAAAAAbgPJnjQMAAAAAAAAcAqvnpHFQ8gdxIbfLAKUbACLCAAAAAAAbgPJnjgMAAAAAAAAe0Pge
    kDpQYIkbXg1o5go7ACLCAAAAAAAbgPJnjwMAAAAAAABGNwCBlt3W1TFaZD71S78cACLCAAAAAAAb
    gPJnkAMAAAAAAAC7vqk4HlQsBT9gUhiR4GZJACLCAAAAAAAbgPJnkQMAAAAAAADnb6bFyGInn2gI
    d598m5/UACLCAAAAAAAbgPJnkgMAAAAAAABukFEv6GvfGuZa4HIuP9CmACLCAAAAAAAbgPJnkwMA
    AAAAAAB5CGgNA57sN2d+nEewnITWACLCAAAAAAAbgPJnlAMAAAAAAADuNUdFqKfutQ==
"""

decoded_data = base64.b64decode(data)

# 1. 尝试解码为UTF-8字符串
try:
    utf8_str = decoded_data.decode('utf-8')
    print("这是一个UTF-8字符串：")
    print(utf8_str[:200])  # 打印前200个字符
except UnicodeDecodeError:
    print("无法解析为UTF-8字符串")

# 2. 尝试解析为JSON
try:
    json_data = json.loads(decoded_data)
    print("这是一个有效的JSON数据：")
    print(json_data)
except (UnicodeDecodeError, json.JSONDecodeError):
    print("无法解析为JSON数据")

# 3. 尝试解析为YAML
try:
    yaml_data = yaml.safe_load(decoded_data)
    print("这是一个有效的YAML数据：")
    print(yaml_data)
except yaml.YAMLError:
    print("无法解析为YAML数据")

# 4. 尝试解析为XML
try:
    xml_data = ElementTree.fromstring(decoded_data)
    print("这是一个有效的XML数据：")
    print(ElementTree.tostring(xml_data, encoding='unicode'))
except ElementTree.ParseError:
    print("无法解析为XML数据")

# 5. 尝试解析为Protocol Buffers
try:
    # 使用protobuf的解码方法解析前两个字节
    offset = 0
    msg_length, offset = _DecodeVarint32(decoded_data, offset)
    protobuf_data = decoded_data[offset:offset + msg_length]
    print("这是一个Protocol Buffers数据：")
    print(protobuf_data)
except Exception as e:
    print("无法解析为Protocol Buffers数据:", e)

# 6. 尝试解析为MessagePack
try:
    msgpack_data = msgpack.unpackb(decoded_data)
    print("这是一个有效的MessagePack数据：")
    print(msgpack_data)
except msgpack.exceptions.ExtraData:
    print("无法解析为MessagePack数据")

# 7. 尝试解析为Avro（假设你有对应的schema）
# 如果你有Avro schema，你可以使用 Avro 的 python 库进行解析
try:
    import fastavro
    from io import BytesIO
    reader = fastavro.reader(BytesIO(decoded_data))
    avro_data = [record for record in reader]
    print("这是一个有效的Avro数据：")
    print(avro_data)
except ImportError:
    print("Avro库未安装")
except Exception as e:
    print(f"无法解析为Avro数据: {e}")

# 8. 尝试其他结构
try:
    unpacked_data = struct.unpack('!20s', decoded_data[:20])
    print("解包后的数据：")
    print(unpacked_data)
except Exception as e:
    print(f"无法使用struct解析数据: {e}")
