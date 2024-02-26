import pathlib

import click

from . import utils


# Common options
force_opt = click.option(
    "-f", "--force", is_flag=True, help="Overwrite existing files."
)
output_opt = click.option(
    "-o",
    "--output",
    default=".",
    metavar="<DIR>",
    help="Output directory for files. Defaults to the current directory.",
    type=click.Path(file_okay=False, path_type=pathlib.Path),
)


@click.group(
    context_settings={"help_option_names": ["-h", "--help"]},
    help="A Python command-line tool to pack and unpack OSW files from GTA: San Andreas Mobile Version.",
)
def cli():
    pass


# Pack command
@cli.command(help="Pack audio files from directories into OSW files.")
@force_opt
@output_opt
@click.argument(
    "src_dirs",
    nargs=-1,
    required=True,
    type=click.Path(
        exists=True,
        file_okay=False,
        readable=True,
        resolve_path=True,
        path_type=pathlib.Path,
    ),
)
def pack(force, output, src_dirs):
    output.mkdir(parents=True, exist_ok=True)

    for src_dir in src_dirs:
        osw_path = output / f"{src_dir.name}.osw"
        idx_path = osw_path.with_suffix(".osw.idx")

        if osw_path.exists() or idx_path.exists():
            if osw_path.is_dir() or idx_path.is_dir():
                print(
                    f"Warning: {osw_path}(.idx) already exists and is a directory. Skipping."
                )
                continue
            elif not force:
                print(
                    f"Warning: {osw_path}(.idx) already exists. Use -f to overwrite. Skipping."
                )
                continue

        utils.pack_osw(osw_path, idx_path, src_dir)


# Unpack command
@cli.command(help="Unpack audio files from OSW files.")
@force_opt
@output_opt
@click.argument(
    "osw_files",
    nargs=-1,
    required=True,
    type=click.Path(
        exists=True,
        dir_okay=False,
        readable=True,
        resolve_path=True,
        path_type=pathlib.Path,
    ),
)
def unpack(force, output, osw_files):
    output.mkdir(parents=True, exist_ok=True)

    for osw_path in osw_files:
        idx_path = osw_path.with_suffix(".osw.idx")

        if not idx_path.exists():
            print(f"Warning: skipping '{osw_path}' as index file is missing.")
            continue

        # For extracted OSW files
        output_dir = output / osw_path.stem

        if output_dir.exists():
            if output_dir.is_file():
                if not overwrite_flag:
                    print(
                        f"Warning: skipping '{output_dir}' as it already exists and is a file. Use -f to overwrite."
                    )
                    continue
                else:
                    output_dir.unlink()
            elif not overwrite_flag:
                print(
                    f"Warning: skipping '{output_dir}' as it already exists. Use -f to overwrite."
                )
                continue
            else:
                shutil.rmtree(output_dir)

        utils.unpack_osw(osw_path, idx_path, output_dir)


def main() -> None:
    cli()


if __name__ == "__main__":
    main()
