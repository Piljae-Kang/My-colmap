import subprocess
import os
import sys

while(True):
    image_path = input("please enter image path : ")
    work_space = input("please enter workspace path : ")

    if not os.path.exists(image_path):
        print("image path isn't exist")

    if not os.path.exists(work_space):
        print("workspace path isn't exist")

    if os.path.exists(image_path) and os.path.exists(work_space):
        break

print()
mode = input("please enter mode(1. automatic reconstruction, 2. customized reconstruction) : ")
print()

# colmap automatic_reconstructor process
if mode == "1":
    

    result = subprocess.run(" ".join(['colmap', 'automatic_reconstructor', '--image_path', image_path, '--workspace_path', work_space]), shell=True)

    print()
    
    if result.returncode == 0:
            print("automatic_reconstructor process completed.")
            print()
    else:
        sys.stdout.flush()
        sys.stderr.flush()
        print("Process failed with code %d." % result.returncode )  


#customized reconstruction
elif mode == "2":

    ########## feature extractor process #############

    print()
    response = input("feature extractor process (y/n) : ")

    if not response == "y":
        sys.exit(0)

    database_path = work_space + "/database.db"

    result = subprocess.run(" ".join(['colmap', 'feature_extractor', '--database_path', database_path, '--image_path', image_path]), shell=True)

    if result.returncode == 0:
            print("feature extractor process completed.")
    else:
        sys.stdout.flush()
        sys.stderr.flush()
        print("Process failed with code %d." % result.returncode )


    ########## exhaustive matcher process #############

    print()
    response = input("exhaustive matcher process (y/n) : ")

    if not response == "y":
        sys.exit(0)

    result = subprocess.run(" ".join(['colmap', 'exhaustive_matcher', '--database_path', database_path]), shell=True)

    if result.returncode == 0:
            print("feature extractor process completed.")
    else:
        sys.stdout.flush()
        sys.stderr.flush()
        print("Process failed with code %d." % result.returncode )

    ########## mapper process #############

    print()
    response = input("mapper process (y/n) : ")

    if not response == "y":
        sys.exit(0)

    output_path = work_space + "/sparse"
    
    result = subprocess.run(" ".join(['mkdir', output_path]), shell=True)

    if result.returncode == 0:
            print("mkdir /path/to/spare completed.")
    else:
        sys.stdout.flush()
        sys.stderr.flush()
        print("Process failed with code %d." % result.returncode )

    result = subprocess.run(" ".join(['colmap', 'mapper', '--database_path', database_path, '--image_path', image_path, '--output_path', output_path]), shell=True)

    if result.returncode == 0:
            print("mapper process completed.")
    else:
        sys.stdout.flush()
        sys.stderr.flush()
        print("Process failed with code %d." % result.returncode )


    ########## image undistorter process #############

    print()
    response = input("image undistorter process (y/n) : ")

    if not response == "y":
        sys.exit(0)

    output_path = work_space + "/dense"
    input_path = work_space + "/sparse/0"
    
    result = subprocess.run(" ".join(['mkdir', output_path]), shell=True)

    if result.returncode == 0:
            print("mkdir /path/to/dense completed.")
    else:
        sys.stdout.flush()
        sys.stderr.flush()
        print("Process failed with code %d." % result.returncode )

    result = subprocess.run(" ".join(['colmap', 'image_undistorter', '--image_path', image_path, '--input_path', input_path, '--output_path', output_path, '--output_type', 'COLMAP', '--max_image_size', '2000']), shell=True)

    if result.returncode == 0:
            print("image undistorter process completed.")
    else:
        sys.stdout.flush()
        sys.stderr.flush()
        print("Process failed with code %d." % result.returncode )


    ########## patch match stereo process #############

    print()
    response = input("patch match stereo process (y/n): ")

    if not response == "y":
        sys.exit(0)


    result = subprocess.run(" ".join(['colmap', 'patch_match_stereo', '--workspace_path', output_path, '--workspace_format', 'COLMAP', '--PatchMatchStereo.geom_consistency', 'true']), shell=True)

    if result.returncode == 0:
            print("patch match stereo process completed.")
    else:
        sys.stdout.flush()
        sys.stderr.flush()
        print("Process failed with code %d." % result.returncode )


    ########## stereo fusion process #############

    print()
    response = input("stereo fusion process (y/n) : ")

    if not response == "y":
        sys.exit(0)

    output_file_path = output_path + "/fused.ply"

    result = subprocess.run(" ".join(['colmap', 'stereo_fusion', '--workspace_path', output_path, '--workspace_format', 'COLMAP', '--input_type', 'geometric', '--output_path', output_file_path]), shell=True)

    if result.returncode == 0:
            print("stereo fusion process completed.")
    else:
        sys.stdout.flush()
        sys.stderr.flush()
        print("Process failed with code %d." % result.returncode )


    response = input("Do you want to open .ply with meshLab? (y/n) : ")

    if response == "y":
        result = subprocess.run(" ".join(['meshlab', output_file_path]), shell=True)

        if result.returncode == 0:
            print(".ply is opened completely")

    
    ########## poisson mesher process #############

    print()
    response = input("poisson mesher process (y/n) : ")

    if not response == "y":
        sys.exit(0)

    poisson_out_file_path = output_path + "/meshed-poisson.ply"

    result = subprocess.run(" ".join(['colmap', 'poisson_mesher', '--input_path', output_file_path, '--output_path', poisson_out_file_path]), shell=True)

    if result.returncode == 0:
            print("poisson mesher process completed.")
    else:
        sys.stdout.flush()
        sys.stderr.flush()
        print("Process failed with code %d." % result.returncode )

    print()
    response = input("Do you want to open .ply with meshLab? (y/n) : ")

    if response == "y":
        result = subprocess.run(" ".join(['meshlab', poisson_out_file_path]), shell=True)

        if result.returncode == 0:
            print(".ply is opened completely")

    ########## delaunay mesher process #############

    print()
    response = input("delaunay mesher process (y/n) : ")

    if not response == "y":
        sys.exit(0)

    delaunay_out_file_path = output_path + "/meshed-delaunay.ply"

    result = subprocess.run(" ".join(['colmap', 'delaunay_mesher', '--input_path', output_path, '--output_path', delaunay_out_file_path]), shell=True)

    if result.returncode == 0:
            print("delaunay mesher process completed.")
    else:
        sys.stdout.flush()
        sys.stderr.flush()
        print("Process failed with code %d." % result.returncode )

    print()
    response = input("Do you want to open .ply with meshLab? (y/n) : ")

    if response == "y":
        result = subprocess.run(" ".join(['meshlab', delaunay_out_file_path]), shell=True)

        if result.returncode == 0:
            print(".ply is opened completely")

    

    





    







        


