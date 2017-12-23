#!/bin/bash
sleep 1

# tmux session name
session_name="xiaoyun"

#Delete Cache
sudo rm -r /root/.cache
sudo rm -r /root/.netease-musicbox
sudo rm -r /root/userInfo
sleep 1

#Update xiaoyun-robot
cd $HOME/xiaoyun
git pull

#Update xiaoyun Requirements
sudo pip install --upgrade -r client/requirements.txt
sleep 1

#Update xiaoyun-contrib
cd $HOME/.xiaoyun/contrib
git pull

#Update xiaoyun-contrib Requirements
sudo pip install --upgrade -r requirements.txt
sleep 1

#Restore Configuration of AlsaMixer
if [ -f $HOME/asound.state ]; then
    alsactl --file=$HOME/asound.state restore
    sleep 1
fi

#Launch xiaoyun in tmux
sudo tmux new-session -d -s $session_name $HOME/xiaoyun/xiaoyun.py
sleep 1

#Start Respeaker-Switcher in Background
if [ -d $HOME/ReSpeaker-Switcher ]; then
    sudo python $HOME/ReSpeaker-Switcher/switcher.py &
fi

cd $HOME/xiaoyun
