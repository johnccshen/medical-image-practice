import numpy as np
import SimpleITK as sitk
from os.path import join
import os, argparse, sys

def createMIP(np_img: np.array, slab_size: int, overlap: int, choice: int, view: int, ndarray_view: int) -> np.array:
    ''' create the mip image from original image. Takes in a medical image np_img,
        slab_size(already convert to voxel), overlap(alreafy convert to voxel), and
        give choice number to decide which method need to choose(MaxIP or MinIP)
        return the ndarray of the image that has been projected.'''
    start = 0
    end = slab_size
    img_shape = np_img.shape # (104,320,240) stands for z, y, x, the unit is voxel
    
    # calculate how many times need to run to iterate through one axis
    times = round((img_shape[ndarray_view] - slab_size) / (slab_size - overlap))
    # store the image that has been projected 
    if(view == 0):
        np_mip = np.zeros((img_shape[0],img_shape[1],times))
    elif(view == 1):
        np_mip = np.zeros((img_shape[0],times,img_shape[2]))
    else:
        np_mip = np.zeros((times,img_shape[1],img_shape[2]))
    
    # iterate the image through axis, move the start & end point (slab_size - overlap) per time
    for i in range(times):
        # choose different method
        if choice == 1:
            if(view == 0):
                # capture the max array from coronal view
                np_mip[:,:,i] = np.amax(np_img[:,:,start:end],ndarray_view)
            elif(view == 1):
                # capture the max array from sagittal view
                np_mip[:,i,:] = np.amax(np_img[:,start:end,:],ndarray_view)
            else:
                # capture the max array from axial view
                np_mip[i,:,:] = np.amax(np_img[start:end,:,:],ndarray_view)
            
        else:
            if(view == 0):
                # capture the min array from coronal view
                np_mip[:,:,i] = np.amin(np_img[:,:,start:end],ndarray_view)
            elif(view == 1):
                # capture the min array from sagittal view
                np_mip[:,i,:] = np.amin(np_img[:,start:end,:],ndarray_view)
            else:
                # capture the min array from axial view
                np_mip[i,:,:] = np.amin(np_img[start:end,:,:],ndarray_view)

        start += (slab_size - overlap)
        end += (slab_size - overlap)
    
    new_spacing = (img_shape[ndarray_view] / np_mip.shape[ndarray_view])
    return np_mip, new_spacing

def main():
    # receive parameters from command line
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, default="Input/3D_AXIAL_SWI_0.nii.gz", dest="source", help="Input the source of the image")
    parser.add_argument("--output", type=str, default="MIP", dest="output", help="Input the output filename")
    parser.add_argument("--slab_size", type=int, default=10, dest="size", help="Input the slab size(mm)")
    parser.add_argument("--overlap", type=int, default=5, dest="overlap", help="Input the overlap size(mm)")
    parser.add_argument("--type", type=str, default="MaxIP", dest="type", help="Choose your prjection type (MaxIP or MinIP)")
    parser.add_argument("--view", type=str, default="axial", dest="view", help="Select which orientation to project (axial/coronal/sagittal)")
    args = parser.parse_args()

    if os.path.isfile(args.source):
        sitk_img = sitk.ReadImage(args.source)
    else:
        sys.exit("File not found in the image path")
    # transform simpleitk image to ndarray, it will change the order of each dimension
    np_img = sitk.GetArrayFromImage(sitk_img)

    slab_size = args.size
    overlap_size = args.overlap

    # process image in different view, and pick spacing from different dimension
    if(args.view == "axial"):
        view = 2
        ndarray_view = 0
    elif(args.view == "coronal"):
        view = 0
        ndarray_view = 2
    elif(args.view == "sagittal"):
        view = 1
        ndarray_view = 1
    else:
        # TODO add record in the log file
        sys.exit("We did not provide this view")

    # one voxel size equals to ? mm (get the spacing on different axis)
    mm_per_voxel = sitk_img.GetSpacing()[view]
    
    if(args.type != 'MinIP' and args.type != 'MaxIP'):
        # TODO add record in the log file
        sys.exit("Please input correct method")
    else:
        if(args.type == 'MinIP'):
            np_mip, new_spacing = createMIP(np_img, int(slab_size/mm_per_voxel), int(overlap_size/mm_per_voxel), 2, view, ndarray_view)
        else:
            np_mip, new_spacing = createMIP(np_img, int(slab_size/mm_per_voxel), int(overlap_size/mm_per_voxel), 1, view, ndarray_view)

        # transform ndarray to simpleitk image
        sitk_mip = sitk.GetImageFromArray(np_mip)
        # set image to its original attributes, including origin, spacing, direction
        sitk_mip.SetOrigin(sitk_img.GetOrigin())
        # adjust the spacing after the projection (make sure the image size will not be compressed)
        val = list(sitk_img.GetSpacing())
        val[view] = new_spacing*mm_per_voxel
        sitk_mip.SetSpacing(val)

        sitk_mip.SetDirection(sitk_img.GetDirection())
        # export the image that has been processed
        # TODO add new record in the log file
        writer = sitk.ImageFileWriter()
        writer.SetFileName(join('Output', '{}.nii.gz'.format(args.output)))
        writer.Execute(sitk_mip)

if __name__ == '__main__':
    main()