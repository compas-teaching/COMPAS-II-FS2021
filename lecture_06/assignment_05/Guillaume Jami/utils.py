"""
This module contains utility functions:
    1) Transformation functions
    2) Useful geometry functions e.g. Intersections
"""

import Rhino.Geometry as rg
import math

# ----- Coordinate System conversions -----

def rhino_to_robotbase(ref_plane, model_base):
    """
    Function that transforms a reference plane from Rhino coordinate system to the robot's base coordinate system
    TODO (Jason): maybe change this whole method? maybe not model but robot base
    
    Args:
        ref_plane: Rhino.Geometry plane object. The reference plane to transform
        model_base: Rhino.Geometry plane object. The base plane for building on. Given in robot's base coordinate system.
    
    Returns:
        ref_plane: Reference plane transformed to robot space
    """
    
    # Transform the orientation plane based on model_base coordinate system
    _matrix = rg.Transform.PlaneToPlane(rg.Plane.WorldXY,model_base)
    #_matrix = rg.Transform.PlaneToPlane(model_base,rg.Plane.WorldXY,)
    ref_plane.Transform(_matrix)
    return ref_plane

def matrix_to_axis_angle(m):
    """
    Function that transforms a 4x4 matrix to axis-angle format
    referenced from Martin Baker's www.euclideanspace.com
    
    Args:
        m: Rhino.Geometry Transform structure  - 4x4 matrix
    
    Returns:
        axis: Rhino.Geometry Vector3d object - axis-angle notation
    """
    
    epsilon = 0.01
    epsilon2 = 0.01
    
    if (math.fabs(m.M01 - m.M10) < epsilon) & (math.fabs(m.M02 - m.M20) < epsilon) & (math.fabs(m.M12 - m.M21) < epsilon):
    #singularity found
    #first check for identity matrix which must have +1 for all terms
    #in leading diagonal and zero in other terms
        if (math.fabs(m.M01 + m.M10) < epsilon2) & (math.fabs(m.M02 + m.M20) < epsilon2) & (math.fabs(m.M12 + m.M21) < epsilon2) & (math.fabs(m.M00 + m.M11 + m.M22 - 3) < epsilon2):
            #this singularity is identity matrix so angle = 0   make zero angle, arbitrary axis
            angle = 0
            x = 1
            y = z = 0
        else:
            # otherwise this singularity is angle = 180
            angle = math.pi;
            xx = (m.M00 + 1) / 2
            yy = (m.M11 + 1) / 2
            zz = (m.M22 + 1) / 2
            xy = (m.M01 + m.M10) / 4
            xz = (m.M02 + m.M20) / 4
            yz = (m.M12 + m.M21) / 4
            if ((xx > yy) & (xx > zz)):
                # m.M00 is the largest diagonal term
                if (xx < epsilon):
                    x = 0
                    y = z = 0.7071
                else:
                    x = math.sqrt(xx)
                    y = xy / x
                    z = xz / x
            elif (yy > zz): 
                # m.M11 is the largest diagonal term
                if (yy < epsilon):
                    x = z = 0.7071
                    y = 0
                else: 
                    y = math.sqrt(yy)
                    x = xy / y
                    z = yz / y
            else: 
                # m.M22 is the largest diagonal term so base result on this
                if (zz < epsilon):
                    x = y = 0.7071
                    z = 0
                else:
                    z = math.sqrt(zz)
                    x = xz / z
                    y = yz / z
    else:
        s = math.sqrt((m.M21 - m.M12) * (m.M21 - m.M12)+ (m.M02 - m.M20) * (m.M02 - m.M20)+ (m.M10 - m.M01) * (m.M10 - m.M01)); # used to normalise
        if (math.fabs(s) < 0.001):
            #prevent divide by zero, should not happen if matrix is orthogonal and should be
            s = 1
        angle = math.acos((m.M00 + m.M11 + m.M22 - 1) / 2)
        x = (m.M21 - m.M12) / s
        y = (m.M02 - m.M20) / s
        z = (m.M10 - m.M01) / s
    angleRad = angle
    axis = rg.Vector3d(x,y,z)
    axis = axis*angleRad
    
    return axis

