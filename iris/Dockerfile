ARG IMAGE=intersystemsdc/iris-community:2024.1-preview
FROM $IMAGE 

# ENV VARS
# https://docs.intersystems.com/irislatest/csp/docbook/DocBook.UI.Page.cls?KEY=RACS_LibPath
ENV LD_LIBRARY_PATH=${ISC_PACKAGE_INSTALLDIR}/bin:${LD_LIBRARY_PATH}

# https://docs.intersystems.com/irisforhealthlatest/csp/docbook/DocBook.UI.Page.cls?KEY=RACS_PYTHONPATH
ENV PYTHON_PATH=/usr/irissys/bin/

# Standard process for classes install
# USER root
# WORKDIR /opt/irisapp
# RUN chown ${ISC_PACKAGE_MGRUSER}:${ISC_PACKAGE_IRISGROUP} /opt/irisapp

# USER ${ISC_PACKAGE_MGRUSER}

# copy files
COPY src src
# COPY iris.script /tmp/iris.script

# # run iris and script
# RUN iris start IRIS \
# 	&& iris session IRIS < /tmp/iris.script \
#     && iris stop IRIS quietly

