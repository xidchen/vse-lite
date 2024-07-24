import os
import platform

input_dir = "videos"
output_dir = "subtitles"
input_sfx = ".mp4"
output_sfx = ".srt"

temp_storage_dir = "temp_storage"

vsf_sub_frame_length = 6
vsf_top_video_image_percent_end = 0.36
vsf_bottom_video_image_percent_end = 0.24
vsf_left_video_image_percent_end = 0.01
vsf_right_video_image_percent_end = 0.99


if platform.system() == "Windows":
    vsf_dir = r"C:\Exes\VideoSubFinder_6.10_x64\Release_x64"
    vsf_exe_path = os.path.join(vsf_dir, "VideoSubFinderWXW.exe")
elif platform.system() == "Linux":
    vsf_dir = os.path.join(os.path.expanduser("~"), "Exes", "VideoSubFinder")
    vsf_exe_path = "./VideoSubFinderWXW.run"
