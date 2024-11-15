def makeHumanReadableConfigValue(config_key: str, value: str | int) -> str:
    # Descriptions for integer-based settings.
    integer_descriptions = {
        "fontAttributeReporting": {
            0: "Off",
            1: "Speech",
            2: "Braille",
            3: "Speech and Braille"
        },
        "reportLineIndentation": {
            0: "Off",
            1: "Speech",
            2: "Tones",
            3: "Both Speech and Tones"
        },
        "reportTableHeaders": {
            0: "Off",
            1: "Rows and columns",
            2: "Rows",
            3: "Columns"
        },
        "reportCellBorders": {
            0: "Off",
            1: "Style",
            2: "Color and style"
        }
    }

    # Return "on" or "off" for boolean values.
    if isinstance(value, bool):
        return "checked" if value else "unchecked"

    # Return human-readable string for known integer settings.
    elif isinstance(value, int) and config_key in integer_descriptions:
        return integer_descriptions[config_key].get(value, "Unknown setting")

    # Fallback for out-of-range values.
    return str(value)
