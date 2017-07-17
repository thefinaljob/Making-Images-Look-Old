from __future__ import print_function
import os
from os import path
import PIL
import PIL.ImageDraw
from PIL import Image, ImageEnhance, ImageFilter


global directory 

print(os.getcwd())
#defines directory which contains the images to be modified, files must be in a directory called Project_Files
directory = os.getcwd()+"/Project_Files"

def make_old(filename):
    
    '''This function makes the image processed look old by 
    pasting a brown mask on top of it, changing the contrast by certain metrics,
    and then pasting a grainy texture on top of it. After this is done, the image is
    cropped and stored in another variable. It then creates a solid border by 
    making a large rectangle, and then the cropped image is pasted upon it. This creates the effect
    of an old style photo. 
    '''
    
    texture = 'Gray_Texture.png'
    imageObject = filename
    
    #opens the texture and image files to be modified
    imageObject = Image.open(filename)
    Texture_img = PIL.Image.open(texture)
    
    width, height = imageObject.size #obtains size of the image in directory
    Texture_img.convert("RGBA") #converts into RGBA for transparency
    Texture_img.putalpha(50) #adds opacity to 
    
    
    enhancer = ImageEnhance.Color(imageObject)
    imageObject = enhancer.enhance(0.0) #lowers brightness, color, contrast etc.
    
    width, height = imageObject.size #obtains size of image being processed
    
    position = (int(0.05*width), int(0.05*height), int(0.95*width), int(0.95*height)) 
    #creates the size of the image to be cropped
    
    width2, height2 = Texture_img.size
    
    position2 = (int(0.05*width2), int(0.05*height2), int(0.95*width2), int(0.95*height2))
    #creates the size of the texture to be cropped
    
    #Image.new(mode, size, color) = image
    brown_mask = PIL.Image.new("RGBA", imageObject.size, (223, 163, 102, 95)) #specifies the color and size of brown mask
    Texture_img = Texture_img.crop(position2) #crops texture image to fit the image processed
    imageObject.paste(brown_mask, (0,0), brown_mask) #makes the image brown, by pasting the mask
    imageObject.paste(Texture_img, (0,0), Texture_img) #adds the texture on top of the image
    
      
    newImage = imageObject.crop(position) #crops the image being processed
    enhancer = ImageEnhance.Contrast(newImage) #increases contrast of the image being processed
    newImage = enhancer.enhance(0.8)
    
    enhancer = ImageEnhance.Brightness(imageObject) 
    imageObject = enhancer.enhance(0.95)
    
    border = PIL.Image.new("RGBA", imageObject.size, (125, 105, 63, 250)) #creates solid brown border
    
    imageObject.paste(border) #pastes solid border on image processed
    imageObject.paste(newImage, position) #pastes the cropped image on top of the solid border (it's a brown rectangle)
    
    return imageObject
    
def get_images(directory):
    """ Returns PIL.Image objects for all the images in directory.
    
    If directory is not specified, uses current directory.
    Returns a 2-tuple containing 
    a list with a  PIL.Image object for each image file in root_directory, and
    a list with a string filename for each image file in root_directory
    """
    
    if directory == None:
        directory = os.getcwd() # Use working directory if unspecified
        
    image_list = [] # Initialize aggregaotrs
    file_list = []
    
    directory_list = os.listdir(directory) # Get list of files
    for entry in directory_list:
        absolute_filename = os.path.join(directory, entry)
        try:
            image = PIL.Image.open(absolute_filename)
            file_list += [entry]
            image_list += [image]
        except IOError:
            pass # do nothing with errors trying to open non-images
    return image_list, file_list

def make_all_images_old(directory):
    """ Saves a modfied version of each image in directory.
    
    Uses current directory if no directory is specified. 
    Places images in subdirectory 'modified', creating it if it does not exist.
    New image files are of type PNG and have transparent rounded corners.
    """
    
    if directory == None:
        directory = os.getcwd() # Use working directory if unspecified
        
    # Create a new directory 'modified'
    new_directory = os.path.join(directory, 'modified')
    try:
        os.mkdir(new_directory)
    except OSError:
        pass # if the directory already exists, proceed  
    
    #load all the image
    image_list, file_list = get_images(directory)  

    #go through the images and save modified versions
    for n in range(len(image_list)):
        # Parse the filename
        filename, filetype = file_list[n].split('.')
        needed_filename = file_list[n]
        # For each item in the directory, make them look old
        new_image = make_old(directory+"/"+needed_filename)
        #save the altered image, suing PNG to retain transparency
        new_image_filename = os.path.join(new_directory, filename +'newly_changed' + '.png')
        new_image.save(new_image_filename)  
        
make_all_images_old(directory)


