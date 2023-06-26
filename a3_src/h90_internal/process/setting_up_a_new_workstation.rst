============================
Setting up a new workstation
============================


Overview
========

This procedure describes how to set up a new
workstation. I.e. a machine that will be
used for design and development.

Mac instructions are below those for Windows.
Development is possible on a Mac workstation,
though there may be hidden compatibility issues
which will make themselves known later. Windows
users should emulate Ubuntu 22.04.

If you would like to use Docker on Mac to emulate
Ubuntu, 


Instructions for a Windows workstation
======================================

We use the Ubuntu 22.04 LTS release as the primary
OS against which we develop.

For Microsoft Windows, the Windows Subsystem for
Linux (WSL) can be used to provide an Ubuntu 22.04
environment.


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


Instructions for a Mac workstation
======================================


This is mostly the same as the windows instructions,
except the commands to make the SSH keypair are
different and you are not running an instance of
Ubuntu (though you are free to do so— if you do,
swap step 1 here for step 4 in the Windows 
instructions).


1. Configure SSH for passwordless SSH to localhost
--------------------------------------------------

The stableflow framework uses ssh to deploy
and run systems. This includes localhost for
local development, so we need passwordless ssh
to every machine that we wish to deploy or run
on.

> ssh-keygen -t rsa
> sudo systemsetup -getremotelogin
> sudo systemsetup -setremotelogin on
> ssh-copy-id $USER@localhost

You might get the error message when running the
third command:

> setremotelogin: Turning Remote Login on or off
requires Full Disk Access privileges.

Here are steps to resolve this:

1. Open **System Preferences** on your Mac.
2. Go to **Security & Privacy**.
3. Switch to the **Privacy** tab.
4. Scroll down the list on the left and select
   **Full Disk Access**.
5. Click on the lock icon in the bottom-left
   corner to make changes. You will need to
   enter your password.
6. Click on the **+** button to add an application
   to the list.
7. Navigate to **Applications** > **Utilities** and
   select **Terminal**, then click **Open**.
8. Terminal now has Full Disk Access. You will need 
   to close Terminal and open it again for the 
   changes to take effect.

2. Copy the workstation public SSH key to github
------------------------------------------------

Open your github SSH keys settings page at:-

    https://github.com/settings/keys

Create a new entry for the SSH key. The title
can be anything you like (<USERNAME>@<HOSTNAME>
is a common convention). The key type should be
"authentication key". Take the key value from
the public key that we have just created:-

> cat ~/.ssh/id_rsa.pub


3. Clone the source design document repository
----------------------------------------------

Instructions and documentation will assume that
the source repository has been checked out to
~/dev/df, but this is not required.

> mkdir dev
> cd dev
> git clone https://github.com/wtpayne/design_factory.git df


4. Get development API keys
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

> tar -xzf ./default.env.tar.gz
> mv default.env ~/dev/df/a3_src/h10_resource/key


5. Run the system
-----------------

Now that everything is set up, you should be able
to run the system. The first time that you run
a command, it should install any missing python
dependencies for you.

> cd ~/dev/df
> ./da
> ./da demo
> ./da demo dm006
> ./da demo dm006 start
> ./da demo dm006 stop


6. Troubleshooting
------------------

If you run into problems with the automatic
dependency installation process, one way to
get back to a clean slate is to delete the
relevant virtual environment directory:

~/dev/df/a0_env/venv/<ENVIRONMENT_ID>
