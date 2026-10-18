#!/usr/bin/env python3
"""Compose exact image grids for campaign mosaics and poster-wall artwork."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable

try:
    from PIL import Image, ImageColor, ImageDraw, ImageFont, ImageOps
except ImportError as exc:
    raise SystemExit(
        "Pillow is required. In Codex desktop, run this script with the bundled "
        "Python executable returned by load_workspace_dependencies."
    ) from exc


def positive_int(value: str) -> int:
    parsed = int(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("value must be greater than zero")
    return parsed


def nonnegative_int(value: str) -> int:
    parsed = int(value)
    if parsed < 0:
        raise argparse.ArgumentTypeError("value cannot be negative")
    return parsed


def parse_color(value: str) -> tuple[int, int, int]:
    try:
        rgb = ImageColor.getrgb(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"invalid color: {value}") from exc
    return rgb[:3]


def load_font(font_path: str | None, size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates: Iterable[Path]
    if font_path:
        candidates = [Path(font_path)]
    else:
        candidates = [
            Path("/System/Library/Fonts/Supplemental/Arial Bold.ttf"),
            Path("/Library/Fonts/Arial Bold.ttf"),
            Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
        ]

    for candidate in candidates:
        if candidate.is_file():
            return ImageFont.truetype(str(candidate), size=size)
    return ImageFont.load_default()


def fit_image(source: Image.Image, size: tuple[int, int], mode: str, background: tuple[int, int, int]) -> Image.Image:
    source = ImageOps.exif_transpose(source).convert("RGB")
    if mode == "cover":
        return ImageOps.fit(source, size, method=Image.Resampling.LANCZOS, centering=(0.5, 0.5))

    contained = ImageOps.contain(source, size, method=Image.Resampling.LANCZOS)
    tile = Image.new("RGB", size, background)
    offset = ((size[0] - contained.width) // 2, (size[1] - contained.height) // 2)
    tile.paste(contained, offset)
    return tile


def draw_center_label(
    size: tuple[int, int],
    label: str,
    background: tuple[int, int, int],
    foreground: tuple[int, int, int],
    font_path: str | None,
    requested_size: int,
) -> Image.Image:
    tile = Image.new("RGB", size, background)
    draw = ImageDraw.Draw(tile)
    max_width = int(size[0] * 0.8)
    max_height = int(size[1] * 0.45)
    font_size = requested_size or max(18, int(min(size) * 0.18))

    while font_size > 10:
        font = load_font(font_path, font_size)
        box = draw.textbbox((0, 0), label, font=font)
        if box[2] - box[0] <= max_width and box[3] - box[1] <= max_height:
            break
        font_size -= 2

    draw.text((size[0] / 2, size[1] / 2), label, fill=foreground, font=font, anchor="mm")
    return tile


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inputs", nargs="+", required=True, type=Path, help="Tile images in reading order")
    parser.add_argument("--output", required=True, type=Path, help="Output PNG or JPEG path")
    parser.add_argument("--cols", type=positive_int, required=True)
    parser.add_argument("--rows", type=positive_int, required=True)
    parser.add_argument("--width", type=positive_int, default=1200)
    parser.add_argument("--height", type=positive_int, default=1200)
    parser.add_argument("--gap", type=nonnegative_int, default=0)
    parser.add_argument("--margin", type=nonnegative_int, default=0)
    parser.add_argument("--background", type=parse_color, default=parse_color("#F4EFE7"))
    parser.add_argument("--fit", choices=("cover", "contain"), default="cover")
    parser.add_argument("--center-label", help="Reserve one tile for a generated center title card")
    parser.add_argument("--center-index", type=nonnegative_int, help="Zero-based title-card position")
    parser.add_argument("--center-bg", type=parse_color, default=parse_color("#AFCADC"))
    parser.add_argument("--center-fg", type=parse_color, default=parse_color("#8F3433"))
    parser.add_argument("--font", help="Path to a TrueType or OpenType font")
    parser.add_argument("--label-size", type=nonnegative_int, default=0, help="Font size; 0 fits automatically")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    slots = args.cols * args.rows
    center_index = None
    if args.center_label is not None:
        center_index = args.center_index if args.center_index is not None else slots // 2
        if center_index >= slots:
            raise SystemExit(f"center index {center_index} is outside a {slots}-tile grid")

    required_inputs = slots - (1 if center_index is not None else 0)
    if len(args.inputs) != required_inputs:
        raise SystemExit(f"expected {required_inputs} input images, received {len(args.inputs)}")

    for path in args.inputs:
        if not path.is_file():
            raise SystemExit(f"input image does not exist: {path}")

    inner_width = args.width - (2 * args.margin) - ((args.cols - 1) * args.gap)
    inner_height = args.height - (2 * args.margin) - ((args.rows - 1) * args.gap)
    if inner_width <= 0 or inner_height <= 0:
        raise SystemExit("margin and gap leave no room for image tiles")
    if inner_width % args.cols or inner_height % args.rows:
        raise SystemExit("canvas dimensions must divide evenly after subtracting margins and gaps")

    tile_size = (inner_width // args.cols, inner_height // args.rows)
    canvas = Image.new("RGB", (args.width, args.height), args.background)
    input_iter = iter(args.inputs)

    for index in range(slots):
        row, col = divmod(index, args.cols)
        x = args.margin + col * (tile_size[0] + args.gap)
        y = args.margin + row * (tile_size[1] + args.gap)

        if index == center_index:
            tile = draw_center_label(
                tile_size,
                args.center_label,
                args.center_bg,
                args.center_fg,
                args.font,
                args.label_size,
            )
        else:
            with Image.open(next(input_iter)) as source:
                tile = fit_image(source, tile_size, args.fit, args.background)
        canvas.paste(tile, (x, y))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    suffix = args.output.suffix.lower()
    if suffix in {".jpg", ".jpeg"}:
        canvas.save(args.output, quality=95, subsampling=0)
    else:
        canvas.save(args.output)
    print(f"Wrote {args.output} ({args.width}x{args.height}, {args.cols}x{args.rows})")


if __name__ == "__main__":
    main()
