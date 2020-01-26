from enum import Enum


class Category(str, Enum):
    String = "Strings"
    Maths = "Maths"
    Unit = "Units"
    TextEncoding = "Text Encoding"
    DataEncoding = "Data Encoding"
    Escape = "Escapes"
    Encryption = "Encryption"
    Hash = "Hashes"
    CryptographyMisc = "Cryptography Misc."
    Image = "Image"
    Document = "Document"
    Video = "Video"
    Audio = "Audio"
    Code = "Code"
    Other = "Other"
