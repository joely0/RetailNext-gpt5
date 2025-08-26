# 🚀 RetailNext Fashion Recommender - Streamlit Interface

This is the **Streamlit web interface** for the RetailNext Fashion Recommendation System.

## 🎯 Features

- **📸 Image Upload**: Upload clothing images for AI analysis
- **🧠 GPT-5 Analysis**: Advanced image understanding with OpenAI's latest model
- **🔍 Smart Search**: Find similar items using semantic embeddings
- **✅ AI Guardrails**: Validate outfit compatibility with AI reasoning
- **🎨 Beautiful UI**: Clean, professional interface built with Streamlit

## 🚀 Quick Start

### 1. **From Project Root** (Recommended)
```bash
python run_streamlit.py
```

### 2. **Direct Streamlit Command**
```bash
cd streamlit_app
streamlit run main.py
```

### 3. **With Custom Port**
```bash
streamlit run streamlit_app/main.py --server.port 8502
```

## 🔧 Requirements

Install the Streamlit-specific requirements:
```bash
pip install -r streamlit_app/requirements.txt
```

## 🌐 Access

Once running, open your browser to:
- **Local**: http://localhost:8501
- **Network**: http://your-ip:8501

## 📁 Structure

```
streamlit_app/
├── main.py              # Main Streamlit application
├── components/          # Reusable UI components
├── pages/              # Multi-page navigation
├── utils/              # Utility functions
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## 🎨 Customization

- **Theme**: Edit `.streamlit/config.toml`
- **Styling**: Modify CSS in `main.py`
- **Components**: Add new components in `components/`
- **Pages**: Create multi-page navigation in `pages/`

## 🔍 Troubleshooting

### Port Already in Use
```bash
pkill -f "streamlit run"
```

### Import Errors
- Ensure you're running from the project root
- Check that `src/` directory exists
- Verify `OPENAI_API_KEY` is set

### Image Analysis Issues
- Use clear, well-lit clothing images
- Ensure images are in JPG/PNG format
- Check OpenAI API quota and billing

## 🚀 Deployment

### Streamlit Cloud
1. Push this branch to GitHub
2. Connect your repository to Streamlit Cloud
3. Deploy automatically on push

### Local Production
```bash
streamlit run streamlit_app/main.py --server.headless true
```

## 📚 Back to Main

This is the **Streamlit branch** of the project. The main branch contains the working command-line version.

- **Main Branch**: Core functionality, command-line interface
- **This Branch**: Web interface, user-friendly UI

---

**Built with ❤️ using Streamlit, OpenAI GPT-5, and semantic search**
