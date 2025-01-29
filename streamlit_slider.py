import argparse
import logging
import pathlib
import sys

import skimage
import numpy as np
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

    # Apply background color & remove margins/padding
    st.markdown(
        """
        <style>
            .block-container { padding: 0px !important; margin: 0px !important; }
            .stApp { background-color: #07323C !important; padding: 0px !important; margin: 0px !important; }
            img { max-width: 100vw !important; height: auto !important; }
            .st-emotion-cache-1kyxreq { width: 100% !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Centered image comparison with rectangular dimensions
    col1, col2, col3 = st.columns([0.1, 0.8, 0.1])  

    with col2:
        image_comparison(
            img1=left_image,
            img2=right_image,
            label1="",
            label2="",
            width=1100  # Wider layout for better rectangular fit
        )


def parse_args():
    parser = argparse.ArgumentParser(description="Compare two images.")
    parser.add_argument("-l", "--left-image", type=str, default=None, help="The left image for the comparison")
    parser.add_argument("-r", "--right-image", type=str, default=None, help="The right image for the comparison")
    return parser.parse_args()


if __name__ == "__main__":
    left_image_path = "left.png"
    right_image_path = "right.png"

    main(left_image_path, right_image_path)

