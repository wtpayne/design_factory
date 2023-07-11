============================
Setting up a new workstation
============================

This process provides guidance on how to set up
a new workstation for design and development
activities.

.. contents:: Table of Contents
   :local:


Introduction
============


Instructions are included for workstations
running Ubuntu Linux, Windows 10 or 11 (via WSL)
and Mac OS X.

Note: The software is primarily developed on
and for Ubuntu 22.04. Minimal consideration has
yet been given to ensuring portability.

Windows users should use the Windows Subsystem
for Linux (WSL) to emulate an Ubuntu 22.04
machine and users running Mac OS X should be
prepared to encounter potential compatibility
issues which may need to be worked through.



Instructions for workstations running Ubuntu 22.04
==================================================


1. Install prerequisites
------------------------

Use the Ubuntu Advanced Packaging Tool (APT) to
install the prerequisites::

   sudo apt-get update
   sudo apt install python3-pip python3-venv openssh-server


2. Configure SSH for passwordless SSH to localhost
--------------------------------------------------

The stableflow framework uses ssh to deploy
and run systems. This includes localhost for
local development, so we need passwordless ssh
to every machine that we wish to deploy or run
on::

   ssh-keygen -t rsa
   sudo systemctl status ssh
   sudo systemctl start ssh
   ssh-copy-id ${USER}@localhost


3. Copy the workstation public SSH key to github
------------------------------------------------

Open your github SSH keys settings page at::

   https://github.com/settings/keys

Create a new entry for the SSH key. The title
can be anything you like (<USERNAME>@<HOSTNAME>
is a common convention). The key type should be
"authentication key". Take the key value from
the public key that we have just created::

   cat ~/.ssh/id_rsa.pub


4. Clone the source design document repository
----------------------------------------------

Instructions and documentation will assume that
the source repository has been checked out to
~/dev/df, but this is not required::

   mkdir dev
   cd dev
   git clone https://github.com/wtpayne/design_factory.git df


5. Get development API keys and tokens
--------------------------------------

If you are working on a system, functional chain
or component that makes use of a third party API
(e.g. OpenAI or Discord) they you will likely need
to set up your own API keys or tokens. Please
refer to the relevant procedure for more detailed
instructions.

In production, these API keys and tokens are
stored in environment variables. During
development, we use a default.env file to
simplify the management of these secrets::

   <REPO_ROOT>/a3_src/h10_resource/key/default.env

This file contains a number of API keys and
tokens stored as key=value pairs::

   TOKEN_DISCORD_DEFAULT=<....>
   TOKEN_DISCORD_HARMONICA_DEV=<....>
   TOKEN_DISCORD_HARMONICA_UAT=<....>
   TOKEN_DISCORD_HARMONICA_PRD=<....>
   TOKEN_DISCORD_PROCESS_ASSISTANT=<....>
   APIKEY_OPENAI=<....>

Each developer should create their own version of
this file with their own keys. Take care not to
commit this file or to share it with others. If
this happens accidentally, regenerate your keys
or tokens as quickly as possible.


6. Run the system
-----------------

Now that everything is set up, you should be able
to run the system. The first time that you run
a command, it should install any missing python
dependencies for you::

   cd ~/dev/df
   ./da
   ./da demo
   ./da demo dm006
   ./da demo dm006 start
   ./da demo dm006 stop


7. Troubleshooting
------------------

If you run into problems with the automatic
dependency installation process, one way to
get back to a clean slate is to delete the
relevant virtual environment directory::

   ~/dev/df/a0_env/venv/<ENVIRONMENT_ID>



Instructions for workstations running Windows 10 or 11
======================================================

For Microsoft Windows, the Windows Subsystem for
Linux (WSL) can be used to provide an Ubuntu 22.04
environment. Once that has been configured, follow
the instructions given above for Ubuntu Linux.


1. Install Ubuntu 22.04 using WSL
---------------------------------

First of all, we need to ensure that we have
the WSL set up at the right version and with
an Ubuntu 22.04 image::

   wsl --set-default-version 2
   shutdown -r
   wsl.exe --install Ubuntu-22.04


2. Launch Ubuntu 22.04 using WSL
--------------------------------

Once we have an Ubuntu 22.04 image installed in
WSL, we can launch it. If you only have one WSL
image on your workstation, then you can simply
invoke wsl with no arguments::

   # Open terminal / shell in admin mode
   wsl

If you have more than one WSL image installed,
then you need to specify which one you want to
launch::

   # Open terminal / shell in admin mode
   wsl -d Ubuntu-22.04


3. Set up the Ubuntu 22.04 WSL instance
---------------------------------------

Follow the instructions for workstations running
Ubuntu 22.04 given above to complete the setup
process.



Instructions for workstations running Mac OS X
==============================================

To set up your Mac workstation, follow the same
instructions as for setting up an Ubuntu 22.04
workstation, except for steps 1 and 2, where you
need to use different (Mac OS X specific)
commands.


1. Install prerequisites
------------------------

Use homebrew to install the prerequisites::

   brew update
   brew install python
   brew install openssh


2. Configure SSH for passwordless SSH to localhost
--------------------------------------------------

The stableflow framework uses ssh to deploy
and run systems. This includes localhost for
local development, so we need passwordless ssh
to every machine that we wish to deploy or run
on::

   ssh-keygen -t rsa
   sudo systemsetup -getremotelogin
   sudo systemsetup -setremotelogin on
   ssh-copy-id $USER@localhost

You might get the error message when running the
third command::

   setremotelogin: Turning Remote Login on or
   off requires Full Disk Access privileges.

Here are steps to resolve this:

#. Open **System Preferences** on your Mac.
#. Go to **Security & Privacy**.
#. Switch to the **Privacy** tab.
#. Scroll down the list on the left and select
   **Full Disk Access**.
#. Click on the lock icon in the bottom-left
   corner to make changes. You will need to
   enter your password.
#. Click on the **+** button to add an application
   to the list.
#. Navigate to **Applications** > **Utilities** and
   select **Terminal**, then click **Open**.
#. Terminal now has Full Disk Access. You will need
   to close Terminal and open it again for the
   changes to take effect.


3. Complete the setup process
-----------------------------

Follow the remainder of the instructions for
workstations running Ubuntu 22.04 given above
to complete the setup process.
