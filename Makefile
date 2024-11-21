build:
	docker build -t watermarker .

dev:
	docker compose run --rm  watermarker

clean:
	docker compose down --timeout 1 --volumes

restart:
	make clean && make dev