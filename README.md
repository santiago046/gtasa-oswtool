# GTA: San Andreas Mobile - OSW Tool

`oswtool` is a Python CLI tool for packing and unpacking .OSW files, which store the game sounds, from the classic GTA: San Andreas Mobile version.

.OSW files can contain MP3 or WAV audio in mono. WAV audio is only supported for SFX files.

Unlike other tools, `oswtool` does not zip the audio files like the conventional way, but concatenates them. It can unpack both zipped and concatenated .OSW files, but only `oswtool` can unpack its own concatenated files.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
  - [Pack Command](#pack-command)
  - [Unpack Command](#unpack-command)
- [Examples](#examples)

## Installation

To install `oswtool`, you can use pip. Follow these steps:

1. Clone this repository:
    ```
    git clone https://github.com/santiago046/oswtool
    ```

2. Change to the project directory:
    ```
    cd oswtool
    ```
3. Install using pip:
    ```
    pip install .
    ```

## Usage

`oswtool` has two commands: `pack` and `unpack`. Here is an overview of how to use them:

### Pack Command

The `pack` command takes one or more directories containing .MP3 or .WAV (only supported in SFX by the game) audio files and packs them into OSW files along with .idx files.

```
Usage: oswtool pack [OPTIONS] SRC_DIRS...

  Pack audio files from directories into OSW files.

Options:
  -f, --force         Overwrite existing files.
  -o, --output <DIR>  Output directory for files. Defaults to the current
                      directory.
  -h, --help          Show this message and exit.
```

### Unpack Command

The `unpack` command takes one or more OSW files and unpacks MP3 or WAV files from them.

```
Usage: oswtool unpack [OPTIONS] OSW_FILES...

  Unpack audio files from OSW files.

Options:
  -f, --force         Overwrite existing files.
  -o, --output <DIR>  Output directory for files. Defaults to the current
                      directory.
  -h, --help          Show this message and exit.
```

### Examples:

- Pack SFX directory containing .WAV files into an OSW file to the current directory:
    ```
    oswtool pack ./SFX
    ```
- Pack FEET and SPC_NA directories in `/sdcard/gtasa-modding/` to OSW files and save them into GTA: SA Android data folder:
    ```
    oswtool pack -o /sdcard/Android/com.rockstargames.gtasa/files/audio/SFX/ /sdcard/gtasa-modding/FEET/ /sdcard/gtasa-modding/SPC_NA
    ```
- Pack CUTSCENES directory in `/sdcard/gtasa-modding/` to OSW file and save it into GTA: SA Android data folder allowing overwrite:
    ```
    oswtool pack -f -o /sdcard/Android/com.rockstargames.gtasa/files/audio/STREAMS/ /sdcard/gtasa-modding/CUTSCENE
    ```
- Unpack MP3/WAV files from GENRL.osw to the current directory:
    ```
    oswtool unpack GENRL.osw
    ```
- Unpack BEATS.osw and TK.osw from GTA: SA Android data folder to `/sdcard/gtasa-modding`:
    ```
    oswtool unpack -o /sdcard/gtasa-modding /sdcard/Android/com.rockstargames.gtasa/files/audio/STREAMS/BEATS.osw /sdcard/Android/com.rockstargames.gtasa/files/audio/TK.osw
    ```
- Unpack SPC_NA.osw from GTA: SA Android data folder and save it to `/sdcard/gtasa-modding' allowing overwrite:
    ```
    oswtool unpack -f -o /sdcard/gtasa-modding /sdcard/Android/com.rockstargames.gtasa/files/audio/SFX/SPC_NA.osw
    ```
