=================================
Setting up a new server or device
=================================

This process provides guidance on how to set up
a new production server or edge device.

.. contents:: Table of Contents
   :local:


Overview
========

This procedure describes how to set up a new
server or device. I.e. a machine that will be
used for deploying a system in production.


Instructions
============


1. Device registration
----------------------

Select a codeword from the codeword register::
    
    /h10_resource/registry/codeword.register.yaml
    
Once you have selected a codeword, look in the
device register to find the next available
serial number, and combine the codeword and 
the serial number together to obtain the device
id. Use this to update both the device register
and the codeword register::

    /h10_resource/registry/device.register.yaml


2. Create device
----------------

If the device is a Linode server, create it using
the Linode management console and name it using 
the device id that you have just registered.


3. Update secrets file with the root password
---------------------------------------------

Update the default.env secrets file with a record
of the root password::

    /h10_resource/key/default.env

The environment variable name should be written
in underscore delimited all caps. It should begin
with the prefix "PWD" followed by the device id
followed by the account name. ("ROOT" in this
instance)::

    PWD_[DEVICE-ID]_ROOT='[password]'


4. Update /etc/hosts on local workstation
-----------------------------------------

On your local workstation, update your hosts
file::

    sudo vim /etc/hosts

Ensure that both the device id and the device
codeword will resolve to the same static IP
address taken from the Linode management console::

    [IP-ADDRESS]   [DEVICE-ID]
    [IP-ADDRESS]   [DEVICE-NAME]


5. Ensure you have a local ssh key pair
---------------------------------------

On your local workstation, ensure that you
have a ssh key pair in ~/.ssh. If not, create
one using::

    ssh-keygen -t rsa


6. Setup passwordless SSH for root
-----------------------------------

On your local workstation, copy your public
key to the new device to enable passwordless
ssh to the root account of the device::

    cd ~/.ssh
    ssh-copy-id -i id_rsa.pub root@[DEVICE-NAME]


7. Create your user account on the new device
---------------------------------------------

On your local workstation, open the team
member register and identify or add an
alias for your user account on the new
machine::

    /h10_resource/registry/team_member.register.yaml

Now SSH to the new device as root, and add a
new user account for your selected alias::

    ssh root@[DEVICE-NAME]
    sudo adduser [ALIAS]
    usermod -aG sudo [ALIAS]

8. Update secrets file with the user password
---------------------------------------------

Back on your local workstation, update the
default.env secrets file with a record of the
user password::

    /h10_resource/key/default.env

The environment variable name should be written
in underscore delimited all caps. It should begin
with the prefix "PWD" followed by the device id
followed by your selected user account name::

    PWD_[DEVICE-ID]_[USER]='[password]'


9. Setup passwordless SSH for your user account
-----------------------------------------------

Still on your local workstation, copy your
public key to the new device to enable
passwordless ssh to your user account on
the device::

    cd ~/.ssh
    ssh-copy-id -i id_rsa.pub [USER]@[DEVICE-NAME]


10. Setup access to github from the new device
----------------------------------------------

Ensure you are logged into the remote machine::

    ssh [USER]@[DEVICE-NAME]

Create a ssh key on the remote machine::

    ssh-keygen -t rsa

Copy ssh key to your github settings::

    cat ~/.ssh/id_rsa.pub
    https://github.com/settings/keys


11. Upgrade packages on the new device
--------------------------------------

Ensure you are logged into the remote machine::

    ssh [USER]@[DEVICE-NAME]

Upgrade all installed packages::

    sudo apt-get update
    sudo apt upgrade -y

Once all the prerequisites have been installed,
reboot the remote machine. (e.g. via the Linode
management console.)


12. Clone the software
----------------------

Ensure you are logged into the remote machine::

    ssh [USER]@[DEVICE-NAME]

Create a development directory::

    cd ~
    mkdir dev
    cd ~/dev
    git clone git@github.com:wtpayne/df.git


13. Install prerequisites on the new device
-------------------------------------------

Ensure you are logged into the remote machine::

    ssh [USER]@[DEVICE-NAME]

Install prerequisites::

    sudo apt-get install python3-pip
    sudo apt-get install python3-venv
    sudo apt-get install openssh-server
