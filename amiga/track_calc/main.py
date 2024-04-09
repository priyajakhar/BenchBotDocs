from track_follower import MotorController_Y

track_file_name = "robot_track.json"

if __name__ == "__main__":
    path_follower = MotorController_Y()
    path_follower.run(track_file_name)

