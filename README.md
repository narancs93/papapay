# papapay
 A webapp where employees can maintain the menu of a restaurant, and customers can place orders 

## Installation using docker

### Prerequisites

* docker
* docker compose

### Steps

* move `.env.sample` to `.env` and optionally overwrite the default values
* execute `scripts/generate-nginx-conf.sh`. It will generate `nginx.conf` from `nginx.conf.template`
* Create and start the containers: `docker compose up -d --build`
* Run migrations: `docker compose exec web python manage.py migrate`
* Run collectstatic: `docker compose exec web python manage.py collectstatic --no-input --clear`

App should be up at `localhost:${NGINX_HOST_PORT}`. (default: http://localhost:1337/)