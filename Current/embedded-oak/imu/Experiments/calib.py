import numpy as np
from scipy import spatial

'''original lawn data parameters'''
# Center = (3.124173641204834, 10.210946083068848)
# Axes = (43.39207458496094, 47.614315032958984)
# Angle = 143.2361297607422

'''new lawn data 10/26'''
# Center = (6.346516132354736, 2.1074562072753906)
# Axes = (46.81740951538086, 53.1333122253418)
# Angle = 19.02606773376465

'''new lawn data with table 10/26'''
# Center = (-7.221834659576416, 14.527664184570312)
# Axes = (29.25990867614746, 47.920196533203125)
# Angle = 86.08250427246094

'''new lawn data with table 10/27'''
# Center = (-5.98426628112793, 12.52568244934082)
# Axes = (30.050765991210938, 47.91799545288086)
# Angle = 81.19168090820312

'''new lawn data with table part 2 10/27'''
# Center = (23.700437545776367, 17.831777572631836)
# Axes = (30.24058723449707, 48.753021240234375)
# Angle = 86.02130889892578

''' data 10/31'''
# Center = (14.9385, 7.5867, 64.4245)
# Axes = (18.85420799255371, 21.232511520385742)
# Angle = 94.03590393066406
# plane_angle = 67.0684

''' data 11/03 '''
Center = (-16.3694, 24.4040, -29.3979)
Axes = (51.355064392089844, 56.90375518798828)
Angle = 73.76220703125
plane_angle = 38.9686

theta = np.linspace(0, 2*np.pi, 500)
l = Axes[1]/2
x = l * np.cos(theta)
y = l * np.sin(theta)
circle_points = np.column_stack((x,y))

def change_center(dx, dy, dz, center):
    tx = dx - center[0]
    ty = dy - center[1]
    tz = dz - center[2]
    return tx, ty, tz

def rotate_ellipse(dx, dy, dz, angle):
    theta = np.radians(angle)
    cos_theta, sin_theta = round(np.cos(theta),3), round(np.sin(theta),3)
    rotation_matrix = np.array([
        [cos_theta, -sin_theta, 0],
        [sin_theta, cos_theta, 0],
        [0, 0, 1]
    ])
    data = np.column_stack((dx, dy, dz))
    n = 1
    # n = len(dx)
    for i in range(n):
        data[i] = np.dot(rotation_matrix, data[i].T).T
    return data[:,0], data[:,1], data[:,2]

def flat_ellipse(dx, dy, dz, angle):
    theta = np.radians(angle)
    cos_theta, sin_theta = round(np.cos(theta),3), round(np.sin(theta),3)
    rotation_matrix = np.array([
        [1, 0, 0],
        [0, cos_theta, -sin_theta],
        [0, sin_theta, cos_theta]
    ])
    data = np.column_stack((dx, dy, dz))
    n = len(dx)
    for i in range(n):
        data[i] = np.dot(rotation_matrix, data[i].T).T
    return data[:,0], data[:,1], data[:,2]

def to_circle(ex, ey, axes):
    major_axis, minor_axis = axes
    # scale_factor = major_axis / minor_axis
    # normalized_x = ex / scale_factor
    # normalized_y = ey
    norm = 48*2
    scale_factor1 = major_axis / norm
    scale_factor2 = minor_axis / norm
    normalized_x = ex / scale_factor1
    normalized_y = ey / scale_factor2
    return normalized_x, normalized_y

def find_closest(cx, cy):
    pt = [cx, cy]
    distance, index = spatial.KDTree(circle_points).query(pt)
    new_pt = circle_points[index]
    return new_pt


def transform_data(mx, my, mz):
    mx, my, mz = change_center(mx, my, mz, Center)
    mx, my, mz = rotate_ellipse(mx, my, mz, -Angle)
    mx, my, mz = flat_ellipse(mx, my, mz, plane_angle)
    circ_x, circ_y = to_circle(mx, my, Axes)
    new_x, new_y = find_closest(circ_x[0], circ_y[0])

    return new_x, new_y


''' functions from class file '''
import math

    def get_imu_reading(self):    
        # try:
        imuPackets = self.nodes['imu'].packets
        for imuPacket in imuPackets:
            mFvalues = imuPacket.magneticField
            aValues = imuPacket.acceleroMeter
            imu_data = self.process_data(mFvalues, aValues)
            # print(imu_data)
            return imu_data                
        # except:
        #     self.stop_camera()
    
    def process_data(self, mag, acc):
        # mx, my, mz = mag[0], mag[1], mag[2]
        mx, my, mz = mag.x, mag.y, mag.z
        # data_arr = [acc.x, acc.y, acc.z]

        '''New calibration process'''
        caliba = False
        if caliba==True:
            data_arr = [mx,my,mz]
            print(data_arr)
        else:
            mx, my = calib.transform_data(mx,my,mz)
            heading = calc_heading(my, mx, self.Declination)
            print(heading)
            data_arr = [my, mx, round(heading, 2)]

        '''After calibration is done'''
        # ax, ay, az = acc.x, acc.y, acc.z
        # mx, my = tilt_comp(mx, my, mz, ax, ay, az)
        # mx, my, mz = apply_iron_offsets([mx, my, mz], self.Soffset, self.Hoffset)

        return data_arr


def apply_iron_offsets(magneto, s_offset, h_offset):
    # apply hard-iron offset
    hard_iron, soft_iron = [], []
    for i in range(3):
        hard_iron.append(magneto[i]-h_offset[i])
    # print(hard_iron)
    # apply soft-iron offset
    for i in range(3):
        res = 0
        for j in range(3):
            res += s_offset[i][j] * hard_iron[j]
        soft_iron.append(res)
    # print(soft_iron)
    return soft_iron

def tilt_comp(mx, my, mz, ax, ay, az):
    # Calculate pitch and roll
    pitch = math.atan2(ax, math.sqrt(ay**2 + az**2))
    roll = math.atan2(ay, math.sqrt(ax**2 + az**2))
    # Tilt compensate magnetometer readings
    mag_x = mx * math.cos(pitch) + mz * math.sin(pitch)
    mag_y = mx * math.sin(roll) * math.sin(pitch) + my * math.cos(roll) - mz * math.sin(roll) * math.cos(pitch)

    # mag_y = my * math.cos(pitch) + mz * math.sin(pitch)
    # mag_x = my * math.sin(roll) * math.sin(pitch) + mx * math.cos(roll) - mz * math.sin(roll) * math.cos(pitch)
    return mag_x, mag_y

def calc_heading(y, x, declination):
    # Calculate heading
    heading = math.atan2(-y, x)
    # Convert heading from radians to degrees
    heading_deg = math.degrees(heading)
    # compensate for declination angle
    heading_deg += declination
    # Adjust heading to be between 0 and 360 degrees
    heading_deg +=180
    # if heading_deg<0: heading_deg += 360
    return heading_deg