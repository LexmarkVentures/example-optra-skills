import os
import time
from Xlib import X, display

def main():
    display_name = os.environ.get('DISPLAY', ':0')
    print(f"Connecting to display: {display_name}")

    try:
        disp = display.Display(display_name)
    except Exception as e:
        print(f"Error connecting to X11 display: {e}")
        print("Make sure HDMI privilege is enabled and DISPLAY environment variable is set")
        return

    screen = disp.screen()
    root = screen.root
    width, height = 800, 600
    window = root.create_window(
        0, 0, width, height, 0,
        screen.root_depth,
        X.InputOutput,
        X.CopyFromParent,
        background_pixel=screen.black_pixel,
        event_mask=X.ExposureMask | X.KeyPressMask
    )
    window.set_wm_name('HDMI Display Example')
    window.set_wm_class('hdmi_example', 'HDMIExample')
    gc = window.create_gc(
        foreground=screen.white_pixel,
        background=screen.black_pixel
    )
    window.map()
    disp.sync()

    print(f"Displaying bouncing ball animation on HDMI output...")

    ball_radius = 30
    ball_x = width // 2
    ball_y = height // 2
    velocity_x = 3
    velocity_y = 2
    colormap = screen.default_colormap
    color = colormap.alloc_named_color("red").pixel
    ball_gc = window.create_gc(
        foreground=color,
        background=screen.black_pixel
    )
    try:
        frame_count = 0
        while True:
            window.clear_area(0, 0, width, height)
            ball_x += velocity_x
            ball_y += velocity_y
            if ball_x - ball_radius <= 0 or ball_x + ball_radius >= width:
                velocity_x = -velocity_x
                ball_x = max(ball_radius, min(width - ball_radius, ball_x))
            if ball_y - ball_radius <= 0 or ball_y + ball_radius >= height:
                velocity_y = -velocity_y
                ball_y = max(ball_radius, min(height - ball_radius, ball_y))

            window.fill_arc(
                ball_gc,
                int(ball_x - ball_radius),
                int(ball_y - ball_radius),
                ball_radius * 2,
                ball_radius * 2,
                0,
                360 * 64
            )

            frame_count += 1
            text = f"Frame: {frame_count}"
            window.draw_text(gc, 10, 20, text)
            disp.sync()
            time.sleep(1.0 / 60.0)
    except KeyboardInterrupt:
        print("\nStopping animation...")
    finally:
        window.unmap()
        disp.close()
        print("Display closed.")

if __name__ == '__main__':
    main()
