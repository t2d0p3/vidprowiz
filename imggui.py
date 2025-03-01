import os
import glob
import subprocess
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
from PIL import Image, ImageTk
import cv2

# GUI Setup
root = tk.Tk()
root.title("Video Processing Wizard - Sass Level: Over 9000!")
root.geometry("520x750")  # Increased height to accommodate the progress bar

# Load and Display Image (because wizards need flair)
try:
    img = Image.open("/mnt/data/image.png")  # Original path from your script
    img = img.resize((100, 100), Image.Resampling.LANCZOS)
    img_photo = ImageTk.PhotoImage(img)
    tk.Label(root, image=img_photo).pack(pady=10)
except Exception as e:
    print(f"Failed to load image: {e}—guess we’re going text-only, peasants!")

# Variables
video_path = tk.StringVar()
output_folder = tk.StringVar()
output_filename = tk.StringVar(value="output.mp4")

# Upscaler toggles
us_brightness = tk.BooleanVar()
us_vulkan = tk.BooleanVar()
us_scunet = tk.BooleanVar()
us_waifu2x = tk.BooleanVar()
us_swinir = tk.BooleanVar()
us_realesrgan = tk.BooleanVar()

# Default PATHS (can be modified via Settings)
PATHS = {
    "realesrgan_vulkan": "./realesrgan-ncnn-vulkan.exe",
    "scunet_script": "C:/new/SCUNet/main_test_scunet_real_application.py",
    "waifu2x": "C:/new/waifu2x-caffe/waifu2x-caffe-cui.exe",
    "swinir_script": "C:/new/SwinIR/main_test_swinir.py",
    "realesrgan_script": "inference_realesrgan.py"
}

# Progress bar and status label
progress_bar = ttk.Progressbar(root, length=400, mode="determinate")
progress_label = tk.Label(root, text="Idle - Ready for magic!", font=("Arial", 10))
progress_bar.pack(pady=10)
progress_label.pack()

# Functions
def update_progress(status, value=0):
    progress_bar["value"] = value
    progress_label.config(text=f"Status: {status}")
    root.update()  # Keep GUI responsive

def check_tool_exists(tool_path, tool_name):
    if not os.path.exists(tool_path):
        messagebox.showerror("Error", f"{tool_name} not found at '{tool_path}'. Check your settings!")
        return False
    return True

def select_video():
    filepath = filedialog.askopenfilename(filetypes=[("Video files", "*.mp4;*.avi;*.mov")])
    if filepath:
        video_path.set(filepath)
        print(f"Video locked and loaded: {filepath}")

def select_output_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        output_folder.set(folder_selected)
        print(f"Output folder set to: {folder_selected}. Ready to make magic!")

