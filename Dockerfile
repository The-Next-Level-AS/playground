FROM python:3.9.7-bullseye

WORKDIR app/

COPY ./app .
RUN python -m pip install --upgrade pip
RUN python -m pip install -r requirements.txt
RUN python -m pip install streamlit-extras

EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
