# vidprowiz

Video Processing Wizard - Sass Level: Over 9000!

**Welcome to the Video Processing Wizard, a sassy, user-friendly GUI application built with Python and Tkinter for enhancing video quality through frame-by-frame upscaling and processing!**

## Overview
The Video Processing Wizard is designed to extract frames from a video, upscale them using advanced AI-based tools like Real-ESRGAN, SCUNet, Waifu2x, SwinIR, and more, and reassemble them into a high-quality video. With a playful, sarcastic tone and a sleek interface, this tool is perfect for video enthusiasts, content creators, and developers looking to supercharge their video clarity.

Used Python 3.10.8. 

Key features include:
- **Frame Extraction**: Break down videos into individual frames for processing.
- **Advanced Upscaling**: Use state-of-the-art upscaling models (e.g., Real-ESRGAN Vulkan, SwinIR) to enhance resolution and clarity, with an optional downscale step to preserve original size while improving quality.
- **Brightness Enhancement**: Add a glow-up to your frames for extra pop.
- **Progress Tracking**: Real-time progress bar and status updates to keep you informed.
- **Interrupt Functionality**: Stop long-running processes mid-operation with a "Stop" button.
- **Cleanup**: Automatically remove temporary files to keep your workspace tidy.
- **Settings Customization**: Configure paths to external tools like Real-ESRGAN, Waifu2x, and more via a settings dialog.

## Why "Sass Level: Over 9000!"?
This app isn’t just functional—it’s got attitude! Expect witty messages and a fun user experience as it transforms your videos with sass and style.

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/video-processing-wizard.git
   cd video-processing-wizard
   ```
2. Install the required dependencies:
   
   pip install -r requirements.txt
   
3. Ensure you have the necessary external tools (e.g., Real-ESRGAN, Waifu2x, FFmpeg) installed and configured in the `PATHS` dictionary or via the Settings menu.
4. Run the app:
 
   python imggui.py
 

## Dependencies
Check `requirements.txt` for Python packages required to run the app. Note that external tools (like Real-ESRGAN, Waifu2x, SwinIR, and SCUNet) need to be downloaded separately and configured manually, as they are not included in this repository due to their size and licensing.

## Usage
- Select a video file and output folder via the GUI.
- Choose enhancement options (e.g., Real-ESRGAN Vulkan, brightness boost).
- Click "Extract Frames," "Upscale Frames," and "Reassemble Video" to process your video.
- Use the "Stop" button to interrupt processing if needed.
- Clean up temporary files with the "Clean Up" button.

## Contributing
Contributions are welcome! Fork this repository, make your changes, and submit a pull request. Please follow the code style and include tests for new features.

## License
This project is licensed under the [MIT License](LICENSE). See the `LICENSE` file for details.

## Acknowledgments
- Built with love using Python, Tkinter, OpenCV, and FFmpeg.
- Thanks to the creators of Real-ESRGAN, Waifu2x, SwinIR, SCUNet, and other upscaling tools for their amazing work.



- **Notes on Dependencies**:
  - `opencv-python`: Used for video frame extraction and processing.
  - `Pillow`: Used for loading and displaying the GUI image.
  - External tools like Real-ESRGAN, Waifu2x, SwinIR, SCUNet, and FFmpeg are not Python packages and must be installed separately (as scripts or executables). They’re configured via the `PATHS` dictionary in the GUI, so they’re not listed in `requirements.txt`.

Save this as `requirements.txt` in your `C:\new` directory alongside `imggui4.py`.

---


  ```
  ## External Tools Required
  This app relies on the following external tools, which must be downloaded and configured manually:

  - **Real-ESRGAN (Vulkan)**: Download the `realesrgan-ncnn-vulkan.exe` from [here](https://github.com/xinntao/Real-ESRGAN/releases).
  - **Waifu2x**: Download `waifu2x-caffe-cui.exe` from [here](https://github.com/lltcggie/waifu2x-caffe/releases).
  - **SwinIR**: Clone the SwinIR repository from [here](https://github.com/JingyunLiang/SwinIR) and install the `main_test_swinir.py` script.
  - **SCUNet**: Clone the SCUNet repository from [here](https://github.com/cszn/SCUNet) and install the `main_test_scunet_real_application.py` script.
  - **FFmpeg**: Download from [here](https://ffmpeg.org/download.html) and ensure it’s in your system PATH.

  Update the `PATHS` dictionary in `imggui4.py` or use the Settings menu to specify these paths.
  ```

---

