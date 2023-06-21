============================
Setting up a new workstation
============================


Overview
========

This procedure describes how to set up a new
workstation. I.e. a machine that will be
used for design and development.


Instructions for a Windows workstation
======================================

We use the Ubuntu 22.04 LTS release as the primary
OS against which we develop, so until such time as
we put some effort into ensuring cross platform
compatibility, we rely on virtualization tools to
support development on workstations that use Apple
Mac OS X or Microsoft Windows.

For Microsoft Windows, the Windows Subsystem for
Linux (WSL) can be used to provide an Ubuntu 22.04
environment, and for Mac OS X, Docker can be used
in a similar way.


1. Install Ubuntu 22.04 using WSL
---------------------------------

First of all, we need to ensure that we have
the WSL set up at the right version and with
an Ubuntu 22.04 image.

#. > wsl --set-default-version 2
#. reboot
#. > wsl.exe --install Ubuntu-22.04

2. Launch ubuntu 22.04 using WSL
--------------------------------

Once we have an Ubuntu 22.04 image installed in
WSL, we can launch it. If you only have one WSL
image on your workstation, then you can simply
invoke wsl with no arguments.

#. Open terminal / shell in admin mode
#. > wsl

If you have more than one WSL image installed,
then you need to specify which one you want to
launch:

#. Open terminal / shell in admin mode
#. > wsl -d Ubuntu-22.04


3. Install prerequisites
------------------------

Use the Ubuntu Advanced Packaging Tool (APT) to
install the prerequisites.

#. > sudo apt-get update
#. > sudo apt install python3-pip python3-venv openssh-server


4. Configure SSH for passwordless SSH to localhost
--------------------------------------------------

The stableflow framework uses ssh to deploy
and run systems. This includes localhost for
local development, so we need passwordless ssh
to every machine that we wish to deploy or run
on.

#. > ssh-keygen -t rsa
#. > sudo systemctl status ssh
#. > sudo systemctl start ssh
#. > ssh-copy-id <USERNAME>@localhost


5. Copy the workstation public SSH key to github
------------------------------------------------

Open your github SSH keys settings page at:-

    https://github.com/settings/keys

Create a new entry for the SSH key. The title
can be anything you like (<USERNAME>@<HOSTNAME>
is a common convention). The key type should be
"authentication key". Take the key value from
the public key that we have just created:-

#. > cat ~/.ssh/id_rsa.pub


6. Clone the source design document repository
----------------------------------------------

Instructions and documentation will assume that
the source repository has been checked out to
~/dev/df, but this is not required.

#. > mkdir dev
#. > cd dev
#. > git clone https://github.com/wtpayne/design_factory.git df


7. Get development API keys
---------------------------

Obtain the development API keys from the team
member responsible (currently t000_wtp).

This file contains the development API key so
keep it secret and do not commit it, or share
it with others in any way.

These will be provided as a default.env file,
compressed as a .tar.gz. Download this file,
decompress it, and move it to the resource/key
directory.

#. tar -xzf ./default.env.tar.gz
#. mv default.env ~/dev/df/a3_src/h10_resource/key


8. Run the system
-----------------

Now that everything is set up, you should be able
to run the system. The first time that you run
a command, it should install any missing python
dependencies for you.

#. > cd ~/dev/df
#. > ./da
#. > ./da demo
#. > ./da demo dm006
#. > ./da demo dm006 start
#. > ./da demo dm006 stop


9. Troubleshooting
------------------

If you run into problems with the automatic
dependency installation process, one way to
get back to a clean slate is to delete the
relevant virtual environment directory:

~/dev/df/a0_env/venv/<ENVIRONMENT_ID>


