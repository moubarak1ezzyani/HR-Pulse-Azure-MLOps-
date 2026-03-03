# Étape 1 : Construction (Build)
FROM node:24-slim AS builder

WORKDIR /app

# Copie des fichiers de configuration
COPY package*.json ./

# Installation des dépendances
RUN npm install

# Copie du reste du code source
COPY . .

# Construction de l'application Next.js
# NEXT_PUBLIC_API_URL peut être passé ici si nécessaire au build
RUN npm run build

# Étape 2 : Exécution (Runner)
FROM node:24-slim AS runner

WORKDIR /app

# On définit l'environnement en production
ENV NODE_ENV=production

# Copie uniquement des fichiers nécessaires depuis le builder
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json

# Exposer le port par défaut de Next.js
EXPOSE 3000

# Commande de lancement
CMD ["npm", "run", "start"]