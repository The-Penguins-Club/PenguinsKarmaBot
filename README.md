
# Penguins Karma Bot

A KarmaBot made with python and created for [Penguins Network](https://t.me/The_penguinsClub).


## Deployment

To deploy this project run

### In a normal unix shell
```bash
  cp sample_config.env config.env
  vim config.env #Use other editor if you want
  pip3 install -r requirements.txt
  python3 -m Karma
```

### In Poetry
```bash
  cp sample_config.env config.env
  vim config.env #Use other editor if you want
  poetry install
  poetry run python -m Karma
  ```

### In Docker (Recommanded)
```bash
  cp sample_config.env config.env
  vim config.env #Use other editor if you want
  docker build . -t karmabot
  docker run karmabot
  ```