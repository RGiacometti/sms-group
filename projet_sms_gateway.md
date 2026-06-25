# Cahier des Charges & Instructions de Développement - Passerelle de Groupe SMS/Email

Ce document est conçu pour être fourni à une Intelligence Artificielle (Agent de codage, Assistant) afin de générer l'intégralité du code du projet.

---

## 1. Présentation du Projet
L'objectif est de créer un système de **Message de Groupe (type WhatsApp)** mais basé exclusivement sur le réseau cellulaire **SMS** et sur les **Emails**. Il permet à un groupe fermé de 10 personnes de communiquer ensemble, même si certains possèdent de vieux téléphones ou n'ont pas de connexion Internet constante.

### Matériel & Environnement :
* **Serveur d'exécution :** Un smartphone Android rooté sous **LineageOS**.
* **Environnement de code :** **Termux** (environnement Linux pour Android), exécutant le script en mode utilisateur classique (non-root).
* **Passerelle SMS :** L'application Android **SMSGate** (`android-sms-gateway`) installée sur le même téléphone. Elle sert d'interface entre le réseau mobile et notre script via des requêtes HTTP sur `localhost`.

### Flux de Développement (Workflow) :
1. Développement et édition du code sur PC via **VSCode**.
2. Gestion de version et hébergement sur **GitHub** (`git push`).
3. Déploiement sur le téléphone dans Termux via un `git pull`.
4. Exécution en tâche de fond sur le téléphone.

---

## 2. Architecture Technique & Fonctionnement

L'architecture repose sur une boucle locale entre l'application Android SMSGate et notre script Python.

```
[Ami (SMS)] ──> [Réseau Mobile] ──> [Application SMSGate]
                                            │
                                    (Webhook HTTP POST)
                                            ▼
[Application SMSGate] <── (API HTTP) <── [Script Python (Termux)] ──> (SMTP) ──> [Mailing List (Email)]
```

### Étape 1 : Réception (Webhook)
Quand l'application SMSGate reçoit un SMS ou un MMS (les messages longs étant automatiquement convertis en MMS par Android), elle extrait le texte et envoie une requête HTTP POST (Webhook) à notre script Python tournant sur `http://127.0.0.1:5000/webhook`.

### Étape 2 : Traitement Logique (Le "Cœur")
Le script Python reçoit le message et applique les règles suivantes :
1. **Vérification de l'expéditeur :** Le numéro doit appartenir à la liste des 10 membres autorisés. Sinon, le message est ignoré (sécurité anti-spam).
2. **Prévention des boucles infinies (CRITIQUE) :** Le script doit identifier l'expéditeur d'origine et **ne jamais** lui renvoyer son propre message.
3. **Analyse de la longueur (Logique de Fallback) :**
   * **Si le message est COURT (<= 160 caractères) :** Il est distribué par SMS aux 9 autres membres du groupe sous la forme : `[Prénom/Nom] : message`.
   * **Si le message est LONG (> 160 caractères) :** * **Action SMS :** Le script tronque le message à 130 caractères et génère un SMS court : `[Prénom/Nom] : [Début du texte]... [Suite reçue par Email]`. Ce SMS est envoyé aux 9 membres.
     * **Action Email :** Le script envoie le pavé de texte complet par Email à la liste de diffusion (les 10 adresses e-mail du groupe) via un serveur SMTP (ex: Gmail).

### Étape 3 : Distribution (API Sortante)
Pour distribuer les SMS, le script Python émet des requêtes HTTP POST vers l'API locale de l'application SMSGate (généralement sur le port `8080` ou configuration personnalisée).

---

## 3. Spécifications du Code Python à Générer

L'IA doit générer une structure de projet propre en Python 3.

### Dépendances requises :
* `Flask` ou `FastAPI` (pour le serveur Webhook).
* `requests` (pour interagir avec l'API SMSGate).
* `smtplib` et `email.message` (bibliothèques natives pour l'envoi d'emails).

### Variables de Configuration (Fichier `.env` ou dictionnaire de configuration) :
* `SMS_GATEWAY_URL` : URL de l'API locale SMSGate (ex: `http://127.0.0.1:8080/api/v1/message/send`).
* `SMS_GATEWAY_TOKEN` : Jeton d'authentification de la passerelle.
* `MEMBRES` : Un dictionnaire associant le numéro de téléphone (format international standard, ex: `+33612345678`), le Prénom/Nom de la personne, et son adresse Email.
* `SMTP_SERVER`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD` : Identifiants pour le serveur de mail sortant.

### Gestion des Cas Limites & Robustesse :
* **Caractères spéciaux :** Le script doit gérer l'encodage `UTF-8` proprement pour éviter que les émojis ou accents ne fassent planter le serveur ou ne corrompent le texte.
* **Logs :** Mettre en place un système de logs clair (`logging`) affichant l'expéditeur, la longueur du message, le canal choisi (SMS pur ou Fallback Email), et le statut de réussite de l'envoi.
* **Erreurs Réseau :** Si le serveur SMTP est temporairement inaccessible, le script ne doit pas planter ; il doit logger l'erreur et s'assurer que le SMS tronqué est tout de même parti.

---

## 4. Feuille de Route du Développement (Roadmap pour l'IA)

L'IA devra implémenter le projet dans l'ordre suivant :

1.  **Fichier de configuration :** Créer un système de configuration propre (dictionnaire ou fichier externe).
2.  **Serveur Webhook :** Créer un serveur Flask/FastAPI écoutant sur le port 5000 avec une route `/webhook` acceptant le format JSON envoyé par `android-sms-gateway`.
3.  **Moteur de routage :** Écrire la fonction de filtrage (vérification de la liste blanche) et de calcul de taille (Condition `<= 160` vs `> 160`).
4.  **Module SMS :** Développer la fonction de boucle qui envoie une requête à l'API SMSGate pour chacun des 9 destinataires (en excluant l'expéditeur).
5.  **Module Email :** Développer la fonction d'envoi SMTP asynchrone ou sécurisée avec `smtplib.SMTP_SSL`.
6.  **Script de lancement :** Fournir une commande ou un script d'exécution pour maintenir le programme actif en tâche de fond dans Termux (`nohup` ou instructions `tmux`).

---

## 5. Instructions de Prompts pour démarrer le code
*"Agis comme un développeur Python expert spécialisé dans les systèmes embarqués et Android/Termux. Génère l'architecture de code complète basée sur ce cahier des charges, en fournissant un fichier `main.py` documenté, robuste, et prêt à être testé en boucle locale. Assure-toi d'inclure une gestion stricte des boucles infinies d'envoi."*
