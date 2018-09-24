#! /usr/bin/env python
import os
import json
import argparse
import cv2
import box

def box_detection(input_dir, output_dir):
    # Implement your logic to detect boxes here.
    # You can choose to implement it in a different class and
    # import it here.
    f_name = []
    for item in os.listdir(input_dir):
        if item[-4:] == '.jpg':
            f_name.append(item)
    for i in f_name:
        img = os.path.join(input_dir, i)
        fb = box.find_box(img)
        img, contours = fb.find_box()
        cv2.imwrite(os.path.join(output_dir, i), img)
        jd = convert_json(contours)
        with open(os.path.join(output_dir, i[:-4]+'.json'), 'w') as f:
            json.dump(jd, f)

def convert_json(l):
    d = dict(boxes=[])
    for i in l:
        cur_dict = dict(points=i)
        d['boxes'].append(cur_dict)
    jsonData = json.dumps(d)
    return jsonData

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Lets detect boxes')
    parser.add_argument('input_directory', help='Location of input images')
    parser.add_argument('output_directory', help='Location of output images')
    args = parser.parse_args()
    box_detection(input_dir=args.input_directory,
                  output_dir=args.output_directory)
