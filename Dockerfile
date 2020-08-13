FROM yauhenipo/ubu-py3-browsers-1.2

RUN ls -a
RUN cd
RUN ls -a
COPY . /py_telegram_popot_bot
RUN ls -a
RUN cd py_telegram_popot_bot \
        && ls -a \
        && pip3 install -r requirements.txt \
        && pip3 install -r requirements_test.txt

CMD pwd \
        && pytest py_telegram_popot_bot/test/
