[# SMART-ER Prompt: 논문 요약 및 시각화 웹사이트 자동화 시스템 개발 #]

S: Situation (상황)

나는 사용자가 논문 PDF 파일을 업로드하면, 해당 논문의 전체 텍스트를 자동 추출하고, 이를 AI로 Abstract, Introduction, Results, Discussion 형태로 자동 구조화 및 요약한 후,

구조화된 요약 데이터를 .md 또는 .docx 형태로 저장하고,
Claude 또는 Gemini API를 이용해 구조화 내용을 시각화 이미지로 변환하며,
이 두 정보를 함께 보여주는 웹사이트를 자동으로 생성하고자 한다.
M: Mission (목표)

사용자 인터페이스(UI): PDF 업로드 기능이 있는 간단한 웹 페이지
백엔드 기능:

PDF → Text 추출
Text → AI 구조화 요약 (Section별 요약: Abstract, Introduction, Results, Discussion)
요약 결과 저장 (.md/.docx)
시각화 프롬프트 자동 생성 및 Claude/Gemini API 호출
결과 웹페이지: 구조화된 요약 + 시각화 이미지를 HTML에 통합 출력

A: Action Steps (행동 단계)

PDF 업로드 UI: HTML + Flask 기반 업로드 폼
텍스트 추출: PyMuPDF(fitz) 또는 pdfminer.six 활용
AI 구조화 요약: Perplexity API 또는 Claude API로 section별 요약 요청
시각화 프롬프트 생성: Claude/Gemini에 전달할 Prompt 자동 생성기 포함
요약 결과 저장: Markdown 또는 .docx 포맷으로 저장 (docs/ 디렉토리에)
시각화 이미지 저장: static/images 폴더에 자동 저장
최종 결과 페이지 출력: HTML 템플릿으로 요약 내용 + 이미지 통합 표시
R: Result Format (결과물)

docs/요약.md 또는 .docx
static/images/시각화.png
templates/result.html : 전체 결과를 보여주는 웹 페이지
T: Tone & Style (스타일)

최소한의 UI, 직관적 UX
구조화된 Section 구분
모듈화된 Flask 코드로 확장성 고려
E: Example (예시)

사용자가 “sample.pdf” 업로드 → 서버에서 추출 → OPEN API 호출 → 요약하여-> Markdown 저장 → Gemini API로 시각화 → 최종 result.html에 출력


## Step‑by‑Step Guide

The following instructions assume you will clone the repository into
`/Users/keyy/0607_Codex`. Adapt the paths if you choose a different
location.

1. **Install Python**
   
   Make sure Python 3.8 or higher is installed and available in your
   command line.

2. **Clone the repository**

   Open a terminal and run:

   ```bash
   mkdir -p /Users/keyy/0607_Codex
   git clone <repository-url> /Users/keyy/0607_Codex
   cd /Users/keyy/0607_Codex
   ```

   Replace `<repository-url>` with the HTTPS address of this project.

3. **Create a virtual environment (recommended)**
   
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Install dependencies**
   
   ```bash
   pip install -r requirements.txt
   ```

   If you run into connection errors while installing packages, you can
   download the required `.whl` files on another machine and transfer them
   here. Install them individually with `pip install <package>.whl`.

5. **Create a `.env` file for API keys**

   Copy the provided example and fill in your credentials. Leave them blank if
   you want to run everything locally.

   ```bash
   cp .env.example .env
   # Edit .env in your editor and add API keys
   ```

   The application loads these variables automatically using `python-dotenv`.
   You may also export them in your shell for the current session:

   ```bash
   export OPENAI_API_KEY="your_actual_openai_key_here"
   export ANTHROPIC_API_KEY="your_actual_anthropic_key_here"
   export GEMINI_API_KEY="your_actual_gemini_key_here"
   ```

   - `OPENAI_API_KEY` – used for text summarization
   - `ANTHROPIC_API_KEY` – used for generating visualization prompts
   - `GEMINI_API_KEY` – reserved for future Gemini image generation

6. **Run the Flask server**
   
   ```bash
   python app.py
   ```

7. **Open the web interface**
   
   Visit `http://localhost:5000` in your browser. Upload a PDF to see the
   generated summary and visualization.

Generated summaries are saved in the `docs/` folder as both Markdown and
DOCX files. Visualization images are placed under `static/images/`. Each
file name includes a timestamp so previous results are preserved.

