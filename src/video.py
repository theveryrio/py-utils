# Author: Chanho Kim <theveryrio@gmail.com>

import os
from pathlib import Path
from typing import Dict, List, Optional

import cv2
from tqdm import tqdm


__all__ = [
    "images_to_video",
]


CV_IMAGE_FORMAT = [
    ".bmp", ".dib",                     # window bitmaps
    ".jpe", ".jpeg", ".jpg",            # jpeg files 
    ".jp2"                              # jpeg 2000 files
    ".png",                             # portable network graphics
    ".webp",                            # webp
    ".pbm", "pgm", "ppm", "pxm", "pnm", # portable image format
    ".pfm",                             # pfm files
    ".sr", ".ras",                      # sun rasters
    ".tiff", ".tif",                    # tiff files
    ".exr",                             # openexr image files
    ".hdr", ".pic",                     # radiance hdr
]


DEFAULT_CODEC = {
    ".avi": "divx",
    ".flv": "flv1",
    ".mkv": "fmp4",
    ".mov": "mp4v",
    ".mp4": "mp4v",
    ".wmp": "wmv2",
}


def images_to_video(
    input_path: str,
    output_path: str = "output.mp4", 
    fps: int = 30,
    codec: Optional[str] = None,
) -> None:
    """Converts an image sequence into a video file using opencv.

    Args:
        input_path: Directory path containing a sequence of images.
        output_path: File path to save the output video (default: "output.mp4").
        fps: Frequency at which consecutive frames are displayed (default: 30).
        codec: 4-character code of codec used to compress the frames. List of 
            codes can be obtained at FOURCC. If None, finds default codec 
            by file extension (default: None).

    Raises:
        FileNotFoundError: If no image sequence is found.
        ValueError: If no default codec for the file extension is found.
    """
    input_files = [ 
        f for f in sorted(os.listdir(input_path))
        if os.path.splitext(f)[1].lower() in CV_IMAGE_FORMAT
    ]

    if not input_files:
        raise FileNotFoundError(f"No image sequence in path: '{input_path}'")

    path = Path(output_path)

    if codec is None:
        extension = path.suffix
        codec = DEFAULT_CODEC.get(extension.lower())

        if codec is None:
            raise ValueError(f"Unsupported file extension name: '{extension}'")

    fourcc = cv2.VideoWriter_fourcc(*codec)

    frames = (cv2.imread(f"{input_path}/{f}") for f in input_files)

    f = next(frames)
    h, w, _ = f.shape
    size = (w, h)

    os.makedirs(path.parent, exist_ok=True)
    out = cv2.VideoWriter(output_path, fourcc, fps, size)

    out.write(f)
    for f in tqdm(frames, desc=path.name, total=len(input_files), initial=1):
        out.write(f)

    out.release()

