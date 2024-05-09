import os
import pathlib
import shutil
import subprocess
import sys

import rapid_videocr

import cfg
import utils


root_dir = os.getcwd()
input_dir = os.path.join(root_dir, cfg.input_dir)
output_dir = os.path.join(root_dir, cfg.output_dir)
temp_storage_dir = os.path.join(root_dir, cfg.temp_storage_dir)

if not os.path.exists(input_dir):
    print(f"Input directory {cfg.input_dir} does not exist.")
    sys.exit(1)
if not os.path.exists(output_dir):
    print(f"Create output directory {output_dir}.")
    os.makedirs(output_dir)


def extract_subtitles() -> None:
    for video_dir, _, video_names in os.walk(input_dir):
        srt_dir = video_dir.replace(cfg.input_dir, cfg.output_dir)
        for video_name in video_names:
            if video_name.endswith(cfg.input_sfx):
                video_path = os.path.join(video_dir, video_name)
                srt_name = video_name.replace(cfg.input_sfx, cfg.output_sfx)
                srt_path = os.path.join(srt_dir, srt_name)
                if not os.path.exists(srt_dir):
                    os.makedirs(srt_dir)
                if os.path.exists(temp_storage_dir):
                    shutil.rmtree(temp_storage_dir)
                os.makedirs(temp_storage_dir)
                subprocess.run(
                    [cfg.vsf_exe_path, "-c", "-r",
                     "-i", video_path,
                     "-o", temp_storage_dir,
                     "-sub_frame_length", f"{cfg.vsf_sub_frame_length}",
                     "-te", f"{cfg.vsf_top_video_image_percent_end}",
                     "-be", f"{cfg.vsf_bottom_video_image_percent_end}",
                     "-le", f"{cfg.vsf_left_video_image_percent_end}",
                     "-re", f"{cfg.vsf_right_video_image_percent_end}"]
                )
                extractor = rapid_videocr.RapidVideOCR(out_format="srt")
                tmp_rgb_dir = os.path.join(temp_storage_dir, "RGBImages")
                for tmp_rgb_name in os.listdir(tmp_rgb_dir):
                    if '-' in tmp_rgb_name:
                        os.remove(os.path.join(tmp_rgb_dir, tmp_rgb_name))
                extractor(
                    video_sub_finder_dir=tmp_rgb_dir,
                    save_dir=srt_dir,
                    save_name=pathlib.Path(srt_name).stem
                )
                shutil.rmtree(temp_storage_dir)
                input_file_path = utils.last_two_levels(video_path)
                output_file_path = utils.last_two_levels(srt_path)
                print(f"{input_file_path} -> {output_file_path}")


if __name__ == "__main__":
    extract_subtitles()