def extract_frames():
    if not video_path.get() or not output_folder.get():
        messagebox.showerror("Error", "Video and output folder required, genius!")
        return

    frame_output_path = os.path.join(output_folder.get(), "frames")
    os.makedirs(frame_output_path, exist_ok=True)
    cap = cv2.VideoCapture(video_path.get())
    frame_count = 0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # Get total frames for progress

    update_progress("Extracting frames... 0%", 0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imwrite(os.path.join(frame_output_path, f"frame_{frame_count:04d}.jpg"), frame)
        frame_count += 1
        # Update progress (e.g., every 10% or so)
        if total_frames > 0 and frame_count % max(1, total_frames // 10) == 0:
            progress = (frame_count / total_frames) * 100
            update_progress(f"Extracting frames... {progress:.1f}%", progress)

    cap.release()
    update_progress(f"Extracted {frame_count} frames. Your video’s now in pieces—hope you’re proud!", 100)
    print(f"Frames extracted: {frame_count}. Time to get sassy with them!")

def upscale_frames():
    frames_dir = os.path.join(output_folder.get(), "frames")
    upscale_output_path = os.path.join(output_folder.get(), "processed_frames")
    downscale_output_path = os.path.join(output_folder.get(), "final_frames")  # New folder for downscaled frames
    os.makedirs(upscale_output_path, exist_ok=True)
    os.makedirs(downscale_output_path, exist_ok=True)

    frame_files = sorted(glob.glob(os.path.join(frames_dir, "*.jpg")))
    if not frame_files:
        messagebox.showwarning("Warning", "No frames found. Did you extract them, hotshot?")
        return

    # Get original resolution from the first frame
    original_frame = cv2.imread(frame_files[0])
    original_height, original_width = original_frame.shape[:2]
    total_frames = len(frame_files)

    update_progress("Upscaling frames... 0%", 0)
    try:
        # Upscale
        if us_vulkan.get():
            if not check_tool_exists(PATHS["realesrgan_vulkan"], "Real-ESRGAN Vulkan"): return
            subprocess.run([
                PATHS["realesrgan_vulkan"],
                "-i", frames_dir,
                "-o", upscale_output_path,
                "-n", "realesr-animevideov3",
                "-s", "4",  # Upscale 4x
                "-f", "jpg"
            ], check=True)
            print("Vulkan mode: Upscaled 4x—time to sharpen those edges!")

        elif us_scunet.get():
            if not check_tool_exists(PATHS["scunet_script"], "SCUNet script"): return
            subprocess.run([
                "python", PATHS["scunet_script"],
                "--model_name", "scunet_color_real_psnr",
                "--testset_name", frames_dir
            ], check=True)
            # SCUNet outputs to frames_dir; move them
            for i, frame in enumerate(glob.glob(os.path.join(frames_dir, "*.jpg"))):
                os.rename(frame, os.path.join(upscale_output_path, os.path.basename(frame)))
                progress = (i + 1) / total_frames * 100
                update_progress(f"Upscaling with SCUNet... {progress:.1f}%", progress)
            print("SCUNet: Frames so clean they’re practically sparkling!")

        elif us_waifu2x.get():
            if not check_tool_exists(PATHS["waifu2x"], "Waifu2x"): return
            subprocess.run([
                PATHS["waifu2x"],
                "-i", frames_dir,
                "-o", upscale_output_path,
                "-m", "noise_scale",
                "--scale_ratio", "2.0",  # Upscale 2x (Waifu2x default)
                "--noise_level", "2"
            ], check=True)
            print("Waifu2x: Anime vibes incoming—your frames are now 2D perfection!")

        elif us_swinir.get():
            if not check_tool_exists(PATHS["swinir_script"], "SwinIR script"): return
            subprocess.run([
                "python", PATHS["swinir_script"],
                "--task", "classical_sr",
                "--scale", "2",  # Upscale 2x
                "--folder_lq", frames_dir,
                "--folder_gt", ""
            ], check=True)
            # Move SwinIR results from default 'results' folder
            for i, result in enumerate(glob.glob("results/*.jpg")):
                os.rename(result, os.path.join(upscale_output_path, os.path.basename(result)))
                progress = (i + 1) / total_frames * 100
                update_progress(f"Upscaling with SwinIR... {progress:.1f}%", progress)
            print("SwinIR: Upscaling so fancy, your frames might demand a red carpet!")

        elif us_realesrgan.get():
            if not check_tool_exists(PATHS["realesrgan_script"], "Real-ESRGAN script"): return
            subprocess.run([
                "python", PATHS["realesrgan_script"],
                "--model", "RealESRGAN_x4plus",
                "--input", frames_dir,
                "--output", upscale_output_path
            ], check=True)
            print("Real-ESRGAN: Non-Vulkan glory—your frames are ready to strut!")

        else:
            if not check_tool_exists(PATHS["realesrgan_vulkan"], "Real-ESRGAN Vulkan"): return
            subprocess.run([
                PATHS["realesrgan_vulkan"],
                "-i", frames_dir,
                "-o", upscale_output_path,
                "-n", "realesr-x4plus",
                "-s", "4",  # Upscale 4x
                "-f", "jpg"
            ], check=True)
            print("Default Vulkan: Because you didn’t pick, I chose the cool one for you!")

        # Downscale back to original resolution
        for i, frame in enumerate(glob.glob(os.path.join(upscale_output_path, "*.jpg"))):
            subprocess.run([
                "ffmpeg",
                "-i", frame,
                "-vf", f"scale={original_width}:{original_height}",
                "-y",  # Overwrite without prompt
                os.path.join(downscale_output_path, os.path.basename(frame))
            ], check=True)
            progress = (i + 1) / total_frames * 100
            update_progress(f"Downscaling frames... {progress:.1f}%", progress)
        print(f"Downscaled back to {original_width}x{original_height}. Clarity incoming!")

        # Brightness boost (applied to downscaled frames)
        if us_brightness.get():
            bright_output_path = os.path.join(output_folder.get(), "bright_frames")
            os.makedirs(bright_output_path, exist_ok=True)
            for i, frame in enumerate(glob.glob(os.path.join(downscale_output_path, "*.jpg"))):
                subprocess.run([
                    "ffmpeg",
                    "-i", frame,
                    "-vf", "eq=brightness=0.1",
                    "-y",
                    os.path.join(bright_output_path, os.path.basename(frame))
                ], check=True)
                progress = (i + 1) / total_frames * 100
                update_progress(f"Applying brightness... {progress:.1f}%", progress)
            print("Brightness: Your frames just got a glow-up—hope they don’t blind you!")

        update_progress("Frames upscaled and downscaled for max clarity!", 100)

    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"Processing failed: {e}. Check the console for drama!")
        update_progress("Error occurred during processing. Check console.", 0)

def reassemble_video():
    final_frames_dir = os.path.join(output_folder.get(), "bright_frames" if us_brightness.get() else "final_frames")
    output_file_path = os.path.join(output_folder.get(), output_filename.get())

    if not os.path.exists(final_frames_dir) or not glob.glob(os.path.join(final_frames_dir, "*.jpg")):
        messagebox.showerror("Error", "No frames to reassemble. Did you upscale them?")
        return

    frame_files = sorted(glob.glob(os.path.join(final_frames_dir, "*.jpg")))
    total_frames = len(frame_files)

    update_progress("Reassembling video... 0%", 0)
    try:
        cmd = [
            "ffmpeg",
            "-framerate", "10",
            "-i", os.path.join(final_frames_dir, "frame_%04d.jpg"),
            "-c:v", "libx264",
            "-preset", "slow",
            "-crf", "18",
            "-y",  # Overwrite without prompt
            output_file_path
        ]
        subprocess.run(cmd, check=True)
        for i in range(total_frames + 1):  # Simulate progress (FFmpeg doesn’t provide progress natively)
            progress = (i / max(1, total_frames)) * 100
            update_progress(f"Reassembling video... {progress:.1f}%", progress)
        update_progress(f"Video reborn as '{output_filename.get()}'. You’re welcome!", 100)
        print(f"Video reassembled at {output_file_path}. Bow to your creation!")
    except subprocess.CalledProcessError as e:
        messagebox.showerror("Error", f"FFmpeg threw a tantrum: {e}. Check your setup!")
        update_progress("Error reassembling video. Check console.", 0)

def cleanup():
    folders = ["frames", "processed_frames", "final_frames", "bright_frames", "results"]
    total_folders = len(folders)
    update_progress("Cleaning up... 0%", 0)
    for i, folder in enumerate(folders, 1):
        folder_path = os.path.join(output_folder.get(), folder)
        if os.path.exists(folder_path):
            shutil.rmtree(folder_path)
        progress = (i / total_folders) * 100
        update_progress(f"Cleaning up {folder}... {progress:.1f}%", progress)
    update_progress("Temporary files yeeted into the void!", 100)
    print("Cleanup complete. Your disk space thanks me.")

def close_app():
    print("Shutting down the wizard—hope you had fun!")
    root.quit()

def open_settings():
    settings_window = tk.Toplevel(root)
    settings_window.title("Settings - Define Your Paths")
    settings_window.geometry("500x400")

    # Variables for path entries
    path_vars = {
        "realesrgan_vulkan": tk.StringVar(value=PATHS["realesrgan_vulkan"]),
        "scunet_script": tk.StringVar(value=PATHS["scunet_script"]),
        "waifu2x": tk.StringVar(value=PATHS["waifu2x"]),
        "swinir_script": tk.StringVar(value=PATHS["swinir_script"]),
        "realesrgan_script": tk.StringVar(value=PATHS["realesrgan_script"])
    }

    # Function to browse for a file
    def browse_path(var):
        filepath = filedialog.askopenfilename(filetypes=[("Executable/Script", "*.exe;*.py"), ("All files", "*.*")])
        if filepath:
            var.set(filepath)

    # GUI layout for settings
    tk.Label(settings_window, text="Customize Tool Paths", font=("Arial", 12, "bold")).pack(pady=10)

    for key, var in path_vars.items():
        frame = tk.Frame(settings_window)
        frame.pack(pady=5, fill="x", padx=10)
        tk.Label(frame, text=f"{key.replace('_', ' ').title()}:", width=20, anchor="w").pack(side="left")
        tk.Entry(frame, textvariable=var, width=40).pack(side="left", padx=5)
        tk.Button(frame, text="Browse", command=lambda v=var: browse_path(v)).pack(side="left")

    def save_settings():
        global PATHS
        PATHS = {key: var.get() for key, var in path_vars.items()}
        messagebox.showinfo("Settings Saved", "Paths updated successfully. Ready to roll!")
        print("Settings saved. Paths are now:", PATHS)
        settings_window.destroy()

    tk.Button(settings_window, text="Save", command=save_settings, bg="lightgreen").pack(pady=10)
    tk.Button(settings_window, text="Cancel", command=settings_window.destroy, bg="red").pack(pady=5)

# ----- GUI Layout ----- #
tk.Label(root, text="Select Video:", font=("Arial", 10, "bold")).pack(pady=5)
tk.Entry(root, textvariable=video_path, width=50).pack()
tk.Button(root, text="Browse", command=select_video).pack(pady=5)

tk.Label(root, text="Output Folder:", font=("Arial", 10, "bold")).pack(pady=5)
tk.Entry(root, textvariable=output_folder, width=50).pack()
tk.Button(root, text="Browse", command=select_output_folder).pack(pady=5)

tk.Label(root, text="Output Filename:", font=("Arial", 10, "bold")).pack(pady=5)
tk.Entry(root, textvariable=output_filename, width=50).pack()

# Checkboxes
tk.Label(root, text="Enhancements:", font=("Arial", 10, "bold")).pack(pady=5)
tk.Checkbutton(root, text="Add Brightness (Glow-Up)", variable=us_brightness).pack(pady=2)
tk.Checkbutton(root, text="Real-ESRGAN Vulkan (GPU Power)", variable=us_vulkan).pack(pady=2)
tk.Checkbutton(root, text="SCUNet (Denoise King)", variable=us_scunet).pack(pady=2)
tk.Checkbutton(root, text="Waifu2x (Anime Vibes)", variable=us_waifu2x).pack(pady=2)
tk.Checkbutton(root, text="SwinIR (Fancy Upscale)", variable=us_swinir).pack(pady=2)
tk.Checkbutton(root, text="Real-ESRGAN (Non-Vulkan)", variable=us_realesrgan).pack(pady=2)

# Action Buttons
tk.Button(root, text="Extract Frames", command=extract_frames, bg="lightblue").pack(pady=5)
tk.Button(root, text="Upscale Frames", command=upscale_frames, bg="lightyellow").pack(pady=5)
tk.Button(root, text="Reassemble Video", command=reassemble_video, bg="lightpink").pack(pady=5)
tk.Button(root, text="Clean Up", command=cleanup, bg="orange").pack(pady=5)
tk.Button(root, text="Settings", command=open_settings, bg="purple").pack(pady=5)
tk.Button(root, text="Exit", command=close_app, bg="red").pack(pady=5)

root.mainloop()