## SamplStak

## Problem Solved
Most modern music productions utilize audio samples to elevate and achieve their sonic goals for their project song. Whether it is a piano melody, or a drum break, or a sound clip of cars passing by on a busy road, producers "chop up" these audio files in their DAWS(digital audio workstations) to isolate specific parts (loops) to inspire the main riff of a song or layer sounds on top of each other for a unique "one-shot" sound. Drum samples specifically, are *very* unique and are often *made*, *collected*, and *traded* amongst producers in packs (zip files) called "drumkits." 
**SamplStak** is a platform for users to browse samples created by others and to upload their very own samples to share. 


## Learning Goals

- Gain an understanding of how to use DRF FileField and ImageField to handle file and image uploads in a Django web application.
- Learn how to set up and configure DRF serializers to handle file/image uploads and handle data in complex formats.
- Gain an understanding of implementing CRUD (Create, Retrieve, Update, Delete) operations using DRF views and serializers.


## Features

SamplStak is a platform that offers music producers an intuitive and user-friendly way to manage their drum samples. The DRF server at the core of this platform provides powerful features that enable users to upload, manage, and share their samples with ease. With streamlined file uploads, dynamic filtering, and the ability to save favorite samples to a personal collection, users can easily find and share the perfect samples to elevate their productions. Users are able to manage their own sample and drumkit collections, allowing them to upload, edit, and delete their own samples and drumkits. These features provide users with a comprehensive and customizable platform that streamlines the process of music production.

## Set Up

1. Clone this repo

    ```
    git clone git@github.com:nicholasvaldez/samplstak-server.git
    cd samplstak-server
    ```

2. Activate virtual environment

    ```
    pipenv shell
    ```

3. Install dependencies

    ```
    pipenv install
    ```

4. [Install Pillow](https://pillow.readthedocs.io/en/stable/installation.html)

4. Run the server

    ```
    python manage.py runserver
    ```

5. Finish installation by following the instructions found here:


<a href="https://github.com/nicholasvaldez/samplstak-client" target="_blank"><img src="https://img.shields.io/badge/client_repo%20-%2375120e.svg?&style=for-the-badge&&logoColor=white" alt="SamplStak-Client Repo" style="height: auto !important; width: auto !important;" /></a>

## Nick Valdez

<a href="https://www.github.com/nicholasvaldez/" target="_blank"><img src="https://img.shields.io/badge/github%20-%23121011.svg?&style=for-the-badge&logo=github&logoColor=white" alt="Nick Valdez GitHub" style="height: auto !important;width: auto !important;" /></a> <a href="https://www.linkedin.com/in/nicholasvaldez/" target="_blank"><img src="https://img.shields.io/badge/linkedin%20-%230077B5.svg?&style=for-the-badge&logo=linkedin&logoColor=white" alt="Nick Valdez LinkedIn" style="height: auto !important;width: auto !important;" /></a>
