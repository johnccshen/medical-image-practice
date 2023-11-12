# medical-image-practice
Repo for WITS intern to learn how to do medical imaging processing

# Goals
Through the implementation of intensity projection algorithms MinIP (minimum intensity projection) and MaxIP (maximum intensity projection), we can have a basic understanding of medical imaging and image processing. Familiar with what information will be stored in DICOM, and what DICOM information needs to be considered and updated during image processing, as well as the concept of medical image coordinates. The concept of version control and software development process CICD can also be glimpsed from the implementation process.

# Prerequisites
Before proceeding with the project, ensure that you have the following:
- Set up the environment, and install the required tools: NumPy, ITK-SNAP (for image display), Nibabel or SimpleITK, and Git.
- Understand the basics of DICOM and NifTI.
- Familiarize yourself with the concept of image orientation.
- Have a basic understanding of Image processing, specifically MaxIP (Maximum Intensity Projection) and MinIP (Minimum Intensity Projection).

# Requests
### **Algorithm implementation**
1. Generate a MinIP image with a **thickness of 10mm** and an **overlap of 5mm**
    1. Write a function that takes the following input arguments: **image path, thickness, overlap,** and **projection type (MaxIP or MinIP)**.
    2. We expect a similar result of MinIP as the attached image (Fig1.).
    3. In which direction should MinIP be applied?
2. Compare the MinIP result with the raw image using **ITK-SNAP**.
3. Create a MaxIP image using the same parameters as the previous MinIP, and then compare it with the result of the MinIP.

### Other requests
1. Use Git for version control
    1. create a new branch
    2. create a PR
3. Write your own design document


# Material

---

### Image File

**Attached File:** 

Input image (DICOM and NifTI): Input image.zip

MinIP example: Sponsor SWI image.zip


# Useful link
[MIP Video](https://www.youtube.com/watch?v=Qmdl0zckFnw)
[Image orientation and spacing 1](https://simpleitk.readthedocs.io/en/v1.2.4/Documentation/docs/source/fundamentalConcepts.html)
[Image orientation and spacing 2](https://simpleitk.org/SPIE2019_COURSE/02_images_and_resampling.html#:~:text=Basic%20Image%20Attributes%20(Meta-Data)%C2%B6)
[DICOM Header](https://dicom.innolitics.com/ciods/rt-dose/image-plane/00200032)
[MaxIP example code 1](https://gist.github.com/fepegar/a8814ff9695c5acd8dda5cf414ad64ee)
[MaxIP example code 2](https://github.com/ljpadam/maximum_intensity_projection/blob/master/maximum_intensity_projection.py)
