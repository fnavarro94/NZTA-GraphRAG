# NZTA-GraphRAG

**Graph Retrieval Augmented Generative Chatbot Prototype**  
Built for the New Zealand Transport Agency (NZTA) as a use case.

## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#Prerequisites)
  - [1. Clone the repository](#1-clone-the-repository)
  - [2. Get a Groq API key](#2-get-a-groq-api-key)
  - [3. Set up Neo4j](#3-set-up-neo4j)
  - [2. Install Google Chrome](#1-install-google-chrome)
  - [3. Download ChromeDriver](#2-download-chromedriver)
  - [4. Configure ChromeDriver](#3-configure-chromedriver)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

NZTA-GraphRAG is a prototype of a Graph Retrieval Augmented Generative Chatbot developed for the New Zealand Transport Agency (NZTA). It leverages graph-based retrieval methods to provide intelligent and contextually relevant responses.

## Prerequisites


### 1. Clone the repository
- use
  ```{bash}
  git clone https://github.com/fnavarro94/NZTA-GraphRAG.git
  ```
- Alternatively download the repository as a zip file and extract it locally.
- Then run the following command on the command prompt
  ```{bash}
  cp .env.example .env
  ```
  you will use this .env file on later.

### 2. Get a Groq Api Key
To run this you will need a groq api key which provides free acces to fast llm inference models through an api. You can get one by going to [groq](https://console.groq.com/keys).

Alternatively you can use Ollama localy on your machine but response generation will be much slower (instructions for this comming soon). 

Once you have generated your groq key, copy it and paste it in the .env file  `GROQ_API_KEY` entry on the .env file you created earlier. 

For example

```
# .env
GROQ_API_KEY=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
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=
NEO4J_URL=bolt://localhost:7687
NEO4J_DATABASE=neo4j


```

### 

### 3. Set Up Neo4j
* We use Neo4j for this usecase but Llama-Index supports many other graph databases. [Llama-index Graph Stores](https://docs.llamaindex.ai/en/stable/community/integrations/graph_stores/)
- Download [Neo4j Descktop](https://neo4j.com/download/?utm_source=Google&utm_medium=PaidSearch&utm_campaign=Evergreen&utm_content=APAC-Search-SEMCE-DSA-None-SEM-SEM-NonABM&utm_term=&utm_adgroup=DSA&gad_source=1&gbraid=0AAAAADk9OYoXSQrlYLZG7dru9vfHVS8AY&gclid=Cj0KCQjwxsm3BhDrARIsAMtVz6P9mwe7uNuMCtDLOdCsyTfMbxGH7oH8MofV4NVE9d4wd2VhJ-jCTkAaAiqtEALw_wcB)
- Follow [this guide](https://docs.google.com/document/d/1f7_xYh_ZiRN6rhQZgvqgnqvm6_KM76Xs1UaiYTIg1RU/edit?usp=sharing) to start the first db instance.
- Copy your created username (`NEO4J_USERNAME`), password (`NEO4J_PASSWORD`) and port (`NEO4J_URL`) into the .env file. 

### 1. Install Google Chrome

Download and install the latest version of Google Chrome from the [official support page](https://support.google.com/chrome/answer/95346?hl=en&co=GENIE.Platform%3DDesktop).

### 2. Download ChromeDriver

Ensure that the ChromeDriver version matches the version of Google Chrome you have installed.

1. Visit the [Chrome for Testing](https://googlechromelabs.github.io/chrome-for-testing/) page.
2. Download the appropriate ChromeDriver executable for your operating system.

### 3. Configure ChromeDriver

1. **Copy the Executable:**
   
   - **Windows:** Rename the downloaded file to `chromedriver.exe`.
   - **Mac:** Rename the downloaded file to `chromedriver`.

   Copy the renamed executable to the `driver` directory in the repository.

2. **Mac Users Only:** Set the necessary permissions by running the following command in the terminal:

    ```bash
    sudo xattr -d com.apple.quarantine "/path/to/driver/executable/chromedriver"
    ```

    Replace `"/path/to/driver/executable/chromedriver"` with the actual path to the ChromeDriver executable.

## Usage

[Provide detailed instructions on how to use the chatbot here.]

## Contributing

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature/YourFeature`.
3. Commit your changes: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin feature/YourFeature`.
5. Open a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

