from PIL import Image,ImageDraw
import numpy as np



def grayScaleConvert(img:Image):
    """
        convert Image Gray Scale
    """
    temp =img.convert("L")
    return temp
    
def imageToColumnVector(img:Image):
    """
        Convert Image to A column Vector
    """
    image_array = np.array(grayScaleConvert(img))
    image_array =image_array/255
    vec =image_array.reshape(image_array.size,1)
    return vec

def normalizeImageVector(img:np.array):
    """
    Normalize Image Vector
    """
    return img/255

def circular_mask(size, center, radius):
    """Create a circular mask with 1 inside the circle and 0 outside."""
    height, width = size
    Y, X = np.ogrid[:height, :width]
    dist_from_center = np.sqrt((X - center[0])**2 + (Y - center[1])**2)
    mask = dist_from_center <= radius
    return mask


def apply_circular_mask(image, center, radius,retimage=False):
    image_array = np.array(grayScaleConvert(image))  # Use grayscale conversion
    
    normalized_array = normalizeImageVector(image_array)
    
    mask = circular_mask(image_array.shape, center, radius)
    
    result_array = np.ones_like(normalized_array)  # Start with all ones
    result_array[mask] =  normalized_array[mask]  # Invert the values within the mask
    
    if retimage==True:
        result_image = Image.fromarray((result_array * 255).astype(np.uint8))  # Convert back to 8-bit image
        return result_image
    else:
        return result_array.reshape(result_array.size,1)

def maskCenterCircle(img:Image):
    (h,w)=img.size
    return apply_circular_mask(img,(h/2,w/2),min(h/2,w/2),True)

def EmptyCanvas(size):
    """
    A Function that create an empty canvas (Gray sacle White)

    :param size: The size of the image(canvas).

    Returns:
        Image
    """
    width, height = size 
    image = Image.new("L",(width,height),color="white")
    return image




def ddx(f,t,R):
    return R*np.cos(2*np.pi*t/f)
def ddy(f,t,R):
    return R*np.sin(2*np.pi*t/f)


def Line(n:int,R:float,phi1:int,phi2:int,img:Image)->Image:
    """
    A Function that Create an Image with a single Line

    :param n: no of Pins.
    :param R: Radious of the circle.
    :param phi1: Point for first pin for a line.
    :param phi2: Pont for second pin for a line.
    :param img: an Image which is useed to find size of canvas.

    
    Returns:
        Image : Image with a line
    """
    canvas=EmptyCanvas(img.size)
    draw = ImageDraw.Draw(canvas)
    centerx,centery= canvas.size[0]/2,canvas.size[1]/2
    start_point = (centerx + ddx(n,phi1,R),centery +ddy(n,phi1,R))
    end_point = (centerx + ddx(n,phi2,R),centery +ddy(n,phi2,R))
    line_color=100
    line_width = 10
    draw.line([start_point, end_point], fill=line_color, width=line_width)
    return canvas

    
def LineInCircle(n,phi1,phi2,img:Image):
    imgS = img.size
    R = min(imgS[0]/2,imgS[1]/2)
    return Line(n,R,phi1,phi2,img)