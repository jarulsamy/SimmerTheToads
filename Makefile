##
# Simmer The Toads
#

.PHONY: all frontend backend deploy

STT_TEMPLATE_DIR = "../frontend/public"

all:
	export STT_TEMPLATE_DIR="$(STT_TEMPLATE_DIR)"; \
	screen -c .screenrc

frontend:
	echo "Starting frontend development server"; \
		cd frontend; \
		npm start & \
		wait;

backend:
	echo "Starting backend development server"; \
		export STT_TEMPLATE_DIR="$(STT_TEMPLATE_DIR)"; \
		flask --debug --app SimmerTheToads run & \
		wait;

deploy:
	cd frontend; \
	npm run build; \
	cd ..; \
	flask --debug --app SimmerTheToads run

# end
