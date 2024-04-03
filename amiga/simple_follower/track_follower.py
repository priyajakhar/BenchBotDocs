from __future__ import annotations

import asyncio
from pathlib import Path
from datetime import datetime
import time
from from_root import from_root, from_here
from path_builder import add_from_json_file, PathBuilder

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
    def __init__(self, config_file="brain_api/common/service_config.json", build_new_path=False, total_path_length=0, waypoint_gap=0):
        config_file_path = from_root(config_file)
        # Setup EventClients defined by the service file
        expected_configs = ["track_follower", "filter"]
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

    # Request to pause the track follower
    async def pause_track(self) -> None:
        await self.clients["track_follower"].request_reply("/pause", Empty())

    # Request to resume the track follower
    async def resume_track(self) -> None:
        await self.clients["track_follower"].request_reply("/resume", Empty())

    # stream the track_follower state
    async def stream_status(self) -> None:
        await asyncio.sleep(1.0)
        message: TrackFollowerState
        start_time = time.time()
        distance_gap = 0.3
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
                    
                # if message.status.track_status == 'TRACK_PAUSED':
                if track_paused:
                    if time.time()-start_time > 2:
                        temp_var = message.status.track_status
                        print(temp_var, type(temp_var))
                        await self.resume_track()
                        print("Resume at:", time.time())
                        track_paused = False
                        
                        # TrackStatusEnum.TRACK_PAUSED
                
                l_file.write(str(message))
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
        await self.set_track(track)
        # Start following the track
        await self.start()

    async def run_track_service(self, track_file: str) -> None:
        # Start the asyncio tasks
        tasks: list[asyncio.Task] = [
            asyncio.create_task(self.start_track(track_file)),
            asyncio.create_task(self.stream_status()),
        ]
        await asyncio.gather(*tasks)

    def run(self, track_file: str) -> None:
        # Create the asyncio event loop and run the track function
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.run_track_service(track_file))
