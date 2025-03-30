# PTSDPresentation #

Welcome! This directory is the entire Day1 presentation experiment, used to test the effect of presentation frequency using a multitude of variated images. Data is recoreded and exported to day 2, which is linked [here](https://github.com/FrankieReyna/PTSDstudyday2).

I am documenting Day1 of our Presentation study in order to make it easier to both change the code and setup the experiement in the following sections:

* Setup
* day1.py
+ MidLevel
    - segment.py
    - segassignment.py
+ LowLevel
    - pillow.py
    - present.py

## Setup

A couple of things you are going to need for the experiment:

- A functioning Windows Machine: Because of some library dependencies, you have to run the rust experiment with Windows OS. The library we use for image presentation (PsychoPy) isnt actually that good. In the future I would actually like to replace it with more stable homebrew code.

- Install [Anaconda](https://www.anaconda.com/download/success), a python environment manager

    - During the install, make sure to add anaconda to path to make it easier :D

- Install [Git](https://git-scm.com/downloads/win) so you can import the scripts of day1 and day2

After everything is installed, make sure to restart your computer.

At this point, you should have everything above installed. Make sure to create a directory for the experiment, and run the following command in powershell INSIDE of your created directory. 

<git clone (url)>

replace the url with [Day1](https://github.com/FrankieReyna/PTSDstudyday1) and [Day2](https://github.com/FrankieReyna/PTSDstudyday2) links.

cd into the day1 directory, run the following command

<conda env create -f environment.yml>

the conda environment should be installed, run 

<conda activate PTSDPYS>

Everything should be set up to run or change now.

## Day1.py