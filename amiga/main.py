
import asyncio
from path_builder import PathBuilder
from track_follower import MotorController_Y

track_file_name = "test_track.json"

if __name__ == "__main__":
    choice = 1
    # create a new path
    if choice == 1:
        path_constructor = PathBuilder()
        asyncio.run(path_constructor.build_path(track_file_name, 4, 0.1))
    # follow existing path
    else:
        path_follower = MotorController_Y()
        path_follower.run(track_file_name)

