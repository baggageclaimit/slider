import argparse
import logging
import pathlib
import sys

import skimage
import streamlit as st
from streamlit_image_comparison import image_comparison

# Configure logger
_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)  # configure log level here
_logger_handlers = [logging.StreamHandler(sys.stdout)]
_logger_formatter = logging.Formatter(
    r"%(asctime)-15s %(levelname)-8s [%(module)s] %(message)s"
)
_logger.handlers.clear()
for h in _logger_handlers:
    h.setFormatter(_logger_formatter)
    _logger.addHandler(h)


@st.cache_data
def load_data(left_image_path, right_image_path):
    _logger.info(f"Load left image: {left_image_path}")
    left_image = skimage.io.imread(str(left_image_path))

    _logger.info(f"Load right image: {right_image_path}")
    right_image = skimage.io.imread(str(right_image_path))

    return left_image, right_image


def main(left_image_path, right_image_path, display_width=2800):
    logo_path = pathlib.Path("./logo").resolve()
    page_icon_folder = logo_path / "Logomark"
    horizontal_folder = logo_path / "Horizontal Logo"

    page_icon = [f for f in page_icon_folder.glob("*Deep*Green.svg")][0]
    horizontal_logo_light = [f for f in horizontal_folder.glob("*Light*Green.svg")][0]

    st.set_page_config(
        page_title="Bedrock Research Change Detection",
        layout="wide",
        page_icon=str(page_icon),
    )

    #st.image(str(horizontal_logo_light), width=1200)
    #st.title("Unsupervised Change Detection Demo")

    left_image, right_image = load_data(left_image_path, right_image_path)

    image_comparison(
        img1=left_image,
        img2=right_image,
        label1="Pre-Image with Change Overlay",
        label2="Post-Image with Change Overlay",
        width=display_width,
    )
    #st.caption("Move slider to compare images before and after.")


def parse_args():
    # Initialize the argument parser
    parser = argparse.ArgumentParser(
        description="Compare two images.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "-l",
        "--left-image",
        type=str,
        default=None,
        help="The left image for the comparison",
    )
    parser.add_argument(
        "-r",
        "--right-image",
        type=str,
        default=None,
        help="The right image for the comparison",
    )
    parser.add_argument(
        "-w",
        "--display-width",
        type=int,
        default=1800,
        help="Width of the Streamlit Image Comparison",
    )
    return parser.parse_args()


if __name__ == "__main__":
    left_image_path = "left.png"
    right_image_path = "right.png"
    display_width = 600

    main(left_image_path, right_image_path, display_width)
