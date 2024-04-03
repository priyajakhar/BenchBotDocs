
import asyncio
import time
from pathlib import Path
from path_builder import PathBuilder
from track_follower import MotorController_Y

track_file_name = "track.json"

if __name__ == "__main__":
    choice = 1
    if choice == 1:
        path_constructor = PathBuilder()
        asyncio.run(path_constructor.build_path(track_file_name, 4, 0.1))
    else:
        # path_follower = MotorController_Y(total_path_length=2, waypoint_gap=0.05, build_new_path=True)
        path_follower = MotorController_Y()
        path_follower.run(track_file_name)

