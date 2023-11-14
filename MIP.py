import numpy as np
import SimpleITK as sitk
from os.path import join
import argparse

# will give mm value as a slab_size(I need to convert them to voxel)
def createMIP(np_img, slab_size, overlap, choice):
    ''' create the mip image from original image, slice_num is the number of 
    slices for maximum intensity projection'''
    img_shape = np_img.shape # (104,320,240) stands for z, y, x, the unit is voxel
    
    # calculate how many times need to run to iterate through z-axis
    times = round((img_shape[0] - slab_size) / (slab_size - overlap))
    np_mip = np.zeros((times,img_shape[1],img_shape[2]))
    
    start = 0
    end = slab_size

    # choose different method
    if choice == 1:
        # iterate the image through z-axis, move the start & end point (slab_size - overlap) per time
        for i in range(times):
            # capture the max array inside the slab
            np_mip[i,:,:] = np.amax(np_img[start:end],0)

            start += (slab_size - overlap)
            end += (slab_size - overlap)
    elif choice == 2:
        for i in range(times):
            # capture the min array inside the slab
            np_mip[i,:,:] = np.amin(np_img[start:end],0)

            start += (slab_size - overlap)
            end += (slab_size - overlap)
    
    new_spacing = (img_shape[0] / np_mip.shape[0])
    return np_mip, new_spacing

def main():
    # receive parameters from command line
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, default="Input/3D_AXIAL_SWI_0.nii.gz", dest="source", help="please input the source of the image")
    parser.add_argument("--slab_size", type=int, default=10, dest="size", help="please input the slab size")
    parser.add_argument("--overlap", type=int, default=5, dest="overlap", help="please input the overlap size")
    parser.add_argument("--type", type=str, default="MaxIP", dest="type", help="please choose your prjection type(MaxIP or MinIP)")
    args = parser.parse_args()

    sitk_img = sitk.ReadImage(args.source)
    # transform simpleitk image to ndarray, it will change the order of each dimension
    np_img = sitk.GetArrayFromImage(sitk_img)

    slab_size = args.size
    overlap_size = args.overlap
    # one voxel size equals to ? mm (get the spacing on z dimension)
    mm_per_voxel = sitk_img.GetSpacing()[2]
    if(args.type != 'MinIP' and args.type != 'MaxIP'):
        print("Please input correct method")
    else:
        if(args.type == 'MinIP'):
            np_mip, new_spacing = createMIP(np_img, int(slab_size/mm_per_voxel), int(overlap_size/mm_per_voxel),2)
        else:
            np_mip, new_spacing = createMIP(np_img, int(slab_size/mm_per_voxel), int(overlap_size/mm_per_voxel),1)

        # transform ndarray to simpleitk image
        sitk_mip = sitk.GetImageFromArray(np_mip)
        # set image to its original attributes, including origin, spacing, direction
        sitk_mip.SetOrigin(sitk_img.GetOrigin())
        # adjust the spacing after the projection (make sure the size will not be compressed)
        val = [sitk_img.GetSpacing()[0], sitk_img.GetSpacing()[1], new_spacing*mm_per_voxel]
        sitk_mip.SetSpacing(val)
        sitk_mip.SetDirection(sitk_img.GetDirection())
        # export the image that has been processed
        writer = sitk.ImageFileWriter()
        writer.SetFileName(join('Output', 'MIP.nii.gz'))
        writer.Execute(sitk_mip)

if __name__ == '__main__':
    main()