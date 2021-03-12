import matplotlib.pyplot as plt

def show_anatomical_slice(image, orientation, slice_nr):
    """
    Shows a preferred slice from the 3D nifti image
    Indexing: [Medio-lateral, Antero-posterior, Cranio-caudal]
    
    :param image: 3D numpy array with grey values
    :param orientation: str, choose from ["sagittal", "frontal", "axial"]
    :param slice_nr: int, desired slice number
    """
    
    # Get desired slice and the according x and y labels
    Slice, x_lab, y_lab = _get_slice(image, orientation, slice_nr)

    # Plot
    fig,ax = plt.subplots(figsize = (8,8))
    ax.set_title(f'{orientation} slice #{slice_nr}', fontsize = 20)
    ax.set_xlabel(x_lab, fontsize = 20)
    ax.set_ylabel(y_lab, fontsize = 20)
    ax.imshow(Slice.T, cmap="gray", origin="lower")  # .T and "lower" are important for orientation
    
    
def show_functional_slice(image, orientation, slice_nr, timepoint, color_map = 'coolwarm'):
    """
    Shows a preferred slice from the 4D nifti image, for a specific timepoint
    Indexing: [Medio-lateral, Antero-posterior, Cranio-caudal, Time]
    
    :param image: 4D numpy array with grey values
    :param orientation: str, choose from ["sagittal", "frontal", "axial"]
    :param slice_nr: int, desired slice number
    :param timepoint: int, desired timepoint
    :param color_map: str, color map that you want to use for fancy slice plotting
    """
    
    # Get desired slice and the according x and y labels
    image_3D = image[:,:,:,timepoint]
    Slice, x_lab, y_lab = _get_slice(image_3D, orientation, slice_nr)

    # Plot
    fig,ax = plt.subplots(figsize = (8,8))
    ax.set_title(f'{orientation} slice #{slice_nr}', fontsize = 20)
    ax.set_xlabel(x_lab, fontsize = 20)
    ax.set_ylabel(y_lab, fontsize = 20)
    ax.imshow(Slice.T, cmap=color_map, origin="lower")  # .T and "lower" are important for orientation


def track_voxel(image, ML_position, AP_position, CC_position, slice_timepoint = 0, color_map = 'coolwarm', voxel_color = 'white', plot_voxel_in_slice = True):
    """
    Tracks the BOLD signal within a voxel over time
    Indexing: [Medio-lateral, Antero-posterior, Cranio-caudal]
    
    :param image: 4D numpy array with grey values
    :param ML_position: int, position of voxel in Medio-lateral direction
    :param AP_position: int, position of voxel in Antero-posterior direction
    :param CC_position: int, position of voxel in Cranio-caudal direction
    :param slice_timepoint: int, at which timepoint you want to show the slices
    :param color_map: str, color map that you want to use for fancy slice plotting
    """
    
    # Get 1D vector containing the voxel's value over time
    voxel_over_time = image[ML_position, AP_position, CC_position, :]
    
    # Plotting
    # 0. Create figure and different subplots - Source: https://www.geeksforgeeks.org/how-to-create-different-subplot-sizes-in-matplotlib/
    fig = plt.figure() 
    fig.set_figheight(20)
    fig.set_figwidth(20) 

    axSagit = plt.subplot2grid(shape=(3, 3), loc=(0, 0), colspan=1) 
    axFront = plt.subplot2grid(shape=(3, 3), loc=(0, 1), colspan=1) 
    axAxial = plt.subplot2grid(shape=(3, 3), loc=(0, 2), colspan=2) 
    axTime = plt.subplot2grid(shape=(3,3), loc =(1,0), colspan = 3)
    
    # 1. Plot position of voxel on all 3 slices
    # Create 1 plot per orientation in a for-loop
    for orientation, ax, slice_nr in zip(['sagittal', 'frontal', 'axial'], 
                                         [axSagit, axFront, axAxial], 
                                         [ML_position, AP_position, CC_position]):
        
        # Get slice and corresponding x and y label
        image_3D = image[:,:,:,slice_timepoint]
        Slice, x_lab, y_lab = _get_slice(image_3D, orientation, slice_nr)
        
        # Aesthetics of slice image
        ax.set_title(f'{orientation} slice #{slice_nr}', fontsize = 18)
        ax.set_xlabel(x_lab, fontsize = 18)
        ax.set_ylabel(y_lab, fontsize = 18)
        ax.imshow(Slice.T, cmap=color_map, origin="lower")  # .T and "lower" are important for orientation
        
        # Plot position of voxel inside slice in red
        if plot_voxel_in_slice:
            x_y_voxel = [ML_position, AP_position, CC_position]
            x_y_voxel.remove(slice_nr)  # Only retain 2 necessary positions (x and y) from all positions
            ax.scatter(x_y_voxel[0], x_y_voxel[1], color = voxel_color)
        
    # 2. Plot voxel over time
    axTime.plot(voxel_over_time)
    axTime.set_title('BOLD signal inside voxel over time', fontsize = 18)
    axTime.set_xlabel('Timepoint', fontsize = 18)
    axTime.set_ylabel('BOLD signal', fontsize = 18)
    plt.show()
    

def _get_slice(image, orientation, slice_nr):
    """
    Get preferred slice from 3D or 4D nifti image
    Indexing: [Medio-lateral, Antero-posterior, Cranio-caudal, Time]
    
    :param image: 3D/4D numpy array with grey values
    :param orientation: str, choose from ["sagittal", "frontal", "axial"]
    :param slice_nr: int, desired slice number
    :output: Slice: np array, x_lab: xlabel, y_lab: ylabel
    """
    
    # Get desired slice and the according x and y labels
    if orientation == 'sagittal':
        # Medio-Lateral: slice_nr, Antero-posterior: all voxels, Cranio-caudal: all voxels, Time: timepoint
        Slice = image[slice_nr,:,:]
        y_lab = 'Cranio-caudal'
        x_lab = 'Antero-posterior'
    elif orientation == 'frontal':
        # Medio-Lateral: all voxels, Antero-posterior: slice_nr, Cranio-caudal: all_voxels, Time: timepoint
        Slice = image[:,slice_nr,:] 
        y_lab = 'Cranio-caudal'
        x_lab = 'Medio-lateral'
    elif orientation == 'axial':
        # Medio-Lateral: all voxels, Antero-posterior: all voxels, Cranio-caudal: slice_nr, Time: timepoint
        Slice = image[:,:,slice_nr]
        y_lab = 'Antero-posterior'
        x_lab = 'Medio-lateral'

    return Slice, x_lab, y_lab