def matrix_to_euler(m):
    """
    Gets the Euler rotation angles from a transformation matrix
    from http://forums.codeguru.com/archive/index.php/t-329530.html
    
    Args:
        m = Transform object
    Returns:
        tuple of euler angles in radians
    """
    
    rotz = math.atan2(m.M10, m.M00)
    roty = -math.asin(m.M20)
    rotx = math.atan2(m.M21, m.M22)
    return (rotx, roty, rotz)

# ----- Matrix related helper functions

def dh_matrix((d, theta, a, alpha)):
    """
    This function creates the Denavit Hartenberg transformation matrix between adjacent frames
    
    Arguments:
        d: Joint distance. in mm
        theta: joint angle. in radians
        a: link length. in mm
        alpha: twist angle. in radians
    
    Returns:
        m: Denavit Hartenberg transformation matrix
    """
    
    _matrix = [
    (math.cos(theta), -math.sin(theta) * math.cos(alpha),math.sin(theta) * math.sin(alpha),a * math.cos(theta)),
    (math.sin(theta), math.cos(theta) * math.cos(alpha), -math.cos(theta) * math.sin(alpha), a * math.sin(theta)),
    (0, math.sin(alpha),math.cos(alpha),d),
    (0,0,0,1)
    ]
    
    m = rg.Transform()
    for i in range(4):
        for j in range(4):
            m[i,j] = _matrix[i][j]
            
    return m

def concatenate_matrices(matrices):
    """
    This function creates a concatenated matrix from a list of matrices
    
    Arguments:
        matrices: A list of tranformation matrices
    
    Returns:
        _transform: Concatenated matrix
    """
    _transform = matrices[0]
    for i in range(1,len(matrices)):
        _transform *= matrices[i]
    return _transform


# ----- Miscellaneous geometry helper functions
def signed_angle(v1,v2,v_normal):
    """
    This function gets the angle between 2 vectors -pi < theta< pi
    
    Arguments:
        v1: Vector3d. First unitized vector
        v2: Vector3d. Second unitized vector
        v_normal: Vector3d. Normal to 2 vectors that determines what is positive/negative
    
    Returns:
        theta: float. signed angle between -pi and pi
    """
    # from 0 to pi
    c = rg.Vector3d.Multiply(v1,v2)
    n = rg.Vector3d.CrossProduct(v1,v2)
    s= n.Length
    
    theta  = math.atan2(s,c)
    
    if (rg.Vector3d.Multiply(n, v_normal) < 0):
        theta *= -1
    return theta

def cir_cir_intersection(cir1,cir2):
    """
    Funtion that returns the intersection points between two circles
    
    Arguments:
        1) cir1: First circle
        2) cir2: Second Circle
    
    Returns:
        xpts: list of 2 Point3d objectts
        
    Note that there is no error checking
    """
    r1 = cir1.Radius
    r2 = cir2.Radius
    d = cir1.Center.DistanceTo(cir2.Center)
    
    a = (r1 **2 - r2**2 + d**2)/(2*d)
    h = math.sqrt(r1 **2 - a **2 )
    
    v_c1 = rg.Vector3d(cir1.Center)
    v_c2 = rg.Vector3d(cir2.Center)
    
    v_c1c2 = v_c2 - v_c1
    v_c1c2.Unitize()
    v_c1c2 *= a
    
    v_pt0 = v_c1 + v_c1c2
    
    v_pt0ptX = rg.Vector3d.CrossProduct(cir1.Normal,v_c1c2)
    v_pt0ptX.Unitize()
    v_pt0ptX *= h
    
    xpt1 = rg.Point3d(v_pt0 + v_pt0ptX)
    v_pt0ptX.Reverse()
    xpt2 = rg.Point3d(v_pt0 + v_pt0ptX)

    return [xpt1,xpt2]
    
def check_arguments(function):
    def decorated(*args):
        if None in args:
            raise TypeError("Invalid Argument")
        return function(*args)
    return decorated
