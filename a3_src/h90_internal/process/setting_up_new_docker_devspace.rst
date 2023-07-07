===================================
Docker Container Installation Guide
===================================

This process provides guidance on how to set up
a docker container as a development environment.

.. contents:: Table of Contents
   :local:


Prerequisites
=============

You will need Docker installed on your machine.
Docker is a containerization platform that
packages your application and all its dependencies
together in the form of a docker container to
ensure that your application works seamlessly in
any environment.



Installation
============


1. Download and install Docker for your OS
------------------------------------------

Visit the Docker website::

   `download page <https://www.docker.com/products/docker-desktop>`_,

select the version for your Operating System
and follow the prompts to install Docker.


2. Create a new directory for the Dockerfiles
---------------------------------------------

Create a new directory on your machine where
you'll store the Dockerfile. You can do this
via the command line or manually in your
system's file explorer.


3. Download the dockerfiles
---------------------------

Download the dockerfiles and save to the new
directory::

   <REPO-ROOT>/a3_src/h90_internal/process/Dockerfile
   <REPO-ROOT>/a3_src/h90_internal/process/.dockerignore


4. Navigate to the dockerfile directory
---------------------------------------

Open a terminal and navigate to the directory
containing the Dockerfile using the 'cd' command.


5. Build the docker container
-----------------------------

Run the following command, replacing <YOURUSERNAME> with your chosen username::

   docker build --build-arg USERNAME=<YOURUSERNAME> -t harmonica .

Docker will start building the container based
on the instructions in the Dockerfile.


6. Run the docker container
---------------------------

After Docker has finished building the
container, you can run it using the following
command, again replacing <YOURUSERNAME> with
your chosen username::

   docker run -v $(pwd):/home/<YOURUSERNAME> /dev -it harmonica /bin/bash

Note: If you are using Windows PowerShell,
change ``$(pwd)`` to ``$(PWD)``.



SSH Key Generation
==================


1. Generate the SSH key
-----------------------

Once the Docker container has finished loading,
you can generate an SSH key by running the
following command::

   cat ~/.ssh/id_rsa.pub

This command prints the contents of the
id_rsa.pub file to the console. Copy the output
to your clipboard, making sure to include the
entire string.


2. Add SSH key to GitHub
------------------------

Go to your GitHub account settings by clicking
on your profile picture in the top right corner
of the screen and then clicking on 'Settings'.
In the left side panel, click on 'SSH and GPG
keys'. Click the green 'New SSH Key' button and
paste your copied SSH key into the text box.
You can also add a title for your reference.



Clone the GitHub repository
===========================


1. Clone the repository
-----------------------

Go back to the running Docker bash terminal
and run the following command to clone the
'design_factory' repository::

   git clone https://github.com/wtpayne/design_factory.git df

This command creates a local copy of the
'design_factory' repository and names it 'df'.


2. Navigate to the repository
-----------------------------

Navigate to the 'df' directory by running
the command::

   cd df



Running the demo
================


1. Start the demo
-----------------

You can start the demo by running the
following commands in sequence::

   ./da
   ./da demo
   ./da demo dm006
   ./da demo dm006 start


2. Stop the demo
----------------

To stop the demo, run the command::

   ./da demo dm006 stop


Editing docker image files in VSC
=================================

1. Find the name of the container that is
   currently running the harmonica docker image by
   clicking on the 'Containers' tab in the top
   left of your docker app. Make a note of it.

2. Open visual studio code and install the
   'Dev Containers' extension. The VS marketplace
   link is::

      https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers

3. In the bottom left corner of VSC click
   on the blue box that has the
   '> <' logo ( <- looks something like that).
    
4. In the pop-up menu that appears, select
   'attach to running container'.

5. Then click on the name of container id that
   is running the docker image. You can now open
   any folder inside of your docker image to edit
   the files in VSC.