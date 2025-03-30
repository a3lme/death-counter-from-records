# Death counter on stream records for The First Berserker: Khazan

## Prepare

- Download streams and save it with names st1.mp4, st2.mp4 and etc.
- Split video to images every 2 seconds: `ffmpeg -i st1.mp4 -s 960x540 -r 0.5 st1/output_%06d.jpg`
- Prepare sample image with death label and save it as sample_full.jpg
- Install python requirements.txt
- Corp image to only death label and config by `crop.py` (for kazan with 960x540 already configured)
- Configure LINKS, PART and DEATH_COUNTER in `main.py` and run for each folder with screenshots


## How it works

- Loop throw all *.jpg in folder
- Crop image from sample and crop from image from loop
- Adjust contrast in `enhance_image` function throw LAB color scheme (without this step many missed death when screen is red at screenshot or if boss behind label)
- Convert images to grayscale (structural_similarity works with only 1 channel)
- Compare images by structural_similarity if result grater than 0.3 - use (coefficient selected manually)