FROM node:19-alpine3.16 as builder

WORKDIR /app
COPY frontend/ frontend/

WORKDIR /app/frontend
RUN npm ci
RUN npm run build

FROM python:3.10.11-slim-bullseye

WORKDIR /app
COPY . .
COPY --from=builder /app/frontend/build /app/frontend/build
RUN pip install . gunicorn

EXPOSE 5000

CMD ["gunicorn", "SimmerTheToads:app"]
