
import os
import streamlit as st
import numpy as np
import healpy as hp
from matplotlib import cm
from matplotlib.colors import ListedColormap

cmap = ListedColormap(["tab:grey", "tab:blue", "tab:red", "tab:purple"], "overlap")

cmb_list = ["Planck-Gal-70",
            "SPTPol",
            "SPTSZ",
            "ACTPol",
            "Simons-Observatory",
            "CMB-S4",
            ]

galaxy_list = ["BOSS-DR10",
               "BOSS-North",
               "DES",
               "DESI",
               "LSST",
               "CMASS-North",
               "eBOSS-North",
               "LOWZ-North",
               ]


def get_fsky(input_mask, threshold=0.1):
    """get the fraction of the observable sky

    Parameters
    ---------
    input_mask: np.ndarray
        healpy array indicating the input mask (0: masked, 1: visible)
    threshold: int
        mask cutoff value
    """
    return len(input_mask[input_mask > threshold]) / len(input_mask)

if __name__ == "__main__":
    st.title("CMB x Galaxy Survey Overlaps")
    st.markdown("*Visualize overlaps between Cosmic Microwave Background (CMB) and "
                "Galaxy Surveys*")
    st.markdown("""
                Made by [Siavash Yasini](https://github.com/syasini)
                
                Contributers: Alex Krolewski, Eric Baxter
                
                Checkout the source code on [GitHub](
                https://github.com/syasini/cmb-x-galaxy-overlaps) and press the star button to 
                show your support! ️🤩👉⭐ 
                
                """)

    # --------------
    # CMB Experiment
    # --------------

    # add a checkbox to select the CMB experiment
    st.sidebar.markdown("# CMB")
    cmb = st.sidebar.selectbox("(blue)", cmb_list)
    cmb_fname = os.path.join(".", "masks", cmb + ".fits")
    cmb_mask = hp.read_map(cmb_fname)

    # add button for adding foregrounds (optional)
    add_foregrounds = st.sidebar.checkbox("Add Planck Foregrounds")
    foregrounds_fname = os.path.join(".", "masks", "Planck-Gal-70.fits")

    if add_foregrounds:
        foregrounds = hp.read_map(foregrounds_fname)
        cmb_mask = np.minimum(cmb_mask, foregrounds)

    # calculate and print the CMB f_sky
    cmb_fsky = get_fsky(cmb_mask)
    st.sidebar.text(f"f_sky = {cmb_fsky:.2f}")

    st.sidebar.markdown("---")

    # -------------
    # Galaxy Survey
    # -------------

    # add a checkbox to select the galaxy survey
    st.sidebar.markdown("# Galaxy")
    galaxy = st.sidebar.selectbox("(red)", galaxy_list)
    gal_fname = os.path.join(".", "masks", galaxy+".fits")
    gal_mask = hp.read_map(gal_fname)

    # calculate and print the galaxy f_sky
    gal_fsky = get_fsky(gal_mask)
    st.sidebar.text(f"f_sky = {gal_fsky:.2f}")

    # plot the CMB (pixel values=1) and galaxy (pixel values=2) masks
    hp.mollview(cmb_mask, fig=1, sub=121, cmap=cmap, title=cmb, cbar=False, max=3)
    hp.mollview(2 * gal_mask, fig=1, sub=122, cmap=cmap, title=galaxy, cbar=False, max=3)
    st.pyplot()

    # calculate the overlap
    overlap_mask = cmb_mask + 2 * gal_mask
    overlap_only_mask = 3 * np.logical_and(cmb_mask, gal_mask)

    if st.checkbox("Show Overlap Only"):
        overlap_mask = overlap_only_mask

    overlap_fsky = get_fsky(overlap_only_mask)
    st.text(f"Overlap f_sky = {overlap_fsky:.2f}")

    hp.mollview(overlap_mask, fig=2, cmap=cmap, title=f"{cmb} x {galaxy}", cbar=False, max=3)
    st.pyplot()

    st.sidebar.markdown(
        """
        ---
        ### Notes
        f_sky is the fraction of the visible pixels in the map. 
        These are colored blue in the CMB experiments, red in the galaxy surveys and purple in 
        the overlap between the two. 
        
        The masked pixels are shown in gray 
        
        ---
        Don't see your favorite experiment on the list?
        
        Open a new [issue on GitHub](https://github.com/syasini/cmb-x-galaxy-overlaps/issues) or 
        get in touch with me via email: <siavash.yasini@gmail.com>
        """
        )