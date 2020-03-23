  
#!/bin/sh


#enable rhscl and optional software repos
sudo --enable rhel-7-server-optional-rpms
sudo --enable rhel-server-rhscl-7-rpms

#install @development. - This would let us use GCC, make, git, etc
#sudo yum -y install @development

#install rh-python36
sudo yum -y install rh-python36

#install numpy
sudo yum -y install rh-python36-numpy

#add python3 to our path
sudo scl enable rh-python36 bash
sudo python3 -V

#install needed tools
sudo yum install pkgconfig
sudo yum install libpng-devel
sudo yum install freetype*
python3 -m pip install matplotlib

#restart if needed
#sudo /etc/init.d/httpd restart








