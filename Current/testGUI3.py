class AcquisitionPage(QWidget):
    

    def capture_image(self, img_no=0):
        t = str(int(time.time()))
        os.startfile(CAM_PATH)
        save_oak_image(t)
        # time.sleep(8)
        threading.Thread(target=self.file_rename(t, img_no)).start()
    
    def file_rename(self, timestamp, img_num):
        time.sleep(4)
        for file_name in os.listdir('.'):
            if file_name.startswith(STATE+'A'):
                if file_name.endswith('.JPG'):
                    self.img_taken.append(img_num-1)
                    new_name = f"{STATE}_{timestamp}.JPG"
                elif file_name.endswith('.ARW'):
                    new_name = f"{STATE}_{timestamp}.ARW"
                os.rename(file_name, new_name)
            else:
                continue

    ##### change logic for repeating rounds
    def check_miss(self, expected_count):
        filelist = [name for name in os.listdir('.') if os.path.isfile(name)]
        actual_count = len(filelist)
        missed_spots = []
        if ((expected_count*3)>actual_count):
            # if expected_count is 4, image_taken list should have 0,1,2,3
            # check for missing number to know the stop
            for x in range(0,expected_count):
                if x not in self.img_taken:
                    missed_spots.append(x)
        return missed_spots

    def acquisition_process(self):
        self.configure_machine_motion()
        total_rows = self.generate_pots_list()
        self.create_directory()
        direction = True

        for pots in total_rows:
            self.img_taken = []
            self.correct_path()
            if pots == 0 or pots == 1:
                if STOP_EXEC:
                    break
                # self.mm.moveRelativeCombined(WHEEL_MOTORS, [DISTANCE_TRAVELED, DISTANCE_TRAVELED])
                # self.mm.waitForMotionCompletion()
            else:
                # total distance between home and end sensor
                cam_stop_distance = int(HOME_TO_END_SENSOR_DISTANCE/(pots-1))
                if not direction:
                    cam_stop_distance *= -1

                # capture images in a row (original round)
                for i in range(1, pots):
                    if STOP_EXEC:
                        break
                    self.capture_image(i)
                    self.mm.moveRelative(self.camera_motor, cam_stop_distance)
                    self.mm.waitForMotionCompletion()
                if STOP_EXEC:
                    break         
                self.capture_image(pots)




                
                # check if any images were missed and if so, take action
                missed_spots = self.check_miss(pots)

                if missed_spots:
                    missed_spots.sort(reverse=True)
                    cam_stop_distance *= -1
                    direction = not direction
                    previous_stop = 0

                    for spot in missed_spots:
                        stop_factor = pots-1-spot-previous_stop
                        temp_distance = cam_stop_distance * stop_factor
                        # move camera plate to missed image spot
                        self.mm.moveRelative(self.camera_motor, temp_distance)
                        self.mm.waitForMotionCompletion()
                        self.capture_image()
                        previous_stop = stop_factor

                    # move camera plate to one of the ends
                    if(spot<(pots/2)):
                        end_distance = cam_stop_distance*spot
                    else:
                        direction = not direction
                        end_distance = -cam_stop_distance*(pots-1-spot)
                    self.mm.moveRelative(self.camera_motor, end_distance)
                    self.mm.waitForMotionCompletion()

                # move image files to respective folders
                # self.move_files()
                threading.Thread(self.move_files()).start()

                # change direction of camera plate movement
                direction = not direction
                # self.mm.moveRelativeCombined(WHEEL_MOTORS, [DISTANCE_TRAVELED, DISTANCE_TRAVELED])
                # self.mm.waitForMotionCompletion()

        if STOP_EXEC:
            self.stop()
        else:
            self.process_finished()