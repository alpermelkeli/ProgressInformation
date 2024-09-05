import subprocess
import os


def export_project(filepath,fps_entry,output_name,file_type,resolution):
    # Verify that the filepath exists
    if not os.path.exists(filepath):
        print(f"Error: Path {filepath} does not exist.")
        return

    # Create output file path for the mp4 file
    output_video = os.path.join(filepath, output_name)

    # ffmpeg command to convert TGA files to MP4
    # Assumes TGA files are named sequentially like img001.tga, img002.tga, etc.
    command = [
        "ffmpeg",
        "-framerate", fps_entry,  # Frame rate for the video
        "-i", os.path.join(filepath, f"img%03d.{file_type}"), # Assuming files are named img001.file_type, img002.file_type, ...
        "-s", resolution,  # Resolution of the output video
        "-c:v", "libx264",  # Codec for video encoding
        "-pix_fmt", "yuv420p",  # Pixel format to ensure compatibility with most players
        output_video
    ]

    try:
        subprocess.run(command, check=True)
        print(f"Video exported successfully at {output_video}")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while exporting video: {e}")
