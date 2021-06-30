# Video to Braille Subtitles

This code will convert a video into braille subtitles. Watch an example video on **[YouTube](https://youtu.be/t_YsTEhcTpo)**.

Will write more READMEs & technical writeups soon.

## Creating a black video for testing subtitles

```
ffmpeg -i path/to/input-video.mp4 -vf drawbox=color=black:t=fill -c:a copy path/to/output-video.mp4
```

