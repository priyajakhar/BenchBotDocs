from __future__ import annotations

import asyncio
from pathlib import Path
from datetime import datetime
import time
import signal
from from_root import from_root, from_here
from path_builder import add_from_json_file

import json
import numpy as np
from scipy.spatial.distance import cdist
from farm_ng_core_pybind import Pose3F64

from farm_ng.core.event_service_pb2 import SubscribeRequest
from farm_ng.core.events_file_reader import proto_from_json_file
from farm_ng.core.uri_pb2 import Uri
from farm_ng.track.track_pb2 import Track
from farm_ng.track.track_pb2 import TrackFollowerState
from farm_ng.track.track_pb2 import TrackFollowRequest
from google.protobuf.empty_pb2 import Empty


log_dir = from_here("logs")
Path(log_dir).mkdir(parents=True, exist_ok=True)
curr_date = datetime.now().strftime('%m-%d_%H:%M')
logfile = f"{curr_date}_track.log"          


class MotorController_Y():
    def __init__(self, config_file="amiga/track_calc/track_config.json", build_new_path=False, total_path_length=0, waypoint_gap=0):
        config_file_path = from_root(config_file)
        # Setup EventClients defined by the service file
        expected_configs = ["track_follower"]
        self.clients = add_from_json_file(expected_configs, config_file_path)
        if build_new_path:
            self.path_builder = PathBuilder()
            self.total_path_length = total_path_length
            self.waypoint_gap = waypoint_gap

    ''' Functions related to following the path'''
    # Set the track of the track_follower
    async def set_track(self, track: Track) -> None:
        await self.clients["track_follower"].request_reply("/set_track", TrackFollowRequest(track=track))

    # Request to start following the track
    async def start(self) -> None:
        await self.clients["track_follower"].request_reply("/start", Empty())
        print('Follower started')

    # Request to pause the track follower
    async def pause_track(self) -> None:
        await self.clients["track_follower"].request_reply("/pause", Empty())

    # Request to resume the track follower
    async def resume_track(self) -> None:
        await self.clients["track_follower"].request_reply("/resume", Empty())
    
    # Request to stop the track follower
    async def stop_track(self) -> None:
        try:
            await self.clients["track_follower"].request_reply("/cancel", Empty())
        except:
            pass

    # stream the track_follower state
    async def stream_status(self) -> None:
        await asyncio.sleep(1.0)
        message: TrackFollowerState
        start_time = time.time()
        distance_gap = 0.5
        last_distance_mark = None
        track_paused = False
        with open(logfile, "a") as l_file:
            async for _, message in self.clients["track_follower"].subscribe(SubscribeRequest(uri=Uri(path="/state"), every_n=1)):
                track_progress = message.progress
                if not last_distance_mark:
                    last_distance_mark = track_progress.distance_total
                    print("Distance Mark:", last_distance_mark)
                if last_distance_mark-track_progress.distance_remaining >= distance_gap:
                    await self.pause_track()
                    last_distance_mark = track_progress.distance_remaining
                    print("Pause at:", last_distance_mark)
                    start_time = time.time()
                    track_paused = True
                    
                if track_paused:
                    if time.time()-start_time > 5:
                        await self.resume_track()
                        print("Resume at:", time.time())
                        track_paused = False

                # if the track is completed
                if message.status.track_status == 5:
                    print("COMPLETED!")
                    break
                # if there is issue with following the track
                if message.status.track_status == 7:
                    print("ABORTED!")
                    break
                # l_file.write(str(message))
                # print("###################\n", message.progress)

    # Start the trackfollower service to have the robot following the path
    async def start_track(self, track_file: str) -> None:
        if hasattr(self, "path_builder"):
            # Build the track and package in a Track proto message
            track: Track = await self.path_builder.build_path(track_file, self.total_path_length, self.waypoint_gap)
        else:
            # load track from json file
            track: Track = proto_from_json_file(track_file, Track())
        # Send the track to the track_follower
        # await self.set_track(track)
        # Start following the track
        # await self.start()
        self.poses = get_poses(track)

        # await self.start()
        # for target_pose in self.poses:
        #     await self.clients["track_follower"].request_reply("/go_to_goal", target_pose)
        
        # await self.clients["track_follower"].request_reply("/set_track", TrackFollowRequest(track=track))

    async def run_track_service(self, track_file: str) -> None:
        try:
            # Start the asyncio tasks
            tasks: list[asyncio.Task] = [
                asyncio.create_task(self.start_track(track_file)),
                # asyncio.create_task(self.stream_status()),
            ]
            await asyncio.gather(*tasks)
        finally:
            ("Stop track_follower")
            await self.stop_track()

    def run(self, track_file: str) -> None:
        # Create the asyncio event loop and run the track function
        loop = asyncio.get_event_loop()
        # handle KeyboardInterrupt
        loop.add_signal_handler(signal.SIGINT, self.signal_handler, loop)
        try:
            loop.run_until_complete(self.run_track_service(track_file))
        finally:
            # loop.run_until_complete(self.stop_track())
            loop.close()
    
    def signal_handler(self, loop):
        asyncio.ensure_future(self.stop_track(), loop=loop)


def get_poses(track: Track) -> list[Pose3F64]:
    complete_track = track.waypoints
    # print(len(complete_track), type(complete_track))
    # for p_point in complete_track:
    #     print(p_point.a_from_b.translation)
    # return

    sub_track: list[Pose3F64] = [previous_pose]
    previous_pose = None
    track_gap = 0.5
    for waypoint in complete_track:
        if not previous_pose:
            sub_track.append(waypoint)
            previous_pose = waypoint
        else:
            p1 = [ [ previous_pose.a_from_b.translation.x, previous_pose.a_from_b.translation.y ] ]
            p2 = [ [ waypoint.a_from_b.translation.x,    waypoint.a_from_b.translation.y ] ]
            dist = round(cdist(p1, p2, 'euclidean')[0][0], 2)
            if dist >= track_gap:
                sub_track.append(waypoint)
                previous_pose = waypoint

    print(len(sub_track))
    return sub_track

