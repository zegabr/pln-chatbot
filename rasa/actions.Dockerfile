FROM rasa/rasa:2.8.3-full

WORKDIR /app/actions
COPY actions .
ENV PYTHONUNBUFFERED=1

CMD ["run", "actions"]
