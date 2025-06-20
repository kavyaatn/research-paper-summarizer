# 📄 Research Paper Summarizer

A powerful tool that generates clear, structured summaries from lengthy research papers using advanced NLP techniques, FAISS vector storage, and Hugging Face models — all wrapped in an intuitive Streamlit interface.

## 🚀 Features

✅ **PDF Upload Support** - Upload any research paper in PDF format  
✅ **Smart Text Extraction** - Extracts and processes text from each page  
✅ **Intelligent Chunking** - Splits text into overlapping chunks for better context preservation  
✅ **Vector Search** - Creates FAISS vector store for fast similarity search  
✅ **Advanced Summarization** - Uses Hugging Face's `facebook/bart-large-xsum` model  
✅ **Robust Error Handling** - Handles API retries and model loading gracefully  
✅ **Interactive Interface** - Runs seamlessly in your browser via Streamlit  

## 🧰 Tech Stack

- **Python 3.8+**
- **Streamlit** - Interactive web application framework
- **FAISS** - Vector similarity search and clustering
- **LangChain** - Text processing (`RecursiveCharacterTextSplitter` & `HuggingFaceEmbeddings`)
- **Hugging Face Transformers** - Pre-trained models and inference API
- **PyMuPDF (fitz)** - PDF text extraction
- **python-dotenv** - Environment variable management

## 📂 Project Structure

```
research-paper-summarizer/
├── app.py                 # Streamlit app entry point
├── summarizer.py          # Core functions for processing and summarization
├── .env                   # Environment variables (not committed to git)
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
└── .gitignore            # Git ignore file
```

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/kavyaatn/research-paper-summarizer.git
cd research-paper-summarizer
```

### 2️⃣ Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Configure API Access

Create a `.env` file in the project root directory:

```ini
HF_API_TOKEN=your_huggingface_api_token_here
```

> 💡 **Get your free API token**: Visit [Hugging Face Settings](https://huggingface.co/settings/tokens) to create your API token.

## ▶️ How to Run

1. **Start the application**:
   ```bash
   streamlit run app.py
   ```

2. **Access the interface**: Open the URL displayed in your terminal (typically `http://localhost:8501`)

3. **Upload and summarize**: Upload your PDF research paper and get instant summaries!

## 📋 Usage Instructions

1. **Upload PDF**: Click the file uploader and select your research paper
2. **Processing**: The app will automatically extract text and create vector embeddings
3. **Summarization**: Get a comprehensive summary generated using state-of-the-art NLP models
4. **Review**: Read through the structured summary with key insights highlighted

## 🔧 Configuration

The application can be customized by modifying parameters in `summarizer.py`:

- **Chunk size**: Adjust text splitting parameters
- **Model selection**: Change the Hugging Face model for different summarization styles
- **Vector store settings**: Modify FAISS configuration for performance tuning

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.


## 🚨 Troubleshooting

**Common Issues:**

- **API Token Error**: Ensure your Hugging Face API token is correctly set in the `.env` file
- **Memory Issues**: For large PDFs, consider increasing chunk size or processing in batches
- **Model Loading**: First-time model loading may take a few minutes

**Need Help?** Open an issue on GitHub with your error message and system details.

## 🔮 Future Enhancements

- [ ] Support for multiple file formats (DOCX, TXT)
- [ ] Customizable summary length
- [ ] Multi-language support
- [ ] Export summaries to various formats
- [ ] Batch processing for multiple papers

---

