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
    return left_image, right_image


def main(left_image_path, right_image_path, display_width=1200):
    left_image, right_image = load_data(left_image_path, right_image_path)

    # Remove all margins and paddings using Streamlit markdown hack
    st.markdown(
        """
        <style>
            .block-container { padding: 0px !important; margin: 0px !important; }
            .stApp { padding: 0px !important; margin: 0px !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    image_comparison(
        img1=left_image,
        img2=right_image,
        label1="",
        label2="",
        width=display_width
    )


def parse_args():
    parser = argparse.ArgumentParser(description="Compare two images.")
    parser.add_argument("-l", "--left-image", type=str, default=None, help="The left image for the comparison")
    parser.add_argument("-r", "--right-image", type=str, default=None, help="The right image for the comparison")
    parser.add_argument("-w", "--display-width", type=int, default=1200, help="Width of the Streamlit Image Comparison")
    return parser.parse_args()


if __name__ == "__main__":
    left_image_path = "left.png"
    right_image_path = "right.png"
    display_width = 1200

    main(left_image_path, right_image_path, display_width)

