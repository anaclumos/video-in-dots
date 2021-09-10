# Video to Braille Subtitles

This code will convert a video into braille subtitles. Watch an example video on **[YouTube](https://youtu.be/t_YsTEhcTpo)**. If the video errors in any way, you can take a look at my [screen recording](https://youtu.be/-Dby42c_4Y4).

- [technical writeup in Korean](https://blog.chosunghyun.com/kr-video-braille-pattern-stream/)

## If you want to run this code

1. Rename your video to simpler words (for easier typing)
1. Edit and run `save-to-frames.py`.
1. If you want to run file locally, edit and run `create-srt.py`.
1. If you want to upload subtitles to YouTube, edit and run `create-smi.py`. Note that YouTube only accepts subtitles with 10MB file size limit.

## Creating a black video for testing subtitles

```
ffmpeg -i path/to/input-video.mp4 -vf drawbox=color=black:t=fill -c:a copy path/to/output-video.mp4
```

