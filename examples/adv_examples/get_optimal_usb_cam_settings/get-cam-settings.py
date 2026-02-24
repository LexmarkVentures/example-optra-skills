import logging
import subprocess
import json
import argparse

usb_camera_info = []

def exec_cmd_return_output(command):
    """Execute a command and return the output."""
    lines = []
    with subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        universal_newlines=True,
        shell=True
    ) as cmdpipe:
        stdout, stderr = cmdpipe.communicate()
        status = cmdpipe.wait()
        lines = stdout.splitlines()
        if status:
            err_msg = stderr.splitlines()
            err = f"Command '{command}' failed: rc={status} {err_msg}"
            logger.error(err)
    return lines

def init_usb_camera_info():
    """Gets the USB Camera info from v4l2-ctl.
        Example:

    [
        {
            "Device": "/dev/video3",
            "Name": "UVC Camera (0603:8612) (usb-3610000.xhci-2.1)",
            "Formats": [
                {
                    "Format": "MJPG",
                    "Resolutions": [
                        {
                            "Width": "1920",
                            "Height": "1080",
                            "FrameRates": [
                                "60.000",
                                "30.000"
                            ]
                        }
                    ]
                }
            ]
        }
    ]
    """

    global usb_camera_info

    cmd = "v4l2-ctl --list-devices"
    lines = exec_cmd_return_output(cmd)

    prev_line = ""
    for line in lines:
        if line.strip()[0:10] == "/dev/video":
            usb_camera_info.append(
                {
                    "Device": line.strip(),
                    "Name": prev_line
                }
            )
        else:
            prev_line = line[:-1]

    for cam in usb_camera_info:
        # Get number following "/dev/video"
        index = cam["Device"].split("video", 1)[1]

        cmd = f"v4l2-ctl -d{index} --list-formats"
        lines = exec_cmd_return_output(cmd)

        cam["Formats"] = []

        #### Selecting valid formats and resolutions from the USB camera ####
        for line in lines:
            if "[" in line:
                parsed_line = line.strip().split("'")
                if len(parsed_line) < 2 or parsed_line[1] == "":
                    logger.info("Bad Pixel Format line")
                    # Pixel Format line not valid, so continue
                    continue
                pixel_format = parsed_line[1]
                pixel_format_index = len(cam["Formats"])
                fmts = cam["Formats"]
                fmts.append(
                    {
                        "Format": pixel_format,
                        "Resolutions": []
                    }
                )

                cmd = (
                    f"v4l2-ctl -d{index} --list-framesizes={pixel_format}"
                )
                lines2 = exec_cmd_return_output(cmd)

                for line2 in lines2:
                    if "Size" in line2:
                        resolution = line2.strip().split(" ")[2]
                        width = resolution.split("x")[0]
                        height = resolution.split("x")[1]
                        resolution_index = (
                            len(
                                cam["Formats"]
                                [pixel_format_index]
                                ["Resolutions"]
                            )
                        )
                        res = fmts[pixel_format_index]["Resolutions"]
                        res.append(
                            {
                                "Resolution": width+"x"+height,
                                "FrameRates": []
                            }
                        )

                        cmd = (
                            f"v4l2-ctl -d{index} --list-frameintervals="
                            + f"width={width},"
                            + f"height={height},"
                            + f"pixelformat={pixel_format}"
                        )
                        lines3 = exec_cmd_return_output(cmd)

                        for line3 in lines3:
                            if "Interval" in line3:
                                frame_rate = (
                                    line3.strip().split(" ")[3][1:]
                                )
                                frame_rates = (
                                    res[resolution_index]["FrameRates"]
                                )
                                frame_rates.append(frame_rate)

    # Remove devices that do not have Formats
    for cam in usb_camera_info:
        if not cam["Formats"]:
            logger.info(
                "Removing device with no formats: %s",
                json.dumps(cam, indent=4)
            )
            usb_camera_info.remove(cam)

# Given the desired minimum FPS, pick the 'best' format/resolution.
def select_format(desired_fps, min_fps):
    format = None

    while True:
        device_formats = {}

        format_options = {}

        # we need to choose the format with the highest resolution that supports the framerate we want.
        for device in usb_camera_info:
            all_framerates = []

            logger.debug("Detected device: %s", device["Device"])
            logger.debug("\n----")
            logger.debug("Formats supported by this camera: ")
            fmt_options = [n['Format'] for n in device["Formats"]]
            for fmt in fmt_options:
                logger.debug(fmt)
            logger.debug("----")

            for fmts in device["Formats"]:
                format_name = fmts["Format"]

                for res in fmts["Resolutions"]:
                    r = res["Resolution"]

                    # Record all of the framerates we've seen, but don't add duplicates:
                    supported_frames = [int(float(x))
                                        for x in res["FrameRates"]]
                    all_framerates += list(set(supported_frames) - set(all_framerates))

                    # Check to see if the desired FPS is supported--if not, don't consider this resolution.
                    if desired_fps in supported_frames:
                        if format_name not in format_options.keys():
                            # The resolution is stored as 'widthxheight', so split on the 'x'.
                            x, y = r.split('x')
                            logger.debug("%s x %s = %s, adding as the initial highest resolution found for format %s at %s FPS", x, y, (int(
                                x) * int(y)), format_name, desired_fps)
                            format_options[format_name] = [(int(x) * int(y)), (x, y)]
                        else:
                            x, y = r.split('x')
                            # Compare current resolution to existing, if the existing is better (larger), then keep it.
                            if (int(x) * int(y)) > format_options[format_name][0]:
                                logger.debug("%s x %s = %s > %s, adding as the current highest resolution found for format %s at %s FPS", x, y, (int(
                                    x) * int(y)), format_options[format_name][0], format_name, desired_fps)
                                format_options[format_name] = [(int(x) * int(y)), (x, y)]

            # Select the format with the highest resolution at the desired fps:
            max = 0
            res = ()
            if format_options:
                for key in format_options:
                    if format_options[key][0] > max:
                        max = format_options[key][0]
                        format = key
                        res = format_options[key][1]
                logger.debug("Selected format is: %s at resolution %s x %s and %s FPS",
                             format, res[0], res[1], desired_fps)

            # Try a lower framerate if the camera doesn't support current FPS.
            # Stop if it would take us past the minimum FPS.
            if format == None and desired_fps != min_fps:
                # Pop the next highest FPS off the (sorted) list
                all_framerates.sort(reverse=True)
                logger.debug("FPS options remaining: ")
                logger.debug(all_framerates)
                desired_fps = all_framerates.pop(0)
                logger.debug("Trying a FPS of %i...", int(desired_fps))
            else:
                # Stop if we have a format or our desired_fps can't go any lower
                return format, str(desired_fps)

def main():
    global logger

    logger = logging.getLogger('logger')

    parser = argparse.ArgumentParser()
    parser.add_argument('--min_fps', type=int, default=15)
    args = parser.parse_args()

    init_usb_camera_info()
    fmt, fps = select_format(60, args.min_fps)
    logger.error("Given minimum FPS of %s. Selected format: %s and FPS: %s", args.min_fps, fmt, fps)


if __name__ == "__main__":
    main()