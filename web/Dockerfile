FROM python:3.7

# install app dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# create the app directory and set as working directory
WORKDIR /app

# copy files into the new directory
COPY . .

# run flask app with migration
RUN chmod u+x ./entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
