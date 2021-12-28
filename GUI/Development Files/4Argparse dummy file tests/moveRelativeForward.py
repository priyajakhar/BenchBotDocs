import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-d')
args = parser.parse_args()

print("move forward relative")
print("Distance to move is " + args.d)