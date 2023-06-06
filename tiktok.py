import sys
import os
import requests
from bs4 import BeautifulSoup

# check if the target_username is provided as a command-line argument
if len(sys.argv) > 1:
    target_username = sys.argv[1]
else:
    target_username = input("Enter the target TikTok username: ")

# construct the URL of the user's profile page
url = f"https://www.tiktok.com/@{target_username}"

try:
    # send a GET request to the profile page
    response = requests.get(url)

    # check if the response is successful
    if response.status_code == 200:
        # create a BeautifulSoup object from the response content
        soup = BeautifulSoup(response.content, "html.parser")

        # find all the video elements on the page
        video_elements = soup.select("video")

        # create a directory to save the videos
        output_dir = f"{target_username}_videos"
        os.makedirs(output_dir, exist_ok=True)

        # download the videos
        for i, video_element in enumerate(video_elements):
            # get the video source URL
            video_url = video_element.get("src")

            # construct the filename
            video_file = os.path.join(output_dir, f"video_{i}.mp4")

            # send a GET request to download the video
            video_response = requests.get(video_url)

            # save the video file
            with open(video_file, "wb") as file:
                file.write(video_response.content)

            print(f"Downloaded video: {video_file}")

        print("Videos downloaded successfully.")
    else:
        print(f"Failed to retrieve profile page for {target_username}.")

except Exception as e:
    print(f"An error occurred: {str(e)}")
