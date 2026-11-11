FROM node:24-slim
WORKDIR /app
COPY servidor.mjs .
ARG COMMIT
ENV COMMIT=$COMMIT PORTA=3000 BANCO=/dados/recados.db
RUN mkdir /dados
EXPOSE 3000
CMD ["node", "--disable-warning=ExperimentalWarning", "servidor.mjs"]
