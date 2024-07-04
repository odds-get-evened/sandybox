import zlib


def crc32(data: bytes):
    """
    a simple CRC32 hasher because fuckwads make things complicated!

    Parameters
    ----------
    data : bytes
        any given byte data

    Returns
    ----------
    bytes
        CRC32 hash in bytes
    """
    c = zlib.crc32(data)
    c = hex(c)
    c = c[2:]

    return c.encode("utf8")
