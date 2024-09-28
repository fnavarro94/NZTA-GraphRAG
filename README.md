# NZTA-GraphRAG

**Graph Retrieval Augmented Generative Chatbot Prototype**

A prototype chatbot developed for the New Zealand Transport Agency (NZTA), leveraging graph-based retrieval methods to provide intelligent and contextually relevant responses.

## Table of Contents

- [Introduction](#introduction)
- [Setup](#setup)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Obtain a Groq API Key](#2-obtain-a-groq-api-key)
  - [3. Set Up Neo4j](#3-set-up-neo4j)
  - [4. Install Google Chrome](#4-install-google-chrome)
  - [5. Set Up ChromeDriver](#5-set-up-chromedriver)
- [Usage](#usage)
  - [Install Dependencies](#install-dependencies)
  - [Crawl Data](#crawl-data)
  - [Load Data into Neo4j](#load-data-into-neo4j)
  - [Run the Chatbot](#run-the-chatbot)

## Introduction

**NZTA-GraphRAG** is a prototype of a Graph Retrieval Augmented Generative Chatbot developed for the New Zealand Transport Agency (NZTA). It utilizes graph-based retrieval methods to deliver intelligent and contextually relevant responses.

## Setup

### Python Version

This project requires **Python 3.11**. Ensure that you have Python 3.11 installed on your system before proceeding with the setup.

You can verify your Python version by running:

...bash
python --version
...


### 1. Clone the Repository

Clone the repository using Git:

```{bash}
git clone https://github.com/fnavarro94/NZTA-GraphRAG.git
```

Alternatively, download the repository as a ZIP file and extract it locally.

Navigate to the `NZTA-GraphRAG` directory:

```{bash}
cd NZTA-GraphRAG
```

Copy the example environment file:

```{bash}
cp .env.example .env
```

You will use this `.env` file later.

### 2. Obtain a Groq API Key

To run this project, you will need a Groq API key, which provides free access to fast LLM inference models through an API. You can obtain one by visiting the [Groq Console](https://console.groq.com/keys).

Alternatively, you can use Ollama locally on your machine, but response generation will be much slower (instructions coming soon).

Once you have generated your Groq API key, copy it and paste it into the `.env` file at the `GROQ_API_KEY` entry.

For example:

```{dotenv}
# .env
GROQ_API_KEY=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
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=
NEO4J_URL=bolt://localhost:7687
NEO4J_DATABASE=neo4j
```

### 3. Set Up Neo4j

We use Neo4j for this use case, but Llama-Index supports many other graph databases. Refer to [Llama-Index Graph Stores](https://docs.llamaindex.ai/en/stable/community/integrations/graph_stores/) for more information.

- Download [Neo4j Desktop](https://neo4j.com/download/).
- Follow [this guide](https://docs.google.com/document/d/1f7_xYh_ZiRN6rhQZgvqgnqvm6_KM76Xs1UaiYTIg1RU/edit?usp=sharing) to start your first database instance.
- Copy your created username (`NEO4J_USERNAME`), password (`NEO4J_PASSWORD`), and URL (`NEO4J_URL`) into the `.env` file.

### 4. Install Google Chrome

Download and install the latest version of Google Chrome from the [official support page](https://support.google.com/chrome/answer/95346?hl=en&co=GENIE.Platform%3DDesktop).

Download ChromeDriver ensuring that the version matches the version of Google Chrome you have installed:

1. Visit the [Chrome for Testing](https://googlechromelabs.github.io/chrome-for-testing/) page.

### 5. Set Up ChromeDriver

1. **Copy the Executable:**

   - **Windows:** Copy `chromedriver.exe`.
   - **Mac:** Copy `chromedriver`.

   Place the executable and all other files from the download into the `driver` directory of the repository.

2. **For Mac Users Only:** Set the necessary permissions by running the following command in the terminal:

   ```{bash}
   sudo xattr -d com.apple.quarantine "/path/to/driver/executable/chromedriver"
   ```

   Replace `"/path/to/driver/executable/chromedriver"` with the actual path to the ChromeDriver executable.

## Usage

After completing the setup steps, you can run the crawlers to download the data and then run the knowledge graph data loader script to start populating the property graph index into the Neo4j database. Once both of these steps are done, you can interact with the chatbot.

### Install Dependencies

First, install the required dependencies:

```{bash}
pip install -r requirements.txt
```

### Crawl Data

To crawl NZTA OIA responses:

```{bash}
python crawler.py
```

For Ministry of Transport data:

```{bash}
python transport_gov_crawler.py
```

### Load Data into Neo4j

Once the crawlers have completed, start uploading data into Neo4j. Ensure you have started the database instance in the Neo4j Desktop application.

```{bash}
python kg_data_loader.py
```

### Run the Chatbot

Navigate to the `chatbot` directory:

```{bash}
cd chatbot
```

Run the Flask app that hosts the chatbot:

```{bash}
python kg_app.py
```

You will find the URL of the locally hosted app in the output. Open that URL in your browser to access the chatbot interface.
