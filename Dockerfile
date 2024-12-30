FROM quay.io/hemanth22/rockylinux9:9
USER root

WORKDIR /root

# Copy all localhost files to the container
COPY . /root/

# Install Python 3.9 and Ansible
#RUN dnf install sudo python312 -y && python3.12 -m ensurepip && python3.12 -m pip install --upgrade pip && python3.12 -m pip install --no-cache-dir -r requirements.txt && alternatives --set python3 /usr/bin/python3.12 && alternatives --set python /usr/bin/python3.12
RUN dnf install sudo python312 -y && python3.12 -m ensurepip && python3.12 -m pip install --upgrade pip && python3.12 -m pip install --no-cache-dir -r requirements.txt && ln -sf /usr/bin/python3.12 /usr/bin/python3 && ln -sf /usr/bin/python3.12 /usr/bin/python

# Execute the Script playbook
CMD ["python3.12", "postgresql.py"]