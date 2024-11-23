# Document Formatting Rotor for NVDA

## Background

The **Document Formatting Rotor** is an NVDA addon that allows users to quickly adjust document formatting settings without needing to open the settings menu or remember numerous keystrokes. With this addon, users can easily navigate through and modify various document formatting options, streamlining the process of making adjustments.

## Usage

To interact with the **Document Formatting Rotor**, use the following commands:

| **Keystroke** | **Action** |
| -------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **NVDA+G** | Open the Document Formatting Rotor. |
| **Up Arrow** | Navigate to the previous formatting item. |
| **Down Arrow** | Navigate to the next formatting item. |
| **Left Arrow** | Switch to the previous category of settings. |
| **Right Arrow** | Switch to the next category of settings. |
| **Spacebar** | Cycle through the available settings for the currently selected item. This could involve toggling a check/uncheck setting or cycling through a list of options, such as font attributes (e.g., off, speech, braille, or speech and braille). |
| **Escape** | Exit the rotor without saving any changes. |
| **Enter** | Save the selected setting. |
| **Characters (A-Z)** | Search for a setting by name. See the [next section](#searching) for more information. |
| **Backspace** | Delete or remove a character from the search. When the last character is removed, navigation by categories is re-enabled. See the [next section](#searching) for more information. |

## Searching <a id="searching">


The **Document Formatting Rotor** includes a search feature that allows users to quickly find and adjust specific settings. Here's how searching works:

- Users can type part of a setting's name, and the rotor will filter the available options based on that input.
- **Left/Right Arrows**: When search mode is active, the left and right arrows become disabled to prevent navigation between categories.
- **Up/Down Arrows**: Navigate through the settings that match the search term, regardless of where the search term appears in the setting name.
- If the **first** or **last** setting in the search results is reached, the rotor will cycle back to the top or bottom of the list.

### Example Search

1. If you search for the word "line", the first setting containing "line" in its name will be selected.
2. Use the **Up/Down Arrows** to cycle through other settings that contain "line" in their names.
3. use the **space** key to modify the setting under the cursor.
4. Press the **enter** key to save your settings, or **escape** to close everything.

This feature helps you quickly locate and adjust specific settings by their name.

## How to File Bugs

If you encounter any issues or bugs while using the **Document Formatting Rotor**, please report them on GitHub. To file a bug, follow these steps:

1. Visit the GitHub repository: [github.com/derekriemer/nvda-documentFormattingRotor/](https://github.com/derekriemer/nvda-documentFormattingRotor/)
2. Check the issues section to see if your bug has already been reported.
3. If not, create a new issue with detailed information about the problem, including any steps to reproduce it.

Your feedback is essential and will help improve the addon for all users.
