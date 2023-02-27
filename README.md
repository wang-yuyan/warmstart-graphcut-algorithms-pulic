# Image Segmentation Based On Graph Cut Algorithms With Warm-Start

This repository contains code written for the experiments of our paper *Predictive Flows for Faster Ford-Fulkerson*. The original datasets are not included in the folder. This file will contain instructions on which datasets to download and how to run the program.

*This project built on the project "Image Segmentation" at https://github.com/julie-jiang/image-segmentation/ by Julie Jiang, with permission from Julie. Many functions from the original repository are reused and adapted to fit into our framework (these functions are marked in the code files). We thank Julie for her amazing work and support!*

## Files
Here is a list of files and their usages.
- image_cropping.py: image pre-processing tools, reads all image groups and crop all images in the sequence. For convenience, The shape and location of the cropping for each image group are written into the code, not read from the command line.
- imagesegmentation.py: contains all the functions related to performing segmentation on a single image. This is typically used to tune the seeds and also provides the baseline (cold-start Ford-Fulkerson).
- warmstart.py: implements the warm-start algorithm and has all experiment settings. Used to perform the warm-start experiment.
- average.py: reads from the experiment result data and takes the average of these results. Stores the output in a separate .txt file.
- simple_test.py: used to perform a simple test on warmstart.py

More detailed description of the functions can be found in the code files.

## Dependencies
- For python packages, see requirements.txt.
- warmstart.py has dependency on both imagesegmentation.py and augmentingPath.py, while imagesegmentation.py has dependency on augmentingPath.py

## Data and Collected Results Directories
For each image group ``` group_name ```, below is where all data/experiment results are stored:
- sequential_datasets/{group_name}: the original image files
- sequential_datasets/{group_name}_cropped: the cropped, grayscaled image files
- sequential_datasets/{group_name}_seeded: the image files with obj/bkg seeds marked. Folders are named with width of the image used.
- sequential_datasets/{group_name}_cuts: the image files with the found min-cut marked. Folders are named with width of the image used.
- sequential_datasets/{group_name}_results: the files that document the running time and other statistics such as average augmenting path length for both cold- and warm- start. For image sequence with size n * n, the file {n}_time.txt documents the running time, whereas the file {n}_path.txt documents other data.

## Usage

First download the datasets from the links listed in the main body of the paper:
- birdhouse, head, shoe, at https://lmb.informatik.uni-freiburg.de/resources/datasets/sequences.en.html
- dog, at https://lmb.informatik.uni-freiburg.de/resources/datasets/StereoEgomotion.en.html, we used the tool ffmpeg to convert the video to .jpg pictures frame by frame.

Each group has many images and we only pick 10 images. The users can pick however many images they like. The four image groups are named "birdhouse", "head", "shoe" and "dog" respectively. In this directory, create four folders with the names respectively, and put the selected images in each folder from that image group.

First we pre-process the images, for example in group birdhouse:
``` 
python image_cropping.py -g birdhouse
```
This file creates a new folder, ``` sequential_datasets/birdhouse_cropped ```, containing the two cropped, greyscaled images. When we run imagesegmentation.py and warmstart.py the code will be run on the images in this folder. Here "-g" is used to specify the name of the group (must be one of the four names).

Then we try the image segmentation algorithm on one of the images, let's say we've picked birdhouse_080.jpg from dataset birdhouse. After running image_cropping.py on birdhouse group we should get the image birdhouse_080_cropped.jpg

``` 
python imagesegmentation.py -i birdhouse_080_cropped.jpg -g birdhouse -s 30 -l no
```
Commands we've used and their meaning:
- -i: image name
- -g: group name (has to be one of the four)
- -s: size of the resized image, if input n, the resized image will be n pixels * n pixels.
- -l: whether or not the seeds are loaded from an existing file. Default is "yes" and the seeds will be loaded from the directory ``` sequential_datasets/{group_name}_cuts/size/{group_name}_seeds.csv ``` If "no", a window will pop out for user to plant object seeds. After that press ESC and another window will pop out for user to plant background seeds. The planted seeds will be stored in the above directiory and overwrite existing seed files with the same name, if any.

The seeded image is saved in: ``` sequential_datasets/{group_name}_seeded/{size}/{image_name}_seeded.jpg ```

After min cut is found, the program marks all the arcs in the cut with color red and saves the resulting image in ```sequential_datasets/{group_name}_cuts/{size}/{image_name}_cuts.jpg```

To run the warm-start algorithm on a sequence of images, first find the file ``` sequential_datasets/birdhouse_seeds.cvs ``` and copy paste it into the folder ``` sequential_datasets/birdhouse_cuts/30/ ``` This guarantees that the code "warmstart.py" can read the seeds. 

Then, run the following line:
```
python warmstart.py -g birdhouse -s 30
```
The "-g" and "-s" have the same meaning as before. The algorithm reads the seeds from the file we copied and applies the seeds to every image in the folder corresponding to the group birdhouse. It stores the seeded images, applies imagesegmentation.py to the first image in the sequence, and starting with the second image, applies both the function in imagesegmentation.py and the warm-start function to the image sequence using the previous max flow solution. The resulting cuts are stored and data is collected, stored in two .text files:

``` sequential_datasets/{group_name}_results/{size}_time.txt ```, ``` sequential_datasets/{group_name}_results/{size}_path.txt ```

One can then run the code ``` python average.py ``` (not needed here as we have only two images in the example sequence).

## Example Images

1. `birdhouse_080.jpg` 

Original, cropped and grayscaled, seeded image of size 30 * 30

![birdhouse_080.jpg](sequential_datasets/birdhouse/birdhouse_080.jpg) ![birdhouse_080_cropped.jpg](sequential_datasets/birdhouse_cropped/birdhouse_080_cropped.jpg) ![birdhouse_080_cropped_seeded.jpg](sequential_datasets/birdhouse_seeded/30/birdhouse_080_cropped_seeded.jpg)

2. `birdhouse_080.jpg`, `birdhouse_081.jpg`

Cuts on two consecutive images with the same seeds

![birdhouse_080_cropped_cuts.jpg](sequential_datasets/birdhouse_cuts/30/birdhouse_080_cropped_cuts.jpg)![birdhouse_081_cropped_cuts.jpg](sequential_datasets/birdhouse_cuts/30/birdhouse_081_cropped_cuts.jpg)




