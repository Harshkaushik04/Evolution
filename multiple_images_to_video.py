# import cv2
# import os
#
# # Directory containing PNG images
# image_folder = r'D:\Evolution_images\generation1'
#
# # Output video file with .mp4 extension
# video_file = r'D:\Evolution_video\output_video.mp4'  # Change the file extension to .mp4
#
# # Get all images in the directory
# images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
# images.sort()  # Ensure the images are in the correct order
#
# # Read the first image to get the width and height
# first_image_path = os.path.join(image_folder, images[0])
# frame = cv2.imread(first_image_path)
# height, width, layers = frame.shape
#
# # Desired frames per second
# fps = 30.0  # You can change this to your desired frame rate
#
# # Define the codec and create VideoWriter object for .mp4
# fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Change the codec to mp4v
# video = cv2.VideoWriter(video_file, fourcc, fps, (width, height))
#
# # Loop through all images and write them to the video
# for image in images:
#     image_path = os.path.join(image_folder, image)
#     frame = cv2.imread(image_path)
#     video.write(frame)
#
# # Release the video writer object
# video.release()

#print(f"Video {video_file} is created successfully with {fps} FPS.")

