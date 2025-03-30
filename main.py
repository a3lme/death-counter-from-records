"""Find death images by death label"""

# pylint: disable=no-member
import datetime
import os
import cv2
from skimage import color, metrics

# Prepare:
# Download steam, save folder with name like st1.mp4, st2.mp4 and etc.
# Split stream to screenshots every 3 seconds with resize image to 960x540:
# ffmpeg -i st1.mp4 -s 960x540 -r 0.5 st1/output_%06d.jpg
# manually find death label image and save it to work folder with name:
# sample_full.jpg


LINKS = {
    "/st1": "https://www.twitch.tv/videos/*********1",
    "/st2": "https://www.twitch.tv/videos/*********2",
    "/st3": "https://www.twitch.tv/videos/*********3",
    "/st4": "https://www.twitch.tv/videos/*********4",
}

# Set folder with screenshots and start death counter if folder not first
PART = "/st1"
DEATH_COUNTER = 0

# Start coords for crop
Y = 235
X = 240
# Height and width for crop
H = 45
W = 480
# sample image
sample_img = cv2.imread("sample_full.jpg")
image1 = sample_img[Y : Y + H, X : X + W]


def enhance_image(img):
    """Enhance image contrast"""
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l_channel, a, b = cv2.split(lab)

    # Applying CLAHE to L-channel
    # feel free to try different values for the limit and grid size:
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    cl = clahe.apply(l_channel)

    # merge the CLAHE enhanced L-channel with the a and b channel
    limg = cv2.merge((cl, a, b))

    # Converting image from LAB Color model to BGR color spcae
    enhanced_img = cv2.cvtColor(limg, cv2.COLOR_LAB2BGR)

    return enhanced_img


def process_images(i1, i2):
    """Process check images"""

    i1 = color.rgb2gray(enhance_image(i1))
    i2 = color.rgb2gray(enhance_image(i2))
    score1 = metrics.structural_similarity(
        i1,
        i2,
        multichannel=True,
        gaussian_weights=True,
        sigma=1.5,
        use_sample_covariance=False,
        data_range=1.0,
    )
    return score1


prev_sec = 0
for path, _, files in os.walk(os.getcwd() + PART):
    for file in sorted(files):
        if file.endswith(".jpg"):
            img2 = cv2.imread(os.getcwd() + PART + "/" + file)
            image2 = img2[Y : Y + H, X : X + W]
            sim_score = process_images(image1, image2)
            # Filter low similar scoring (value manual selected)
            if sim_score > 0.3:
                # Usage coefficient fromm ffmpeg params
                sec = int(file[7:13]) * 2
                # If no death at previous 12 seconds:
                if (sec - prev_sec) > 12:
                    DEATH_COUNTER += 1
                    # generate hours, mins and seconds for twitch link
                    td = datetime.timedelta(seconds=sec)
                    hours, remainder = divmod(td.seconds, 3600)
                    minutes, seconds = divmod(remainder, 60)

                    # Save image to separate folder for quick check for false positive
                    if not os.path.exists(f"{os.getcwd()}{PART}-c"):
                        os.makedirs(f"{os.getcwd()}{PART}-c")
                    cv2.imwrite(
                        f"{os.getcwd()}{PART}-c/{hours:02d}h{minutes:02d}m{seconds:02d}s.jpg",
                        img2,
                    )
                    # Print results with link to stream for check by everyone
                    print(
                        f"{DEATH_COUNTER:03d}",
                        "ssim:",
                        f"{round(sim_score, 2):.2f}",
                        LINKS[PART]
                        + "?t="
                        + f"{hours:02d}h{minutes:02d}m{seconds:02d}s",
                    )
                prev_sec = sec
