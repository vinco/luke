#!/bin/bash
echo "Installing yarn..."
curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list

echo "Updating apt repositories..."
apt-get update


echo "Installing base packages..."
PACKAGES="build-essential zsh git vim-nox tree htop libjpeg-dev libfreetype6-dev graphviz gettext"
PACKAGES="$PACKAGES python3 python3-setuptools python3-pip python3-dev"
PACKAGES="$PACKAGES postgresql-10 postgresql-server-dev-10"
PACKAGES="$PACKAGES nginx yarn"

apt-get install -y $PACKAGES


echo "Setting up PostgreSQL server..."
cp /tmp/templates/postgresql/pg_hba.conf /etc/postgresql/10/main/pg_hba.conf
service postgresql restart

USER_EXISTS=$(psql -U postgres -h localhost -tAc "SELECT 1 FROM pg_roles WHERE rolname='vagrant'" postgres)

if [ ! $USER_EXISTS ]; then
    sudo -Hu postgres bash -c 'createuser -dSR vagrant'
fi

echo "Setting up reverse proxy with Nginx..."
unlink /etc/nginx/sites-enabled/default
cp /tmp/templates/nginx/local.conf /etc/nginx/sites-available/
ln -s /etc/nginx/sites-available/local.conf /etc/nginx/sites-enabled/
service nginx restart


echo "Installing Oh My Zsh!..."
PROJECT_NAME=luke
OHMYZSH_DIR=/home/vagrant/.oh-my-zsh

if [ ! -d $OHMYZSH_DIR ]; then
    sudo -Hu vagrant bash -c "git clone https://github.com/robbyrussell/oh-my-zsh.git $OHMYZSH_DIR"
fi

export PROJECT_NAME
echo "$(envsubst < /tmp/templates/zsh/zprofile)" > /home/vagrant/.zprofile
cp /tmp/templates/zsh/zshrc /home/vagrant/.zshrc


echo "Copying fabfile, tox, environments and yarn configs..."
echo "$(envsubst < /tmp/templates/fabric/fabfile.py)" > /vagrant/fabfile.py
echo "$(envsubst < /tmp/templates/tox/tox.ini)" > /vagrant/tox.ini
echo "$(envsubst < /tmp/templates/env/environments.json)" > /vagrant/environments.json
echo "$(envsubst < /tmp/templates/yarn/package.json)" > /vagrant/package.json


chown vagrant:vagrant /home/vagrant/.zshrc
chown vagrant:vagrant /home/vagrant/.zprofile
chsh -s $(which zsh) vagrant


echo "Configuring virtualenv..."
VIRTUALENV_DIR=/home/vagrant/env

pip3 install virtualenv

if [ ! -d "$VIRTUALENV_DIR" ]; then
    mkdir $VIRTUALENV_DIR
    virtualenv $VIRTUALENV_DIR
    chown -R vagrant:vagrant $VIRTUALENV_DIR
fi


echo "Configuring nodejs with nvm..."
NVM_DIR=/home/vagrant/env/nvm

if [ ! -d "$NVM_DIR" ]; then
    git clone https://github.com/creationix/nvm.git $NVM_DIR && cd $NVM_DIR && git checkout `git describe --abbrev=0 --tags`
    chown -R vagrant:vagrant $NVM_DIR
    sudo -Hu vagrant bash -c "source $NVM_DIR/nvm.sh && nvm install stable"
fi


echo "Installing python dependencies..."
REQUIREMENTS_FILE=/home/vagrant/src/requirements/local.txt

if [ -f "$REQUIREMENTS_FILE" ]; then
    sudo -Hu vagrant bash -c "source $VIRTUALENV_DIR/bin/activate && pip3 install -r $REQUIREMENTS_FILE"
fi


echo "Creating Django project..."
PROJECT_DIR=/home/vagrant/src/$PROJECT_NAME

if [ ! -d  "$PROJECT_DIR" ]; then
    export PROJECT_NAME
    sudo -Hu vagrant bash -c "source $VIRTUALENV_DIR/bin/activate && django-admin.py startproject $PROJECT_NAME $PROJECT_DIR/.."
    mkdir $PROJECT_DIR/settings
    rm $PROJECT_DIR/settings.py
    echo "$(envsubst < /tmp/templates/django/settings_base.py)" > $PROJECT_DIR/settings/__init__.py
    echo "$(envsubst < /tmp/templates/django/settings_local.py)" > $PROJECT_DIR/settings/local.py
    echo "$(envsubst < /tmp/templates/django/settings_staging.py)" > $PROJECT_DIR/settings/staging.py
    echo "$(envsubst < /tmp/templates/django/settings_testing.py)" > $PROJECT_DIR/settings/testing.py

    cp -r /tmp/templates/django/utils $PROJECT_DIR
    cp -r /tmp/templates/django/core $PROJECT_DIR
    cp -r /tmp/templates/django/api $PROJECT_DIR

    echo "$(envsubst < /tmp/templates/django/api/urls.py)" > $PROJECT_DIR/api/urls.py

    echo "$(envsubst < /vagrant/tox.ini)" > $PROJECT_DIR/tox.ini
    chown -R vagrant:vagrant $PROJECT_DIR/..
fi


echo "Done."
