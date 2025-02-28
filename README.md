# VidioFlow

VidioFlow is a powerful web application for creating video scripts and optimizing content for SEO. It leverages OpenAI's API to generate high-quality, customizable video scripts and enhance existing content for better search engine visibility.

## Features

### Video Script Generation
- **Script Templates** - Choose from multiple pre-defined templates (Tutorial, Review, Explainer, Storytelling, Vlog)
- **Customization** - Adjust tone, duration, target audience, and language
- **Multi-language Support** - Generate scripts in different languages
- **SEO Optimization** - Enhance scripts with keywords for better search visibility

### Content Analysis
- **Script Analytics** - Get readability scores, tone analysis, and improvement suggestions
- **B-Roll Suggestions** - Receive tailored visual/b-roll ideas for each section of your script
- **Thumbnail Generation** - Get creative thumbnail ideas with compelling overlay text
- **SEO Analysis** - Score your content's SEO effectiveness with actionable recommendations

### Production Tools
- **Voice-Over Preview** - Listen to a text-to-speech preview of your script with multiple voice options
- **Export Options** - Download your scripts as PDF or Word documents
- **Script Versioning** - Save and compare multiple versions of your scripts
- **Visual Guidance** - Get caption and visual suggestions throughout your script

### SEO Optimization
- **Content Enhancement** - Optimize existing content for search engines
- **Keyword Integration** - Naturally incorporate target keywords
- **Structure Improvement** - Get better headings, paragraphs, and content flow
- **Meta Tag Generation** - Create SEO-friendly titles, descriptions, and keywords

## Requirements

- Python 3.8+
- Flask
- OpenAI API key
- Additional packages listed in requirements.txt

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/vidioflow.git
   cd vidioflow
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Directory Structure

```
VidioFlow/
├── app.py                  # Flask application
├── utils/                  # Utility modules
│   ├── script_generator.py # Script generation module
│   ├── seo_optimizer.py    # SEO optimization module
│   ├── export.py           # PDF/DOCX export module
│   └── text_to_speech.py   # Voice preview module
├── requirements.txt        # Project dependencies
├── .env                    # Environment variables (create this)
├── README.md               # Project documentation
└── templates/              # HTML templates
    └── index.html          # Main application interface
```

## Usage

1. Start the Flask server:
   ```
   python app.py
   ```

2. Open your web browser and navigate to:
   ```
   http://localhost:5000/
   ```

3. Use the interface to:
   - Generate video scripts using various templates and customization options
   - Analyze scripts for readability and engagement metrics
   - Get B-roll and thumbnail suggestions
   - Preview script sections with text-to-speech
   - Export scripts in different formats
   - Optimize content for SEO with keyword analysis

## API Endpoints

### Script Generation
- `GET /api/templates` - Get available script templates
- `POST /generate-script` - Generate a video script
- `GET /script-versions` - Get versions of scripts for a topic
- `GET /script-version/<script_id>` - Get a specific version of a script

### Script Analysis
- `POST /analyze-script` - Analyze a script and provide metrics
- `POST /generate-b-roll` - Generate B-roll suggestions
- `POST /generate-thumbnails` - Generate thumbnail ideas

### Export and Media
- `POST /export-pdf` - Export script as PDF
- `POST /export-docx` - Export script as DOCX
- `POST /generate-speech` - Generate speech from script text

### SEO Tools
- `POST /optimize-seo` - Optimize content for SEO
- `POST /seo-analysis` - Analyze content for SEO effectiveness

## Future Enhancements

- User accounts and cloud storage for scripts
- Collaborative editing features
- AI-generated images for thumbnails
- Integration with video editing software
- Custom template creation
- Advanced analytics dashboard
- Video publishing integrations (YouTube, Vimeo, etc.)

## License

This project is licensed under the MIT License - see the LICENSE file for details.