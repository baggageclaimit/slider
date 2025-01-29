import argparse
import logging
import pathlib
import sys

import skimage
import streamlit as st
from streamlit_image_comparison import image_comparison

# Configure logger
_logger = logging.getLogger(__name__)
_logger.setLevel(logging.WARNING)  # Minimize logging output
_logger_handlers = [logging.StreamHandler(sys.stdout)]
_logger_formatter = logging.Formatter(r"%(asctime)-15s %(levelname)-8s [%(module)s] %(message)s")
_logger.handlers.clear()
for h in _logger_handlers:
    h.setFormatter(_logger_formatter)
    _logger.addHandler(h)


@st.cache_data
def load_data(left_image_path, right_image_path):
    left_image = skimage.io.imread(str(left_image_path))
    right_image = skimage.io.imread(str(right_image_path))

    # Crop images to make them more rectangular
    target_height = int(left_image.shape[0] * 0.6)  # Reduce height to ~60% for a rectangular shape
    center = left_image.shape[0] // 2
    left_image = left_image[center - target_height // 2 : center + target_height // 2, :]
    right_image = right_image[center - target_height // 2 : center + target_height // 2, :]

    return left_image, right_image


def main(left_image_path, right_image_path):
    left_image, right_image = load_data(left_image_path, right_image_path)

    # Force full left-alignment, remove Streamlit footer, and remove all padding/margins
    st.markdown(
        """
        <style>
            .stApp {
                background-color: #07323C !important;
                padding: 0px !important; 
                margin: 0px !important; 
                overflow: hidden !important;
            }
            .block-container {
                padding: 0px !important; 
                margin: 0px !important; 
                width: 100vw !important; 
                max-width: 100vw !important;
            }
            div[data-testid="stVerticalBlock"],
            div[data-testid="stImage"],
            div[data-testid="stHorizontalBlock"] {
                padding: 0px !important; 
                margin: 0px !important;
            }
            section[data-testid="stSidebar"] {
                display: none !important;
            }
            .image-container {
                position: fixed;
                top: 0;
                left: 0;
                width: 100vw;
                height: auto;
                overflow: hidden;
                display: flex;
                align-items: flex-start;
                justify-content: flex-start;
            }
            /* Hide Streamlit branding/footer using the latest class */
            div[class*="_container_1upux_"],
            div[class*="_hostedName_"],
            div[class*="_linkOutText_"],
            div[class*="_linkOutIcon_"],
            footer {
                display: none !important;
                visibility: hidden !important;
                height: 0px !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Ensure the slider is fully flush left
    st.markdown('<div class="image-container">', unsafe_allow_html=True)
    
    image_comparison(
        img1=left_image,
        img2=right_image,
        label1="",
        label2="",
        width=1200  # Wider for better browser fit
    )

    st.markdown('</div>', unsafe_allow_html=True)


def parse_args():
    parser = argparse.ArgumentParser(description="Compare two images.")
    parser.add_argument("-l", "--left-image", type=str, default=None, help="The left image for the comparison")
    parser.add_argument("-r", "--right-image", type=str, default=None, help="The right image for the comparison")
    return parser.parse_args()


if __name__ == "__main__":
    left_image_path = "left.png"
    right_image_path = "right.png"

    main(left_image_path, right_image_path)

