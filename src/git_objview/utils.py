def sha1_hexstr_to_bytes(hex_str: str) -> bytes:
    b = bytes.fromhex(hex_str)
    if len(b) != 20:
        raise ValueError(f"Length of hex bytes isn't 20 it is {len(b)} hex_str: '{hex_str}'")
    return b
