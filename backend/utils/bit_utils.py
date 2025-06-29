import logging
from utils.logger import setup_logger

logger = setup_logger(__name__)

def string_to_bits(s: str) -> list[int]:
    if not isinstance(s, str):
        logger.error("Input to string_to_bits is not a string.")
        raise TypeError("Expected string input")
    logger.debug(f"Converting string to bits: '{s}'")
    byte_data = s.encode('utf-8')
    bits = [int(bit) for byte in byte_data for bit in format(byte, '08b')]
    logger.debug(f"String converted to {len(bits)} bits.")
    return bits

def bits_to_string(bits: list[int]) -> str:
    if len(bits) % 8 != 0:
        logger.error("Bit length is not a multiple of 8.")
        raise ValueError("Bit length must be a multiple of 8 to convert to string.")
    logger.debug(f"Reconstructing string from bits. Bit length = {len(bits)}")
    bytes_list = [int("".join(str(bit) for bit in bits[i:i+8]), 2)
                  for i in range(0, len(bits), 8)]
    try:
        result = bytes(bytes_list).decode('utf-8')
    except UnicodeDecodeError as e:
        logger.error(f"Failed to decode bytes to string: {e}")
        raise ValueError("Invalid byte sequence; cannot decode.")
    logger.debug(f"Bits successfully converted to string: '{result}'")
    return result

def int_to_bits(n: int, length=16) -> list[int]:
    if n < 0 or n >= 2**length:
        logger.error(f"Integer {n} is out of range for {length} bits.")
        raise ValueError(f"Integer must be in [0, {2**length-1}] to fit in {length} bits.")
    bits = [int(b) for b in format(n, f'0{length}b')]
    logger.debug(f"Converted integer {n} to {length}-bit header: {bits}")
    return bits

def bits_to_int(bits: list[int]) -> int:
    if not all(bit in (0, 1) for bit in bits):
        logger.error("Bit list contains non-binary values.")
        raise ValueError("Bits must be 0 or 1 only.")
    value = int("".join(str(b) for b in bits), 2)
    logger.debug(f"Converted bits to integer: {value}")
    return value

def add_header(message_bits: list[int]) -> list[int]:
    """
    Prepend a 16-bit header indicating the length of message_bits.
    Returns header_bits + message_bits.
    """
    message_length = len(message_bits)
    logger.debug(f"Preparing header for message length: {message_length} bits")
    header = int_to_bits(message_length, length=16)
    combined = header + message_bits
    logger.debug(f"Total bitstream length after header = {len(combined)} bits")
    return combined

def extract_header(full_bitstream: list[int]) -> tuple[int, list[int]]:
    """
    Reads the first 16 bits as the header to get message_length,
    then returns (message_length, message_bits).
    """
    if len(full_bitstream) < 16:
        logger.error("Bitstream too short to extract header.")
        raise ValueError("Bitstream too short for header (need at least 16 bits).")
    header_bits = full_bitstream[:16]
    logger.debug(f"Extracted header bits: {header_bits}")
    message_length = bits_to_int(header_bits)
    if len(full_bitstream) < 16 + message_length:
        logger.error(f"Bitstream shorter ({len(full_bitstream)}) than expected length (16+{message_length}).")
        raise ValueError("Bitstream shorter than header-specified message length.")
    message_bits = full_bitstream[16:16 + message_length]
    logger.debug(f"Message length from header: {message_length}")
    logger.debug(f"Extracted header: message_length = {message_length} bits")
    return message_length, message_bits
