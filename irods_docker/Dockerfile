FROM ubuntu:20.04
# ARG means it's only valid when building image, not at runtime
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Brussels



# set bash as current shell
RUN chsh -s /bin/bash
SHELL ["/bin/bash", "-c"]

# COPY /mnt/data/ /mnt/data
# install anaconda
RUN TZ=Etc/UTC
RUN apt-get update
RUN apt-get install -y wget  lsb-core vim && \
        apt-get clean
	

RUN wget -qO - https://packages.irods.org/irods-signing-key.asc | apt-key add - && \
        echo "deb [arch=amd64] https://packages.irods.org/apt/ $(lsb_release -sc) main" | tee /etc/apt/sources.list.d/renci-irods.list && \ 
        apt-get update && \ 
        apt-get install -y irods-icommands

RUN mkdir -p ~/.irods 
# cat > ~/.irods/irods_environment.json <<'EOF' \
#         { \
#           "irods_host": "gbiomed.irods.icts.kuleuven.be", \
#           "irods_port": 1247, \
#           "irods_zone_name": "gbiomed", \
#           "irods_authentication_scheme": "PAM", \
#           "irods_encryption_algorithm": "AES-256-CBC", \
#           "irods_encryption_salt_size": 8, \
#           "irods_encryption_key_size": 32, \
#           "irods_encryption_num_hash_rounds": 16, \
#           "irods_user_name": "u0147891", \
#           "irods_ssl_ca_certificate_file": "", \
#           "irods_ssl_verify_server": "cert", \
#           "irods_client_server_negotiation": "request_server_negotiation", \
#           "irods_client_server_policy": "CS_NEG_REQUIRE", \
#           "irods_default_resource": "default" \
#         } \
#         EOF

# RUN iinit -h | grep Version | grep -v -q 4.3.0 || sed -i 's/"irods_authentication_scheme": "PAM"/"irods_authentication_scheme": "pam_password"/' ~/.irods/irods_environment.json
