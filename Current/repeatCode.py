expected_count = 6
img_taken = [0,1,2,3,4,5]
cam_stop_distance = 1000/(expected_count-1)
 
def check_miss(actual_count=5):
    missed_spots = []
    if(actual_count<expected_count):
        for x in range(0,expected_count):
            if x not in img_taken:
                missed_spots.append(x)
    return missed_spots
        
missed_img = check_miss(6)
print('Missed images are ', missed_img)

if missed_img:
    missed_img.sort(reverse=True)
    cam_stop_distance *= -1
    previous_stop = 0

    for spot in missed_img:
        stop_factor = expected_count-1-spot-previous_stop
        temp_distance = cam_stop_distance * stop_factor
        print('Move bot by ', temp_distance)
        previous_stop = stop_factor
        
    print(spot)
    
    if(spot<(expected_count/2)):
        print('Move bot in same dir to end by', cam_stop_distance*spot)
    else:
        print('Move bot in oppo dir to end by', -cam_stop_distance*(expected_count-1-spot))
