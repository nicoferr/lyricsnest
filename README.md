# Installation

Once you've cloned this repository, use the commands below
```python 
# Create a virtual env
py -m venv .venv 

# Activate the virtual env
.venv/Scripts/activate

# Install dependencies from requirements.txt
py -m pip install -r requirements.txt

# Migrate the migrations
py manage.py migrate

# Install tailwindcss dependencies
py manage.py tailwind install

# Launch server for test
py manage.py runserver

# Launch tailwindcss
py manage.py tailwind start

```

## AI Configuration

I use https://www.together.ai/ to use one of its AI.
You need an account and an API Key (you have a few credits for free but then you have to pay to refresh your balance)
Create an **.env** file from **.env.example** and put your API Key there.

You can go to Together AI website to see which AI models are available and replace the **model=** parameter in the **invokeAI()** function in **lyricsnest/views.py**


## Deployment
```
docker compose up -d
```