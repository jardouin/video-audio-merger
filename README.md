🎬 YouTube Video & Music Mixer


An intuitive web application that allows you to mix the audio from a main YouTube video with a separate YouTube music track, adjusting volumes and start times. Perfect for creating remixes, content with background music, or simply experimenting with your favorite videos!

✨ Features
Dual Audio Mix: Combine the original audio from a YouTube video with a separate music audio track.
Volume Control: Independently adjust the volume of both audio tracks for the perfect balance.
Custom Music Start Time: Specify the exact point (HH:MM:SS) where you want the music track to begin.
Final Video Duration: Define the duration of your resulting video.
Real-time Preview: Preview YouTube videos directly within the interface.
Multi-language Support: Interface available in English, Spanish, Mandarin, French, and Portuguese.
Direct Download: Download the mixed video directly from the application.
🚀 How to Use
Visit the deployed application on Streamlit Community Cloud: YOUR_STREAMLIT_CLOUD_APP_URL
Select Your Language: Use the language selector in the left sidebar to choose your preferred language (English by default).
Enter Main Video URL: Paste the YouTube URL of the video whose main audio you want to use.
Enter Music Track URL: Paste the YouTube URL of the song or audio you want to mix with the main video.
Adjust Music Start Time: If you want the music to start at a specific point, enter it in HH:MM:SS format (default 00:00:00).
Set Duration (Optional): If you want the final video to have a specific duration, enter it in seconds. Otherwise, the main video's duration will be used.
Adjust Volumes: Use the sliders to modify the volume of each audio track to your liking.
Click "Process": The application will download the audios, mix them with the video, and present you with a final video that you can preview and download.
🛠️ Local Development
If you wish to run this application on your local machine for development or testing:

Prerequisites
Python 3.8+
pip (Python package installer)
FFmpeg: You will need to have FFmpeg installed on your system. You can download it from ffmpeg.org and ensure it's added to your system's PATH.
Installation
Clone the repository:

Bash

git clone https://github.com/YOUR_GITHUB_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
Create a virtual environment (recommended):

Bash

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
Install Python dependencies:

Bash

pip install -r requirements.txt
Running the Application
Bash

streamlit run main.py
This will open the application in your local web browser (usually http://localhost:8501).

📁 Project Structure
main.py: The main Streamlit application code.
requirements.txt: Lists Python dependencies.
packages.txt: Lists operating system-level dependencies for Streamlit Community Cloud (contains ffmpeg).
README.md: This file.
📄 License
This project is licensed under the MIT License (if you choose MIT, create a LICENSE file in your repo with the MIT license text).

❤️ Support the Project
If you find this tool useful, please consider supporting us! Every contribution helps us maintain and improve the application.


Remember to replace these placeholders:

YOUR_STREAMLIT_CLOUD_APP_URL with the actual URL of your deployed application.
YOUR_BUYMEACOFFEE_USERNAME with your actual Buy Me a Coffee username.
YOUR_GITHUB_USERNAME with your GitHub username.
YOUR_REPO_NAME with the name of your GitHub repository.
Create a LICENSE file in the root of your repository if you decide to use the MIT license.
