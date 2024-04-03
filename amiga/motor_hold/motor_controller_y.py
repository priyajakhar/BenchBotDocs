from __future__ import annotations

import asyncio
from pathlib import Path
import time
from from_root import from_root, from_here
import numpy as np

from farm_ng.canbus.canbus_pb2 import Twist2d
from farm_ng.core.event_client import EventClient
from farm_ng.core.event_service_pb2 import EventServiceConfig
from farm_ng.core.events_file_reader import proto_from_json_file

# linear velocity in m/s and angular velocity is in rad/s
LINEAR_VELOCITY = 0.1
VELOCITY_INCREMENT = 0.05
ANGULAR_VELOCITY = 0.05

class MotorControllerY():
    def __init__(self, file_path=from_root("brain_api/common/service_config.json")):
        service_config_path = Path(file_path)
        self.twist = Twist2d()
        config: EventServiceConfig = proto_from_json_file(service_config_path, EventServiceConfig())
        self.client: EventClient = EventClient(config)

    async def set_motor_velocity(self, speed) -> None:
        self.twist.linear_velocity_x = speed
        await self.client.request_reply("/twist", self.twist)
        await asyncio.sleep(0.05)

    async def move_y(self, distance) -> None:
        distance_in_m = abs(distance/100)
        direction_flag = True
        if distance < 0:
            direction_flag = False
        velocity_track = get_velocity_graph(distance_in_m, LINEAR_VELOCITY, VELOCITY_INCREMENT, direction_flag)
        for v in velocity_track:
           await self.set_motor_velocity(v)


'''
create an array that contains values from 0 to 'max' with increments defined by 'step'
'''
def get_up_slope(step, max):
    arr = np.arange(max, 0, -step)
    flipped = np.flip(arr)
    return np.around(flipped, decimals=2)


'''
create an array containing velocity values needed to traverse a certain distance
arguments:  dist_m -> total distance to be covered (in m)
            max_v -> maximum velocity
            step_v -> increments in velocity
            direction -> direction of movement, either positive(forward) or negative(backward)
'''
def get_velocity_graph(dist_m, max_v, step_v, direction):
    # create a semi-smooth upslope for velocity (acceleration)
    up_slope = get_up_slope(step_v, max_v)
    # create a velocity graph to traverse expected distance ([acceleration, constanst max velocity, deacceleration])
    ret_val = make_v_graph(dist_m, up_slope)
    # negate velocity values if direction is backwards
    if not direction:
        ret_val = [-i for i in ret_val]
    return ret_val


'''
create an array of velocity values to cover desired distance
arguments:  dist -> total distance to be covered (in m), e.g. 1
            v_slope -> array of velocity going up till max value with fix increments, defining acceleration
                        e.g. [0, 0.05, 0.1], values are in m/s
'''
def make_v_graph(dist, v_slope):
    dist_travelled = 0
    half_dist_flag = False
    vel_step_duration = 5
    time_duration = 0.05
    v_list = []
    # create velocity list till half distance
    for i in v_slope:
        if i != max(v_slope):
            # add each incremental velocity particular number of times to the graph
            for j in range(vel_step_duration):
                v_list.append(i)
                dist_travelled += i*time_duration
                # break out from loop if half distance is covered
                if dist_travelled >= (dist/2):
                    half_dist_flag = True
                    break
        else:
            # add max velocity values till half distance is covered
            while True:
                v_list.append(i)
                dist_travelled += i*time_duration
                if dist_travelled >= (dist/2):
                    half_dist_flag = True
                    break
        if half_dist_flag:    break
    # reverse the list and append as the second half, to account for deacceleration as well
    temp_list = v_list.copy()
    temp_list.reverse()
    for i in temp_list: dist_travelled += i*time_duration
    v_list.extend(temp_list)
    # print(f"Total distance moved: {np.around(dist_travelled*100, decimals=2)} cm")
    return v_list