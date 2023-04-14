# My Home Server Manager
My Home Server Manager is a web page that allows you to manage your local PC by monitoring system information such as RAM, CPU, and GPU in real-time. You can also download programs or run specific shells on the server. Most of the code was written using ChatGPT on a zero base.

# Requirements
The following are required to run the program:

* Python
* Pip
* Flask
* Tqdm
* Matplotlib

# Configuration
* Copy the `./config/config_example.json` file to create your own `./config/config.json` file, and add your own configuration values.

# Running
## Logger
* To run the logger, navigate to `./src/monitor` and execute `python main.py`. We recommend running the logger as a daemon in the background.

# Web
* To run the web server, navigate to `./src/web` and execute `python app.py`. We recommend running both the logger and web server on Ubuntu using systemctl.

# Usage
##Home
![image](https://user-images.githubusercontent.com/3786258/231930973-4ca5aeac-807f-4790-82cd-c1ad3bced46d.png)
* Main page
* Click the "Monitor System" button to go to the system management page
* Click the "Download" button to go to the download page
* Click the "Restart Stable Diffusion" button to run the shell that restarts Stable Diffusion. The button becomes semi-transparent while the shell command is being executed, and an alert message pops up after completion indicating whether the operation was successful or not. The button color changes based on the success or failure of the operation.

## System Monitoring
![image](https://user-images.githubusercontent.com/3786258/231934185-2980a8fa-a6d6-4f9f-8c98-49c4a4bbf120.png)
* View CPU, Memory, and GPU information as time-series graphs.
* Enter a number in the "Max Time" field to see changes over a period of n hours (default is 1 hour).

## Download
![image](https://user-images.githubusercontent.com/3786258/231934595-6e68686d-e11d-4071-bced-c1c96fb7e43a.png)
* Based on the Stable Diffusion Shell.
* Select the category of the model you want to download.
* Find the web URL of the file you want to download in the "File URL" field.
* Set the name of the file you want to download in the "File Name" field. If no name is specified, the file will be downloaded using the name specified in the download URL.
