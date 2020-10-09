# kurve-art

make sure to create a folder called "export" when using record = True

OpenGL does not seem to work on Windows. Tell me if you know what I am doing wrong

use for example ffmpeg to make a video of exported images

ffmpeg -i %04d.png -vcodec libx265 -crf 28 output.mp4
