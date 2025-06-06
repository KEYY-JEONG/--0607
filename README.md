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

## Usage

1. Install dependencies

```bash
pip install -r requirements.txt
```

2. Run the Flask server

```bash
python app.py
```

3. Visit `http://localhost:5000` in your browser to upload a PDF and view the results.

Set `SUMMARY_API_URL`, `SUMMARY_API_KEY`, `VISUAL_API_URL`, and `VISUAL_API_KEY` environment variables to integrate external AI services.
