from __future__ import annotations

from math import copysign
from from_root import from_root

from farm_ng.core.event_client import EventClient
from farm_ng.core.event_service_pb2 import EventServiceConfigList
from farm_ng.core.events_file_reader import proto_from_json_file
from farm_ng.core.events_file_writer import proto_to_json_file
from farm_ng.filter.filter_pb2 import FilterState
from farm_ng.track.track_pb2 import Track
from farm_ng_core_pybind import Isometry3F64
from farm_ng_core_pybind import Pose3F64
from farm_ng_core_pybind import Rotation3F64
from google.protobuf.empty_pb2 import Empty


def add_from_json_file(expected_list: list, json_file_path: str) -> dict[str, EventClient]:
    config_list = proto_from_json_file(json_file_path, EventServiceConfigList())
    client_list: dict[str, EventClient] = {}
    for config in config_list.configs:
        if config.name in expected_list:
            client_list[config.name] = EventClient(config)
    for config in expected_list:
        if config not in client_list:
            raise RuntimeError(f"No {config} service config in {json_file_path}")
    return client_list


''' Class for creating a straight path'''
class PathBuilder():
    def __init__(self, config_file="amiga/track_config.json"):
        config_file_path = from_root(config_file)
        # Setup EventClients defined by the service file
        expected_configs = ["filter"]
        self.clients = add_from_json_file(expected_configs, config_file_path)
        
    # Get the current pose of the robot in the world frame, from the filter service
    async def get_pose(self) -> Pose3F64:
        state: FilterState = await self.clients["filter"].request_reply("/get_state", Empty(), decode=True)
        return Pose3F64.from_proto(state.pose)

    # distance and spacing are in meters
    def create_straight_path(self, previous_pose: Pose3F64, next_frame_b: str, distance: float, spacing: float = 0.1) -> list[Pose3F64]:
        track_poses: list[Pose3F64] = [previous_pose]
        counter: int = 0
        remaining_distance: float = distance

        while abs(remaining_distance) > 0.01:
            # Compute the distance of the next segment
            segment_distance: float = copysign(min(abs(remaining_distance), spacing), distance)
            # Compute the next pose
            straight_segment: Pose3F64 = Pose3F64(
                a_from_b=Isometry3F64([segment_distance, 0, 0], Rotation3F64.Rz(0)),
                frame_a=track_poses[-1].frame_b,
                frame_b=f"{next_frame_b}_{counter}",
            )
            track_poses.append(track_poses[-1] * straight_segment)
            counter += 1
            remaining_distance -= segment_distance

        # Rename the last pose to the desired name
        track_poses[-1].frame_b = next_frame_b
        return track_poses
    
    # Pack the track waypoints into a Track proto message
    def format_track(self, track_waypoints: list[Pose3F64]) -> Track:
        return Track(waypoints=[pose.to_proto() for pose in track_waypoints])
    
    # Build a straight path track, from the current pose of the robot
    async def build_path(self, track_file: str, track_length: float, track_resolution: float) -> Track:
        # get current pose of the robot in the world frame from the state estimation filter
        world_pose_robot: Pose3F64 = await self.get_pose()
        # list to store the track waypoints
        track_waypoints: list[Pose3F64] = []
        # Add current pose of the robot as the first goal
        world_pose_goal0: Pose3F64 = world_pose_robot * Pose3F64(a_from_b=Isometry3F64(), frame_a="robot", frame_b="goal_init")
        track_waypoints.append(world_pose_goal0)
        # creat a straight path given the length and the space between waypoints
        track_waypoints.extend(self.create_straight_path(track_waypoints[-1], "goal", track_length, track_resolution))

        # Return the list of waypoints as a Track proto message and save the track in json file
        constructed_track: Track = self.format_track(track_waypoints)
        output_dir = from_root("amiga")
        if not proto_to_json_file(track_file, constructed_track):
            raise RuntimeError(f"Failed to write Track to {output_dir}")
        print(f"Saved track of length {len(constructed_track.waypoints)} to {output_dir}")
        return constructed_track