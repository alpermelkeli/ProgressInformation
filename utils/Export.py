import subprocess
import os


def export_project(selected_project, filepath, fps_entry, output_name, file_type, resolution, export_project_callback):
    # Verify that the filepath exists
    if not os.path.exists(filepath):
        print(f"Error: Path {filepath} does not exist.")
        return

    # Create output file path for the mp4 file
    output_video = os.path.join(filepath, output_name)

    # ffmpeg command to convert TGA files to MP4
    command = [
        "ffmpeg",
        "-framerate", fps_entry,
        "-i", os.path.join(filepath, f"1_%05d.{file_type}"),
        "-s", resolution,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        output_video
    ]

    try:
        subprocess.run(command, check=True)

        # Mark project as exported
        selected_project.exported = True

        # Callback to update the UI
        export_project_callback(selected_project.id)

        print(f"Video exported successfully at {output_video}")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while exporting video: {e}")