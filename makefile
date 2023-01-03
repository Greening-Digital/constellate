install:
	python -m pipenv install --dev
	npm install

serve: front_end_bundle
	cd backend && \
	python -m pipenv run python ./manage.py runserver

# clean_vue_static:
# 	rm -rf ./static-vue/
# 	rm -rf ./backend/static-vue/
# 	rm -rf ./backend/staticfiles

# front_end_bundle: clean_vue_static
# 	npm run build && \
# 	cp -R ./static-vue/ ./backend/static-vue/

# dev.frontend:
# 	npm run serve

# dev.backend:
# 	cd backend && \
# 	python -m pipenv run python ./manage.py runserver

# test.frontend:
# 	npm run test:unit

# test.backend:
# 	cd backend && \
# 	pytest -x
