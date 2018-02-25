import numpy as np
import os
from skimage import io
from skimage.measure import regionprops
from skimage.measure import label
from skimage import util
from skimage import img_as_uint
from skimage import exposure
from skimage import filters, segmentation
from skimage.color import rgb2gray, gray2rgb
import skimage.morphology as morph
from scipy import ndimage
import sys


def labeled_version(grey_im, im):

    # find a dividing line between 0 and 255
    # pixels below this value will be black
    # pixels above this value will be white
    val = filters.threshold_otsu(grey_im)

    # the mask object converts each pixel in the image to True or False
    # to indicate whether the given pixel is black/white
    mask = grey_im < val

    # apply the mask to the image object
    clean_border = segmentation.clear_border(mask)

    p2 = np.percentile(grey_im, 20)
    p98 = np.percentile(grey_im, 70)
    grey_im = exposure.rescale_intensity(grey_im, in_range=(p2, p98))
    io.imsave('test.png', grey_im)

    # labeled contains one integer for each pixel in the image,
    # where that image indicates the segment to which the pixel belongs
    labeled = label(clean_border)

    # create array in which to store cropped articles
    cropped_images = []

    # define amount of padding to add to cropped image
    pad = 20

    # for each segment number, find the area of the given segment.
    # If that area is sufficiently large, crop out the identified segment.
    print(len(im))
    top_ten_areas = sorted(regionprops(labeled), key=lambda x: x.area, reverse=True)[:10]

    for region_index, region in enumerate(top_ten_areas):
        print("area: ", region.area)

        # draw a rectangle around the segmented articles
        # bbox describes: min_row, min_col, max_row, max_col
        minr, minc, maxr, maxc = region.bbox

        # use those bounding box coordinates to crop the image
        cropped_images.append(im[minr - pad:maxr + pad, minc - pad:maxc + pad])

    # create a directory in which to store cropped images
    out_dir = "segmented_articles/"
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    # save each cropped image by its index number
    for c, cropped_image in enumerate(cropped_images):
        io.imsave(out_dir + str(c) + ".png", cropped_image)


def morph_version(grey_im, im):
    Thresh = filters.threshold_otsu(grey_im)

    io.imsave("test1.png", grey_im)
    print(Thresh)
    print(grey_im)
    picBW = grey_im < Thresh
    print(picBW)
    Strel = morph.disk(2)
    Strel2 = morph.disk(5)
    BWimg_dil = morph.dilation(picBW, Strel)
    BWimg_close = morph.closing(BWimg_dil, Strel2)
    foreground = morph.closing(grey_im > Thresh, morph.square(3))
    io.imsave("test.png", img_as_uint(foreground))

    L = label(BWimg_close)
    half_length = int(np.floor(np.size(L, 1) / 2))
    L_cntr = L[half_length, half_length]
    print("Label of blob that contains the center pixel: {}".format(L_cntr))

    cropped_images = []
    pad = 20

    top_ten_areas = sorted(regionprops(L), key=lambda x: x.area, reverse=True)[:10]

    for region_index, region in enumerate(top_ten_areas):
        print("area: ", region.area)

        # draw a rectangle around the segmented articles
        # bbox describes: min_row, min_col, max_row, max_col
        minr, minc, maxr, maxc = region.bbox

        # use those bounding box coordinates to crop the image
        cropped_images.append(im[minr - pad:maxr + pad, minc - pad:maxc + pad])

    # create a directory in which to store cropped images
    out_dir = "segmented_articles/"
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    # save each cropped image by its index number
    for c, cropped_image in enumerate(cropped_images):
        io.imsave(out_dir + str(c) + ".png", cropped_image)

def main(image_file):
    file_extension = image_file.split(".")[-1]

    if file_extension in ["jpg", "jpeg"]:
        im = ndimage.imread(image_file)

    elif file_extension in ["jp2"]:
        im = io.imread(image_file, plugin='freeimage')

    else:
        print("your input file isn't jpg or jp2")
        sys.exit()


    grey_im = rgb2gray(im)
    morph_version(grey_im, im)



if __name__ == '__main__':
    image_file = sys.argv[1]
    main(image_file)
