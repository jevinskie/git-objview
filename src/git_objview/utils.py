def sha1_hexstr_to_bytes(hex_str: str) -> bytes:
    buf = bytes.fromhex(hex_str)
    if len(buf) != 20:
        raise ValueError(f"Length of hex bytes isn't 20 it is {len(buf)} hex_str: '{hex_str}'")
    return buf


def sha1_bytes_to_hexstr(buf: bytes) -> str:
    if len(buf) != 20:
        raise ValueError(f"Length of buffer isn't 20 it is {len(buf)} buf: '{buf.hex()}'")
    return buf.hex()
