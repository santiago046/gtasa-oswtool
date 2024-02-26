import os
import pathlib
import shutil
import struct
from collections.abc import Iterator


def _list_audio_files(input_dir: pathlib.Path) -> Iterator[pathlib.Path]:
    """A helper function to yield .wav and .mp3 audio files.

    Args:
        input_dir: The directory pathlib.Path object to search files in.

    Yields:
        pathlib.Path: The .wav or .mp3 file path.
    """
    for root, dirs, files in os.walk(input_dir):
        # Sorting files in place because `sorted(os.walk)` still returned
        # results out of order.
        dirs.sort()
        files.sort()

        for file in files:
            if file.lower().startswith((
                "sound_",
                "track_",
            )) and file.lower().endswith((".wav", ".mp3")):
                yield pathlib.Path(root) / file


def pack_osw(
    osw_path: pathlib.Path, idx_path: pathlib.Path, input_dir: pathlib.Path
) -> None:
    """Pack a directory cointaining audio files into a OSW file.

    Args:
        osw_path: The output OSW file path.
        idx_path: The output OSW idx/index file path.
        input_dir: The input directory path to pack into OSW file.

    Returns:
        None
    """
    with (
        open(osw_path, "wb") as osw_file,
        open(idx_path, "wb") as idx_file,
    ):
        # Total of files, it will be upgraded after for loop
        idx_file.write(b"\x00" * 4)

        for total_files, audio_file in enumerate(_list_audio_files(input_dir), 1):
            audio_rel_path = f"{audio_file.relative_to(input_dir)}".encode(
                "ASCII"
            )

            # Write offset, data size, file name lenght and file name
            idx_file.write(
                struct.pack(
                    "<IIH",
                    osw_file.tell(),
                    audio_file.stat().st_size,
                    len(audio_rel_path),
                )
            )
            idx_file.write(audio_rel_path)

            with open(audio_file, "rb") as audio_data:
                shutil.copyfileobj(audio_data, osw_file, 1000 * 1000)

        # Update total of files in idx file
        idx_file.seek(0)
        idx_file.write(struct.pack("<I", total_files))


def unpack_osw(
    osw_path: pathlib.Path, idx_path: pathlib.Path, output_dir: pathlib.Path
) -> None:
    """Unpack audio files from OSW file to a directory.

    Args:
        osw_path: The input OSW file path.
        idx_path: The input OSW index/idx file path.
        output_dir: The output directory path to unpack files to.

    Returns:
        None
    """
    with (
        open(osw_path, "rb") as osw_file,
        open(idx_path, "rb") as idx_file,
    ):
        (total_files,) = struct.unpack("<I", idx_file.read(4))

        # Counter for later checking
        extracted_files = 0

        while True:
            idx_chunk = idx_file.read(10)
            if not idx_chunk:
                break

            # Read offset, data size, file name lenght and file name
            audio_data_offset, audio_data_size, audio_name_len = struct.unpack(
                "<IIH", idx_chunk
            )
            audio_name = idx_file.read(audio_name_len).decode("ASCII")

            audio_output_path = output_dir / audio_name
            audio_output_path.parent.mkdir(parents=True, exist_ok=True)

            with open(audio_output_path, "wb") as audio_output_file:
                osw_file.seek(audio_data_offset)
                audio_output_file.write(osw_file.read(audio_data_size))

            extracted_files += 1

        if extracted_files != total_files:
            print(
                f"Warning: total of files in '{idx_path}' header differs from total of extracted files."
            )
