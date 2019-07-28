FROM python:3.7-stretch

EXPOSE 80 80
EXPOSE 3000 3000

WORKDIR /usr/src/app
# In order for the Docker build cache to cache packages installed via pip,
# it’s necessary to add the requirements.txt file to the image, and run pip install
# before adding the rest of the app code (via COPY . .)
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# needed for vscode
RUN pip install pylint

COPY . .
# TODO: implement gunicorn or some other productiongrade server
CMD [ "flask", "run", "--host=0.0.0.0", "--port=80" ]