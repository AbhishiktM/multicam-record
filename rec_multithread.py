# First run to get global names of camera
# ffmpeg -f dshow -list_devices true -i dummy

import subprocess
import datetime
import os

def record_multiple_cams(cam_names):
    """
    Record multiple USB cameras in parallel using ffmpeg.
    cam_names: dict with { "cam0": "<full_dshow_device_name>", "cam1": "<full_dshow_device_name>" }
    """

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs("recordings", exist_ok=True)

    processes = []

    for idx, (cam_label, cam_name) in enumerate(cam_names.items()):
        output_file = f"recordings/{cam_label}_{timestamp}.avi"

        ffmpeg_cmd = [
            "ffmpeg",
            "-y",
            "-f", "dshow",
            "-framerate", "30",
            "-video_size", "1280x720",
            "-i", f"video={cam_name}",
            "-c:v", "copy",              # <-- copy MJPEG directly, no re-encode
            output_file
        ]

        print(f"[INFO] Starting {cam_label}: {cam_name} → {output_file}")
        processes.append(subprocess.Popen(ffmpeg_cmd))

    print("\n[INFO] Recording... Press ENTER to stop all.\n")
    input()

    print("[INFO] Stopping all recordings...")
    for p in processes:
        p.terminate()

    print("[INFO] Saved all recordings.")


if __name__ == "__main__":
    # Use full DirectShow device names from `ffmpeg -list_devices true -f dshow -i dummy`
    cam_devices = {
        "cam0": r"@device_pnp_\\?\usb#vid_1bcf&pid_2cd1&mi_00#7&1bd18552&0&0000#{65e8773d-8f56-11d0-a3b9-00a0c9223196}\global",
        "cam1": r"@device_pnp_\\?\usb#vid_1bcf&pid_2cd1&mi_00#8&3464d073&0&0000#{65e8773d-8f56-11d0-a3b9-00a0c9223196}\global"
    }

    record_multiple_cams(cam_devices)


