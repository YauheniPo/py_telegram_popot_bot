FROM yauhenipo/ubu-py3-browsers-1.2
MAINTAINER Yauheni Papovich <ip.popovich@mail.ru>
ENV robot_dir /py_telegram_popot_bot
RUN ls -a
RUN cd
RUN ls -a
COPY . ${robot_dir}
#WORKDIR /py_telegram_popot_bot
#ENV BROWSER "chrome"
#ADD http://example.com/big.tar.xz codes/file2.cpp root/test/
RUN ls -a
RUN cd ${robot_dir} \
        && ls -a \
        && pip3 install -r requirements.txt \
        && pip3 install -r requirements_test.txt

#EXPOSE 80

CMD pwd \
        && pytest ${robot_dir}/test/
