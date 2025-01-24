# Retrieval-Augmented-Generation-API

An advanced Retrieval-Augmented Generation (RAG) API built using the Django framework without relying on LangChain's chain module. This API leverages the power of the **Llama 3.2 3B Instruct** model for efficient and precise text generation augmented with retrieval capabilities.

## Features

- **RAG Architecture**: Combines retrieval and generation seamlessly for more context-aware responses.
- **Django Framework**: Built with Django for scalability and maintainability.
- **Llama 3.2 3B Instruct**: Employs Llama's 3.2 billion parameter instruct-tuned model for state-of-the-art performance.
- **Custom Implementation**: Designed without using LangChain's chain, providing flexibility and insight into the core architecture.
- **Interactive Chat Interface**: A simple HTML-based chat interface for engaging with the API.

## Getting Started

### Prerequisites

1. **Python**: Ensure you have Python 3.8+ installed.
2. **Anaconda**: Recommended for environment management.
3. **Django**: Install Django 4.0+.
4. **Llama Model**: Set up Llama 3.2 3B Instruct in your environment.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/Retrieval-Augmented-Generation-API.git
   cd Retrieval-Augmented-Generation-API
   ```

2. Create a new conda environment and activate it:
   ```bash
   conda create -n rag-api python=3.8
   conda activate rag-api
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run migrations and start the server:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

5. Access the API at `http://127.0.0.1:8000/api/`.

### Setting Up Llama 3.2 3B Instruct

- Follow the official instructions to set up Llama 3.2 3B Instruct locally or on a server.
- Ensure the API has access to the model for generating responses.

## Usage

- Open the interactive chat interface in your browser at `http://127.0.0.1:8000/web/`.
- Start chatting with the bot to experience the retrieval-augmented generation.

## Showcase

Check out the demo video showcasing the chat interface:

![Chat Interface Demo](https://github.com/user-attachments/assets/85c74bd2-3370-44a4-a35c-887a2b293bf4)


## Project Structure

```
Retrieval-Augmented-Generation-API/
├── api/                # Core Django app for the RAG API
├── templates/          # HTML files for the chat interface
├── static/             # Static assets like CSS and JavaScript
├── manage.py           # Django project management script
├── requirements.txt    # Project dependencies
└── README.md           # Project documentation
```

## Contributing

Contributions are welcome! If you have suggestions, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

### Notes

- Ensure that you have sufficient computational resources for running Llama 3.2 3B Instruct.
- The showcase video demonstrates the basic chat interface interacting with the API.

