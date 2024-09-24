# NZTA-GraphRAG

**Graph Retrieval Augmented Generative Chatbot Prototype**  
Built for the New Zealand Transport Agency (NZTA) as a use case.

## Table of Contents

- [Introduction](#introduction)
- [Setup Instructions](#setup-instructions)
  - [1. Install Google Chrome](#1-install-google-chrome)
  - [2. Download ChromeDriver](#2-download-chromedriver)
  - [3. Configure ChromeDriver](#3-configure-chromedriver)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

NZTA-GraphRAG is a prototype of a Graph Retrieval Augmented Generative Chatbot developed for the New Zealand Transport Agency (NZTA). It leverages advanced graph-based retrieval methods to provide intelligent and contextually relevant responses.

## Setup Instructions

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

