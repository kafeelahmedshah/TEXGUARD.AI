# 🧵 TexGuard AI

**AI-Powered Textile Fabric Quality Inspection — Hackathon MVP**

TexGuard AI is a Streamlit-based prototype for textile quality control. A user uploads a fabric image and the application performs image-statistics analysis to identify suspicious irregular areas, assign a quality grade, estimate waste risk, suggest possible causes/actions, and generate a QC report.

> **Important:** This version is a hackathon MVP. The current detector is a lightweight heuristic prototype, not a trained industrial AI model. For production-quality detection, connect a trained YOLO/CNN/vision model.

## Features

- 📸 Fabric image upload
- 🔎 AI-assisted suspicious-area marking
- 🧵 Fabric quality grading: A/B/C/D
- ⚠️ Severity classification
- 📊 Surface irregularity and texture indicators
- ♻️ Estimated waste-risk score
- 🛠️ Possible defect causes
- 💡 Recommended corrective actions
- 📄 Downloadable QC inspection report
- 📈 Demo factory dashboard
- 🤖 Textile AI knowledge guide
- 🌐 Streamlit web interface
- 🚀 GitHub + Streamlit Cloud friendly

## Project Structure

```text
TexGuard-AI/
│
├── app.py
├── required.text
└── readme.md
```

## Run Locally

### 1. Clone the GitHub repository

```bash
git clone https://github.com/YOUR-USERNAME/TexGuard-AI.git
cd TexGuard-AI
```

### 2. Install dependencies

The file supplied with this project is named `required.text` because that was the requested filename.

For Streamlit/Python package installation, rename it to:

```text
requirements.txt
```

Then run:

```bash
pip install -r requirements.txt
```

### 3. Start Streamlit

```bash
streamlit run app.py
```

The application will open in your browser.

## Deploy on Streamlit Community Cloud

1. Create a GitHub repository.
2. Upload:
   - `app.py`
   - `requirements.txt` (rename `required.text` to `requirements.txt`)
   - `readme.md`
3. Open Streamlit Community Cloud.
4. Select your GitHub repository.
5. Select `app.py` as the main file.
6. Deploy.

## How the Current Prototype Works

```text
Fabric Image
     ↓
Image preprocessing
     ↓
Brightness + texture analysis
     ↓
Surface irregularity score
     ↓
Quality grade
     ↓
Possible defect category
     ↓
Root-cause suggestion
     ↓
Waste-risk estimate
     ↓
QC report
```

## How to Make It a REAL AI Defect Detector

For a stronger final hackathon version, replace the `analyze_image()` heuristic function with a trained computer-vision model.

Recommended architecture:

```text
Camera / Image
      ↓
Image preprocessing
      ↓
YOLO / CNN model
      ↓
Defect detection
      ↓
Defect classification
      ↓
Root-cause prediction
      ↓
Quality grading
      ↓
Dashboard + QC report
```

### Recommended defect classes

- Hole
- Broken yarn
- Stain
- Slub
- Missing yarn
- Oil mark
- Knot
- Crease
- Color variation
- Weaving/knitting fault

### Recommended dataset

For a serious model, collect labelled fabric images from different:

- Fabric types
- Lighting conditions
- Machine speeds
- Defect sizes
- Camera distances
- Production batches

Each image should have a correct defect label and, for object detection, a bounding box.

## Hackathon Presentation Flow

### Problem

Manual fabric inspection can be slow, inconsistent, and difficult to scale.

### Solution

TexGuard AI uses computer vision to assist textile quality inspectors and highlight suspicious fabric areas.

### Innovation

The project does not stop at defect detection. It connects:

**Detection → Quality Grade → Possible Cause → Corrective Action → Waste Risk → QC Report**

### Future Scope

- Real-time camera inspection
- YOLO/advanced vision model
- Factory database
- Sensor integration
- Machine-condition monitoring
- Predictive maintenance
- Production analytics
- PDF/Excel reports
- Multi-language textile assistant

## Demo Tip

For the hackathon, prepare 3–5 clear fabric images:

1. Good-quality sample
2. Stain sample
3. Hole/open-area sample
4. Uneven-texture sample
5. Broken-yarn/slub sample

Then demonstrate the complete workflow from upload to QC report.

## Author

**Syed Kafeel Ahmed Shah**  
Textile Engineering Student  
Mehran University of Engineering & Technology (MUET)

---

**Hackathon concept:** Textile Engineering + Computer Vision + Quality Control + Industry 4.0 + Sustainability
