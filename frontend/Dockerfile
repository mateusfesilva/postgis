# Usando a versão estável mais recente do Node em 2026
FROM node:22-slim

WORKDIR /app

# Copiamos apenas os arquivos de dependência primeiro para aproveitar o cache do Docker
COPY package*.json ./

RUN npm install

# Copiamos o restante dos arquivos do projeto
COPY . .

# O Vite roda por padrão na porta 5173
EXPOSE 5173

# O "--host" é fundamental: sem ele, o Vite não aceita conexões de fora do container
CMD ["npm", "run", "dev", "--", "--host"]