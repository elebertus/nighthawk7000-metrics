FROM centos
RUN yum clean all && yum makecache
RUN yum -y install https://centos7.iuscommunity.org/ius-release.rpm
RUN yum -y install python36u python36u-pip python36u-devel
RUN yum clean all
RUN mkdir /opt/app
ADD . /opt/app
RUN pip3.6 install -r /opt/app/requirements.txt
RUN ln -s /usr/bin/python3.6 /usr/bin/python3
ADD run_metrics.sh /opt/app/
CMD [ '/opt/app/run_metrics.sh' ]

