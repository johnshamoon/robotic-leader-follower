from follower import Follower

follower = Follower()

def seek():
    #tag_data = follower.detect()
    turn = follower.turn()

    if follower.detect() == False:
        print('Detect False')
        follower._speed = follower.LEADER_MAX_SPEED
        turn = turn + 35
    else:
        print("Detect True")
        #print(tag_data)

def main():
    while True:
        seek()

if __name__ == '__main__':
    main()