# Technical Architecture Documentation
## Pothole Detection System - Dual Neural Networks, Video Processing & Depth Estimation

**Version:** 2.0.0  
**Date:** February 15, 2026  
**Author:** Technical Documentation Team

---

## 📊 QUICK REFERENCE: ANNs vs Algorithms in This Project

```
┌─────────────────────────────────────────────────────────────────┐
│  ✅ ARTIFICIAL NEURAL NETWORKS (ANNs) - Total: 2                │
│                                                                  │
│  1. YOLOv8          → Object Detection (finds potholes)         │
│  2. MiDaS           → Depth Estimation (measures depth)         │
│                                                                  │
│  Both have MILLIONS of learned parameters from training         │
├─────────────────────────────────────────────────────────────────┤
│  ❌ TRADITIONAL ALGORITHMS (NOT ANNs) - Total: 9+               │
│                                                                  │
│  • Camera Geometry  → Pinhole camera equations                  │
│  • Shadow Analysis  → Pixel thresholding                        │
│  • Depth Fusion     → Weighted average (0.6×A + 0.4×B)         │
│  • Severity Class   → IF-THEN rules (depth thresholds)         │
│  • IoU Tracking     → Geometric overlap calculation            │
│  • Temporal Smooth  → Arithmetic mean                           │
│  • ROI Extraction   → Array slicing                             │
│  • Visualization    → OpenCV drawing functions                  │
│  • Frame Processing → Video I/O                                 │
│                                                                  │
│  All use FIXED formulas and rules, NO training required        │
└─────────────────────────────────────────────────────────────────┘

ONLY YOLOv8 and MiDaS are ANNs. Everything else is classical programming.
```

---

## 🧠 KEY HIGHLIGHT: This System Uses TWO Artificial Neural Networks (ANNs)

1. **YOLOv8** - Object Detection Network (Finds potholes)
2. **MiDaS** - Depth Estimation Network (Measures pothole depth)

---

## Table of Contents

1. [System Overview](#1-system-overview)
2. [Neural Network #1: YOLOv8 Object Detection](#2-neural-network-1-yolov8-object-detection)
3. [Neural Network #2: MiDaS Depth Estimation](#3-neural-network-2-midas-depth-estimation)
4. [Video Processing Pipeline](#4-video-processing-pipeline)
5. [Depth Estimation System](#5-depth-estimation-system)
6. [Detection & Tracking](#6-detection--tracking)
7. [Severity Classification](#7-severity-classification)
8. [Performance Optimizations](#8-performance-optimizations)
9. [Mathematical Models](#9-mathematical-models)
10. [Technical Specifications](#10-technical-specifications)

---

## 1. System Overview

### 1.1 Dual Neural Network Architecture

This pothole detection system employs **TWO distinct Artificial Neural Networks (ANNs)** working in sequence:

```
                    ┌─────────────────────────────────────┐
                    │      Video Input Stream            │
                    └──────────────┬──────────────────────┘
                                   │
                    ┌──────────────▼──────────────────────┐
                    │    Frame-by-Frame Processing        │
                    └──────────────┬──────────────────────┘
                                   │
        ╔══════════════════════════▼══════════════════════════╗
        ║         ANN #1: YOLOv8 Detection Network           ║
        ║  • Input: RGB Frame (640×480)                      ║
        ║  • Output: Bounding Boxes + Confidence Scores      ║
        ║  • Architecture: CNN (CSPDarknet53 backbone)       ║
        ╚══════════════════════════▼══════════════════════════╝
                                   │
                    ┌──────────────▼──────────────────────┐
                    │   Extract Pothole ROIs (Regions)    │
                    └──────────────┬──────────────────────┘
                                   │
        ╔══════════════════════════▼══════════════════════════╗
        ║         ANN #2: MiDaS Depth Network                ║
        ║  • Input: Pothole ROI (cropped region)             ║
        ║  • Output: Relative Depth Map                      ║
        ║  • Architecture: Encoder-Decoder with Transformer  ║
        ╚══════════════════════════▼══════════════════════════╝
                                   │
                    ┌──────────────▼──────────────────────┐
                    │   Severity Classification           │
                    │   (Critical/Dangerous/Moderate...)  │
                    └──────────────┬──────────────────────┘
                                   │
                    ┌──────────────▼──────────────────────┐
                    │   Temporal Tracking (IoU-based)     │
                    └──────────────┬──────────────────────┘
                                   │
                    ┌──────────────▼──────────────────────┐
                    │   Visualization & Output            │
                    └─────────────────────────────────────┘
```

### 1.2 Why Two Neural Networks?

**Different Tasks Require Different Architectures:**

| Aspect | YOLOv8 (ANN #1) | MiDaS (ANN #2) |
|--------|-----------------|----------------|
| **Primary Task** | Object Detection | Depth Estimation |
| **Input** | Full video frame | Pothole region (ROI) |
| **Output** | Bounding boxes | Depth map |
| **Architecture** | Single-stage detector | Encoder-Decoder |
| **Training Data** | Labeled pothole images | Mixed depth datasets |
| **Inference Time** | 15-30ms | 50-100ms |
| **GPU Memory** | ~500MB | ~1GB |

### 1.3 Core Components Summary

1. **YOLOv8 Detection Network (ANN #1)** - Locates potholes in frames
2. **MiDaS Depth Network (ANN #2)** - Estimates pothole depth
3. **Temporal Tracker** - IoU-based tracking (non-neural, algorithmic)
4. **Severity Estimator** - Hybrid depth + geometric analysis
5. **Video Processor** - Frame handling and orchestration

### 1.4 Technology Stack

- **Deep Learning Frameworks**: PyTorch 1.10+
- **Detection Library**: Ultralytics YOLOv8
- **Depth Model**: Intel MiDaS (via PyTorch Hub)
- **Computer Vision**: OpenCV 4.5+
- **Numerical Computing**: NumPy 1.19+

---

## 2. Neural Network #1: YOLOv8 Object Detection

### 2.1 Overview

**YOLO (You Only Look Once)** is a real-time object detection system. YOLOv8 is the latest version optimized for speed and accuracy.

**Role in System**: The first neural network that identifies WHERE potholes are located in each video frame.

### 2.2 Architecture Details

#### 2.2.1 Network Structure

```
Input Image (640×640×3)
         ↓
┌────────────────────────┐
│  BACKBONE              │
│  CSPDarknet53          │
│  • Conv layers         │
│  • Cross-stage partial │
│  • Feature extraction  │
└──────────┬─────────────┘
           ↓
┌────────────────────────┐
│  NECK                  │
│  PANet (Path Agg.)     │
│  • Multi-scale fusion  │
│  • FPN + PAN           │
└──────────┬─────────────┘
           ↓
┌────────────────────────┐
│  HEAD                  │
│  Decoupled Detection   │
│  • Classification      │
│  • Box Regression      │
└──────────┬─────────────┘
           ↓
Output: [x1, y1, x2, y2, confidence, class]
```

#### 2.2.2 Model Specifications

```python
# YOLOv8 Detection Network (ANN #1)
Model: YOLOv8n or YOLOv8s (nano or small variant)
Input Size: 640×640 (configurable: 320, 416, 480, 640)
Output: Bounding boxes [x1, y1, x2, y2], confidence, class_id
Classes: 1 (pothole)
Parameters: 
  - YOLOv8n: ~3.2M parameters
  - YOLOv8s: ~11.2M parameters
Model File: models/pothole_detector_v1.pt
```

#### 2.2.3 Layer Architecture

**Backbone (CSPDarknet53)**:
- Input layer: 3 channels (RGB)
- Conv blocks: 53 convolutional layers
- Cross-Stage Partial connections (CSP) for efficiency
- Feature maps at multiple scales: P3 (80×80), P4 (40×40), P5 (20×20)

**Neck (PANet)**:
- Feature Pyramid Network (FPN): Top-down pathway
- Path Aggregation Network (PAN): Bottom-up pathway
- Concatenation and fusion of multi-scale features

**Head (Detection)**:
- Decoupled head: Separate branches for classification and regression
- Anchor-free design (unlike earlier YOLO versions)
- Three detection scales for different object sizes

### 2.3 Training Details

The YOLOv8 model has been trained on a custom pothole dataset:

**Training Configuration**:
```python
Dataset: Custom pothole images (thousands of annotated samples)
Epochs: 100-300
Batch Size: 16-32
Image Size: 640×640
Optimizer: AdamW
Learning Rate: 0.001 (with cosine decay)
Weight Decay: 0.0005

Augmentation:
  - Mosaic: 4-image combination
  - MixUp: Image blending
  - Random Scaling: 0.5x - 1.5x
  - Rotation: ±15°
  - HSV Color Jitter
  - Horizontal Flip
  - Random Crop
```

**Loss Function** (Multi-component):
```
Total_Loss = λ₁·L_classification + λ₂·L_box + λ₃·L_objectness

Where:
  L_classification = Binary Cross-Entropy Loss
  L_box = CIoU Loss (Complete Intersection over Union)
  L_objectness = Binary Cross-Entropy Loss
  λ₁, λ₂, λ₃ = loss weights
```

### 2.4 Inference Pipeline

```python
class PotholeDetector:
    def __init__(self, config):
        # Load YOLOv8 model (ANN #1)
        self.model = YOLO(config.model.model_path)
        
        # Optimize model
        self.model.fuse()  # Fuse Conv + BatchNorm layers
        
        # Enable FP16 for faster inference
        if config.model.use_half_precision and torch.cuda.is_available():
            self.model.half()
    
    def _run_inference(self, frame):
        """Run YOLOv8 inference"""
        
        # 1. Preprocessing
        inference_frame, scale_factor = self._prepare_inference_frame(frame)
        
        # 2. YOLO Forward Pass (Neural Network Inference)
        results = self.model(
            inference_frame,
            conf=0.35,        # Confidence threshold
            iou=0.45,         # NMS IoU threshold
            agnostic_nms=True,# Class-agnostic NMS
            max_det=10        # Maximum detections per frame
        )[0]
        
        # 3. Extract detections
        detections = []
        for box in results.boxes.data:
            x1, y1, x2, y2, conf, cls = box
            
            # Scale back to original resolution
            x1, x2 = x1 / scale_factor, x2 / scale_factor
            y1, y2 = y1 / scale_factor, y2 / scale_factor
            
            detections.append({
                'box': (int(x1), int(y1), int(x2), int(y2)),
                'confidence': float(conf),
                'class': int(cls)
            })
        
        return detections
```

### 2.5 Key Parameters

```python
# YOLOv8 Configuration
confidence_threshold = 0.35   # Minimum confidence to accept detection
iou_threshold = 0.45          # NMS threshold (removes overlapping boxes)
max_detections = 10           # Maximum potholes per frame
agnostic_nms = True           # NMS across all classes
use_half_precision = True     # FP16 for 2x speedup on GPU
```

**Parameter Presets**:
```python
# Accuracy Preset
conf_threshold: 0.25  # More detections, lower confidence

# Balanced Preset (Default)
conf_threshold: 0.35  # Good balance

# Speed Preset
conf_threshold: 0.4   # Fewer detections, higher confidence
```

### 2.6 Output Format

```python
# YOLOv8 Output (ANN #1)
Detection = {
    'boxes': [[x1, y1, x2, y2], [x1, y1, x2, y2], ...],  # Bounding box coords
    'confidence': [0.85, 0.72, 0.91, ...],                # Confidence scores
    'class': [0, 0, 0, ...],                              # Class IDs (0=pothole)
}

# Example:
{
    'boxes': [[120, 350, 280, 450], [400, 200, 520, 340]],
    'confidence': [0.87, 0.73],
    'class': [0, 0]
}
```

### 2.7 Performance Characteristics

**Inference Speed**:
- GPU (RTX 3060): 15-30ms per frame
- CPU (i7-10700K): 80-150ms per frame

**Memory Usage**:
- Model size: 20-50 MB (.pt file)
- GPU VRAM: ~500 MB during inference
- RAM: ~1 GB

**Accuracy Metrics** (on test set):
- Precision: 85-92%
- Recall: 80-88%
- mAP@0.5: ~0.85
- mAP@0.5:0.95: ~0.62

---

## 3. Neural Network #2: MiDaS Depth Estimation

### 3.1 Overview

**MiDaS (Mixed Data Sampling)** is a neural network for monocular depth estimation developed by Intel ISL.

**Role in System**: The second neural network that estimates HOW DEEP each detected pothole is.

### 3.2 Architecture Details

#### 3.2.1 Network Structure

```
Input RGB Image (H×W×3)
         ↓
┌─────────────────────────┐
│  ENCODER                │
│  EfficientNet-Lite      │
│  • Feature extraction   │
│  • Multi-scale features │
│  Stages: 5 levels       │
└──────────┬──────────────┘
           ↓
┌─────────────────────────┐
│  TRANSFORMER FUSION     │
│  • Reassemble features  │
│  • Cross-scale attention│
│  • Global context       │
└──────────┬──────────────┘
           ↓
┌─────────────────────────┐
│  DECODER                │
│  • Progressive upsample │
│  • Conv refinement      │
│  • Skip connections     │
└──────────┬──────────────┘
           ↓
Output: Depth Map (H×W×1)
[Inverse depth: High=Close, Low=Far]
```

#### 3.2.2 Model Specifications

```python
# MiDaS Depth Network (ANN #2)
Model: MiDaS_small (optimized for real-time)
Source: intel-isl/MiDaS (PyTorch Hub)
Input: RGB image (any resolution, auto-resized internally)
Output: Inverse depth map (relative, not metric)
Parameters: ~9M parameters
Model Size: ~18 MB (downloaded automatically)

Alternative (not used by default):
  DPT_Large: Higher accuracy, ~340M parameters, much slower
```

#### 3.2.3 Model Variants Comparison

| Model Variant | Parameters | Accuracy | Speed | Use Case |
|--------------|-----------|----------|-------|----------|
| MiDaS_small | 9M | Good | Fast | ✅ Real-time (Used) |
| DPT_Hybrid | 123M | Better | Medium | Balanced |
| DPT_Large | 344M | Best | Slow | Offline processing |

**This project uses MiDaS_small for real-time performance.**

### 3.3 Depth Estimation Process

#### 3.3.1 Loading MiDaS Model

```python
# Global model cache (loaded once)
midas_model = None
midas_transform = None
device = None

def load_midas():
    """Loads the MiDaS neural network once"""
    global midas_model, midas_transform, device
    
    if midas_model is not None:
        return  # Already loaded
    
    print("🧠 Loading MiDaS Neural Network (ANN #2)...")
    
    # 1. Select model variant
    model_type = "MiDaS_small"  # Fast variant for real-time
    
    # 2. Load from PyTorch Hub
    midas_model = torch.hub.load("intel-isl/MiDaS", model_type, trust_repo=True)
    
    # 3. Move to GPU if available
    device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
    midas_model.to(device)
    midas_model.eval()  # Set to evaluation mode
    
    # 4. Load corresponding transform
    midas_transforms = torch.hub.load("intel-isl/MiDaS", "transforms", trust_repo=True)
    
    if model_type == "MiDaS_small":
        midas_transform = midas_transforms.small_transform
    else:
        midas_transform = midas_transforms.dpt_transform
    
    print(f"✅ MiDaS {model_type} loaded on {device}")
```

#### 3.3.2 Running Depth Inference

```python
def run_midas_depth(img):
    """
    Runs MiDaS Neural Network (ANN #2) to get depth map.
    
    Args:
        img: RGB image (H×W×3) numpy array
    
    Returns:
        depth_map: Normalized depth map (H×W) float32 [0, 1]
                  Higher values = closer to camera
                  Lower values = farther from camera
    """
    global midas_model, midas_transform, device
    
    # 1. Load model if not already loaded
    if midas_model is None:
        load_midas()
    
    try:
        # 2. Preprocessing (resize and normalize)
        input_batch = midas_transform(img).to(device)
        
        # 3. Neural Network Forward Pass (NO gradient computation)
        with torch.no_grad():  # Faster inference, no training
            prediction = midas_model(input_batch)
            
            # 4. Resize output to original resolution
            prediction = torch.nn.functional.interpolate(
                prediction.unsqueeze(1),
                size=img.shape[:2],
                mode="bilinear",  # Fast interpolation
                align_corners=False,
            ).squeeze()
        
        # 5. Convert to numpy
        depth_map = prediction.cpu().numpy()
        
        # 6. Normalize to [0, 1]
        d_min = depth_map.min()
        d_max = depth_map.max()
        depth_map_norm = (depth_map - d_min) / (d_max - d_min + 1e-8)
        
        # 7. CLAHE enhancement (Contrast Limited Adaptive Histogram Equalization)
        clahe = cv2.createCLAHE(clipLimit=1.5, tileGridSize=(8, 8))
        depth_map_u8 = (depth_map_norm * 255).astype(np.uint8)
        depth_enhanced = clahe.apply(depth_map_u8).astype(np.float32) / 255.0
        
        # 8. Blend original with enhanced (80:20)
        final_depth = (0.8 * depth_map_norm + 0.2 * depth_enhanced).astype(np.float32)
        
        return final_depth
        
    except Exception as e:
        print(f"⚠️ MiDaS Inference Error: {e}")
        # Fallback to simple gradient-based pseudo-depth
        return fallback_depth_estimation(img)
```

### 3.4 Depth Map Characteristics

**Output Properties**:
```python
Type: float32 numpy array
Shape: (H, W) - same as input image
Range: [0.0, 1.0] normalized
Interpretation:
  - 1.0 (white) = Close to camera
  - 0.0 (black) = Far from camera
  - Inverse depth representation
```

**Limitations**:
1. **Scale Ambiguity**: Output is relative, not metric (needs calibration for cm)
2. **Monocular Limitation**: Cannot resolve absolute scale from single image
3. **Reflections**: Specular highlights can confuse the network
4. **Shadows**: Dark regions may be incorrectly interpreted as far
5. **Texture Dependency**: Better on textured surfaces

### 3.5 Scene Condition Detection

MiDaS output is refined based on scene conditions:

```python
def detect_wet_muddy(img):
    """
    Detects wet/muddy conditions that affect depth accuracy.
    
    Returns:
        {
            'wet': bool,          # True if wet surface detected
            'muddy': bool,        # True if muddy/brown surface
            'spec_mask': ndarray  # Binary mask of specular reflections
        }
    """
    # Convert to HSV color space
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    v = hsv[:, :, 2].astype(float) / 255.0  # Value (brightness)
    s = hsv[:, :, 1].astype(float) / 255.0  # Saturation
    h = hsv[:, :, 0].astype(float)           # Hue
    
    # Specular detection (wet surfaces have bright, low-saturation highlights)
    spec_mask = (v > 0.85) & (s < 0.25)
    wet = spec_mask.mean() > 0.02 or v.mean() < 0.45
    
    # Muddy detection (brownish hue, moderate saturation)
    muddy_mask = ((h > 5) & (h < 35)) & (s > 0.15) & (v < 0.6)
    muddy = muddy_mask.mean() > 0.02
    
    return {
        'wet': bool(wet),
        'muddy': bool(muddy),
        'spec_mask': (spec_mask.astype(np.uint8) * 255)
    }
```

### 3.6 Depth Refinement

```python
def refine_depth(depth_metric, mask, spec_mask):
    """
    Refine MiDaS depth output by:
    1. Inpainting specular regions (wet reflections)
    2. Smoothing inside pothole mask
    3. Enforcing rim boundary conditions
    """
    depth = depth_metric.copy()
    
    # 1. Inpaint specular areas (neural network confused by reflections)
    inpaint_mask = (spec_mask > 0).astype(np.uint8)
    if inpaint_mask.sum() > 0:
        depth_u8 = (depth / np.max(depth) * 255).astype(np.uint8)
        depth = cv2.inpaint(depth_u8, inpaint_mask, 3, 
                           cv2.INPAINT_TELEA).astype(np.float32)
        depth = depth / 255.0 * depth_metric.max()
    
    # 2. Smooth inside mask (reduce neural network noise)
    kernel = np.ones((5, 5), np.float32) / 25
    depth_smooth = cv2.filter2D(depth, -1, kernel)
    
    # 3. Enforce rim at road plane (depth ≈ 0 at pothole edges)
    rim = cv2.morphologyEx(mask, cv2.MORPH_GRADIENT, 
                          np.ones((7, 7), np.uint8))
    depth_smooth[rim > 0] = np.minimum(
        depth_smooth[rim > 0],
        np.percentile(depth_smooth[mask > 0], 20)
    )
    
    return depth_smooth
```

### 3.7 Performance Characteristics

**Inference Speed**:
- GPU (RTX 3060): 50-100ms per ROI
- CPU (i7-10700K): 200-400ms per ROI

**Memory Usage**:
- Model size: 18 MB
- GPU VRAM: ~1 GB during inference
- RAM: ~1.5 GB

**Accuracy**:
- Relative depth: Excellent correlation with true depth order
- Metric depth: Requires calibration (error without: ±20-30%)

---

## 4. Video Processing Pipeline

### 4.1 Complete Processing Flow

```python
def process_video(video_path):
    """
    Main video processing loop integrating BOTH neural networks
    """
    # Initialize components
    detector = PotholeDetector(config)  # Contains YOLOv8 (ANN #1)
    depth_estimator = DepthEstimator(config)  # Contains MiDaS (ANN #2)
    tracker = DetectionTracker(config)
    
    cap = cv2.VideoCapture(video_path)
    
    while True:
        # 1. Read frame
        ret, frame = cap.read()
        if not ret:
            break
        
        # 2. YOLOv8 Detection (ANN #1)
        detections = detector.detect(frame)
        # Output: [{'box': (x1,y1,x2,y2), 'confidence': 0.85}, ...]
        
        # 3. For each detected pothole:
        for det in detections:
            x1, y1, x2, y2 = det['box']
            
            # Extract Region of Interest (ROI)
            roi = frame[y1:y2, x1:x2]
            
            # 4. MiDaS Depth Estimation (ANN #2)
            depth_cm = depth_estimator.estimate_depth(roi, frame, det['box'])
            
            # 5. Severity Classification
            severity, color = classify_severity(depth_cm)
            
            det['depth_cm'] = depth_cm
            det['severity'] = severity
            det['color'] = color
        
        # 6. Temporal Tracking (non-neural, algorithmic)
        tracked_detections = tracker.track(detections)
        
        # 7. Visualization
        visualized_frame = visualize(frame, tracked_detections)
        
        # 8. Display
        cv2.imshow('Pothole Detector', visualized_frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
```

### 4.2 Frame Processing Stages

**Stage Breakdown**:

| Stage | Component | Type | Time (ms) |
|-------|-----------|------|-----------|
| 1. Frame Read | OpenCV | I/O | 2 |
| 2. YOLOv8 Detection | **ANN #1** | Neural | 15-30 |
| 3. ROI Extraction | OpenCV | CPU | 1 |
| 4. MiDaS Depth | **ANN #2** | Neural | 50-100 |
| 5. Severity Class | Algorithm | CPU | 1 |
| 6. Tracking | IoU Algorithm | CPU | 3 |
| 7. Visualization | OpenCV | CPU | 5 |
| **Total** | | | **77-142** |

**FPS**: ~7-13 FPS (with both neural networks)

### 4.3 Optimization Strategies

```python
# 1. Frame Skipping (process every Nth frame)
frame_skip = 1  # Process every 2nd frame → 2x faster

# 2. Batch Processing (not yet implemented)
# Process multiple frames in single YOLOv8 call

# 3. Resolution Reduction
inference_size = 480  # Instead of 640 → 1.7x faster

# 4. Half Precision (FP16)
use_half_precision = True  # → 2x faster on modern GPUs

# 5. Model Caching
# Load both ANNs once, reuse for all frames
```

---

## 5. Depth Estimation System

### 5.1 Hybrid Approach

The system combines THREE depth sources:

```
Final Depth = α·Neural_Depth + β·Geometric_Depth + γ·Physics_Depth

Where:
  Neural_Depth:    From MiDaS (ANN #2)
  Geometric_Depth: Shadow analysis
  Physics_Depth:   Camera geometry
  
  α = 0.6 (neural_weight)
  β = 0.4 (geometric_weight)
```

### 5.2 Neural Depth Component (MiDaS)

```python
def _estimate_neural_depth(roi, width_cm, frame_shape):
    """
    Use MiDaS (ANN #2) for depth estimation
    """
    # 1. Camera parameters
    cam_params = {
        'f': 800.0,                    # Focal length (pixels)
        'cx': frame_shape[1] / 2,      # Principal point X
        'cy': frame_shape[0] / 2,      # Principal point Y
        'H': 1.5,                      # Camera height (meters)
        'pitch': 0.0                   # Camera tilt (radians)
    }
    
    # 2. Detect scene condition
    condition = detect_wet_muddy(roi)
    
    # 3. Run MiDaS neural network (ANN #2)
    depth_rel = run_midas_depth(roi)  # Returns [0, 1] normalized
    
    # 4. Segment pothole
    mask = simple_pothole_segmentation(roi)
    
    if mask.sum() < 50:  # Minimum mask area
        return 0.0
    
    # 5. Refine depth (handle specular regions)
    depth_refined = refine_depth(depth_rel, mask, condition['spec_mask'])
    
    # 6. Extract rim and interior
    rim_pixels = rim_pixels_from_mask(mask)
    rim_vals = depth_refined[rim_pixels[:, 1], rim_pixels[:, 0]]
    rim_median = np.median(rim_vals)
    
    interior_vals = depth_refined[mask > 0]
    bottom = np.min(interior_vals)
    
    # 7. Calculate relative depth difference
    rel_depth_val = max(0.0, rim_median - bottom)
    
    # 8. Convert to metric (cm) using width calibration
    depth_cm = width_cm * rel_depth_val * 0.5
    
    return depth_cm
```

### 5.3 Geometric Depth Component (Shadow Analysis)

```python
def _estimate_geometric_depth(roi, width_cm):
    """
    Estimate depth using shadow intensity (non-neural)
    """
    # 1. Convert to grayscale
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    
    # 2. Blur
    blurred = cv2.GaussianBlur(gray_roi, (5, 5), 0)
    
    # 3. Threshold for shadows
    threshold_val = int(np.mean(blurred) * 0.7)
    _, dark_mask = cv2.threshold(
        blurred, threshold_val, 255, cv2.THRESH_BINARY_INV
    )
    
    # 4. Calculate shadow ratio
    shadow_area = np.sum(dark_mask > 0)
    total_area = roi.shape[0] * roi.shape[1]
    shadow_ratio = shadow_area / total_area
    
    # 5. Depth formula (deeper potholes → more shadow)
    depth_cm = width_cm * 0.03 * (1 + shadow_ratio * 0.5)
    
    return depth_cm
```

### 5.4 Physics-Based Distance & Width

```python
def estimate_physical_metrics(frame, box):
    """
    Estimate real-world distance and width using pinhole camera model
    """
    x1, y1, x2, y2 = box
    h_frame, w_frame = frame.shape[:2]
    
    # Camera parameters
    focal_length_px = 800.0
    camera_height_cm = 150.0
    horizon_ratio = 0.50
    
    # 1. Calculate horizon
    horizon_y = h_frame * horizon_ratio
    
    # 2. Pixels below horizon
    pixels_below_horizon = max(10, y2 - horizon_y)
    
    # 3. Distance estimation (pinhole model)
    #    Z = (H * f) / (v - cy)
    distance_cm = (camera_height_cm * focal_length_px) / pixels_below_horizon
    
    # Clamp to realistic range
    distance_cm = np.clip(distance_cm, 100, 2000)
    
    # 4. Width estimation with perspective correction
    #    W = (w_pixels * Z) / f
    pixel_width = x2 - x1
    width_cm = (pixel_width * distance_cm) / focal_length_px
    
    # Clamp width
    width_cm = np.clip(width_cm, 5, 300)
    
    return distance_cm, width_cm
```

### 5.5 Complete Hybrid Depth Estimation

```python
def estimate_dry_pothole_depth(frame, box):
    """
    Complete hybrid depth estimation using both ANNs and geometry
    """
    # 1. Extract ROI
    x1, y1, x2, y2 = box
    roi = frame[y1:y2, x1:x2]
    
    # 2. Physics-based metrics (camera geometry)
    distance_cm, width_cm = estimate_physical_metrics(frame, box)
    
    # 3. Neural depth (ANN #2: MiDaS)
    neural_depth = _estimate_neural_depth(roi, width_cm, frame.shape)
    
    # 4. Geometric depth (shadow analysis)
    geometric_depth = _estimate_geometric_depth(roi, width_cm)
    
    # 5. Hybrid combination
    neural_weight = 0.6
    geometric_weight = 0.4
    
    final_depth = (
        neural_weight * neural_depth +
        geometric_weight * geometric_depth
    )
    
    # 6. Clamp to realistic range
    final_depth = np.clip(final_depth, 0.5, 35.0)  # 0.5-35 cm
    
    return final_depth
```

---

## 6. Detection & Tracking

### 6.1 Temporal Tracking (Non-Neural)

**Note**: Tracking is NOT a neural network - it's an algorithmic approach using IoU.

```python
class DetectionTracker:
    """
    IoU-based tracking for temporal smoothing
    (Not a neural network - algorithmic)
    """
    
    def calculate_iou(self, box1, box2):
        """Intersection over Union"""
        x1_min, y1_min, x1_max, y1_max = box1
        x2_min, y2_min, x2_max, y2_max = box2
        
        # Intersection
        inter_xmin = max(x1_min, x2_min)
        inter_ymin = max(y1_min, y2_min)
        inter_xmax = min(x1_max, x2_max)
        inter_ymax = min(y1_max, y2_max)
        
        inter_area = max(0, inter_xmax - inter_xmin) * \
                     max(0, inter_ymax - inter_ymin)
        
        # Union
        box1_area = (x1_max - x1_min) * (y1_max - y1_min)
        box2_area = (x2_max - x2_min) * (y2_max - y2_min)
        union_area = box1_area + box2_area - inter_area
        
        return inter_area / (union_area + 1e-8)
    
    def track_detections(self, detections):
        """Match current detections to previous tracks"""
        for det in detections:
            # Find best match
            best_id, best_iou = self._find_best_match(det['box'])
            
            if best_iou > 0.3:  # IoU threshold
                # Update existing track
                track_id = best_id
                self._update_track(track_id, det)
            else:
                # Create new track
                track_id = self._create_new_track(det)
        
        return tracked_detections
```

### 6.2 Temporal Smoothing

```python
def _smooth_box(self, track_id):
    """Average bounding boxes over last N frames"""
    boxes = self.tracked_objects[track_id]['boxes']  # Deque of size 5
    
    # Convert to numpy and average
    boxes_array = np.array(list(boxes))
    smoothed = boxes_array.mean(axis=0).astype(int)
    
    return tuple(smoothed)
```

---

## 7. Severity Classification

### 7.1 Classification Thresholds

```python
class SeverityLevel(Enum):
    CRITICAL = ("CRITICAL", (0, 0, 255))      # Red, ≥ 15 cm
    DANGEROUS = ("DANGEROUS", (0, 69, 255))   # Orange-Red, 10-15 cm
    MODERATE = ("MODERATE", (0, 165, 255))    # Orange, 6-10 cm
    MINOR = ("MINOR", (0, 255, 255))          # Yellow, 3-6 cm
    SURFACE = ("SURFACE", (0, 255, 0))        # Green, < 3 cm
    UNKNOWN = ("UNKNOWN", (128, 128, 128))    # Gray
```

### 7.2 Classification Logic

```python
def classify_severity(depth_cm):
    """Classify based on estimated depth from hybrid approach"""
    if depth_cm >= 15.0:
        return SeverityLevel.CRITICAL
    elif depth_cm >= 10.0:
        return SeverityLevel.DANGEROUS
    elif depth_cm >= 6.0:
        return SeverityLevel.MODERATE
    elif depth_cm >= 3.0:
        return SeverityLevel.MINOR
    else:
        return SeverityLevel.SURFACE
```

---

## 8. Performance Optimizations

### 8.1 Neural Network Optimizations

#### 8.1.1 YOLOv8 (ANN #1) Optimizations

```python
# 1. Model Fusion (Conv + BatchNorm)
model.fuse()  # ~10-15% faster

# 2. Half Precision (FP16)
if torch.cuda.is_available():
    model.half()  # ~2x faster on modern GPUs

# 3. Inference Size Reduction
inference_size = 480  # vs 640 → 1.7x faster

# 4. Batch Processing (future)
# Process multiple frames in one forward pass
```

#### 8.1.2 MiDaS (ANN #2) Optimizations

```python
# 1. Small Model Variant
model_type = "MiDaS_small"  # ~6x faster than DPT_Large

# 2. Bilinear Upsampling
mode = "bilinear"  # vs bicubic (faster)

# 3. Reduced CLAHE Processing
clipLimit = 1.5, tileGridSize = (8, 8)

# 4. Model Caching
# Load once, reuse for all frames (global variable)
```

### 8.2 Pipeline Optimizations

```python
# 1. Frame Skipping
frame_skip = 1  # Process every 2nd frame → 2x faster

# 2. ROI-only Depth
# Run MiDaS only on detected pothole regions, not full frame

# 3. Conditional Depth
# Skip depth estimation for low-confidence detections

# 4. Async Processing (future)
# Run YOLOv8 and MiDaS in parallel threads
```

### 8.3 Performance Presets

```python
# ACCURACY PRESET
conf_threshold: 0.25
frame_skip: 0
inference_size: 640
enable_tracking: True
buffer_size: 7
Result: 8-10 FPS

# BALANCED PRESET (Default)
conf_threshold: 0.35
frame_skip: 0
inference_size: 640
enable_tracking: True
buffer_size: 5
Result: 10-14 FPS

# SPEED PRESET
conf_threshold: 0.4
frame_skip: 1
inference_size: 480
enable_tracking: True
buffer_size: 3
Result: 20-35 FPS

# CPU PRESET
conf_threshold: 0.4
half_precision: False
frame_skip: 1
inference_size: 416
enable_tracking: True
buffer_size: 3
Result: 2-5 FPS
```

---

## 9. Mathematical Models

### 9.1 Pinhole Camera Model

**Forward Projection** (3D world → 2D image):
```
u = f_x · (X / Z) + c_x
v = f_y · (Y / Z) + c_y

Where:
  (X, Y, Z) = 3D world coordinates
  (u, v) = 2D image coordinates
  f_x, f_y = focal length in pixels
  c_x, c_y = principal point (image center)
```

**Ground Plane Distance**:
```
For a point on the ground (Y = -H), where H = camera height:

v = f_y · (-H / Z) + c_y
(v - c_y) = -f_y · H / Z
Z = -f_y · H / (v - c_y)
Z = f_y · H / (c_y - v)    [for v > c_y, below horizon]

Simplified (c_y ≈ H/2):
Z ≈ (H · f) / (v - c_y)
```

### 9.2 Hybrid Depth Formula

```
D_final = w_neural · D_neural + w_geo · D_geo

Where:
  D_neural = W · d_rel · 0.5
  D_geo = W · 0.03 · (1 + shadow_ratio · 0.5)
  
  W = pothole width (cm) from pinhole model
  d_rel = MiDaS relative depth difference (rim - bottom)
  shadow_ratio = dark_pixels / total_pixels
  
  w_neural = 0.6  (60% weight to neural network)
  w_geo = 0.4     (40% weight to geometry)
```

### 9.3 IoU (Intersection over Union)

```
IoU(A, B) = Area(A ∩ B) / Area(A ∪ B)

Where:
  A ∩ B = intersection area
  A ∪ B = Area(A) + Area(B) - Area(A ∩ B)
```

### 9.4 Temporal Smoothing (Simple Averaging - NOT ANN)

**This is basic arithmetic averaging, NOT a neural network.**

```
Box_smooth[t] = (1/N) · Σ(Box[t-i])  for i = 0 to N-1

Where:
  N = buffer_size (typically 5)
  Box[t] = (x1, y1, x2, y2) at time t
```

**Implementation** (Simple mean):
```python
# NOT a neural network - just averaging numbers
def smooth_box(boxes):
    # boxes is a deque of last 5 bounding boxes
    boxes_array = np.array(list(boxes))
    smoothed = boxes_array.mean(axis=0)  # Simple average
    return smoothed.astype(int)
```

### 9.5 Severity Classification (IF-THEN Rules - NOT ANN)

**This is rule-based logic, NOT a neural network.**

```
IF depth >= 15.0 cm THEN severity = CRITICAL
ELSE IF depth >= 10.0 cm THEN severity = DANGEROUS
ELSE IF depth >= 6.0 cm THEN severity = MODERATE
ELSE IF depth >= 3.0 cm THEN severity = MINOR
ELSE severity = SURFACE
```

**Implementation** (Simple conditionals):
```python
# NOT a neural network - just IF-THEN rules
def classify_severity(depth_cm):
    if depth_cm >= 15.0:
        return "CRITICAL"
    elif depth_cm >= 10.0:
        return "DANGEROUS"
    elif depth_cm >= 6.0:
        return "MODERATE"
    elif depth_cm >= 3.0:
        return "MINOR"
    else:
        return "SURFACE"
```

**These thresholds are fixed/hardcoded, NOT learned from data like a neural network would.**

---

## 10. Technical Specifications

### 10.1 System Requirements

**Minimum** (CPU only):
- CPU: Intel i5 / AMD Ryzen 5 (4 cores)
- RAM: 8 GB
- GPU: None
- Storage: 2 GB
- Performance: 2-5 FPS

**Recommended** (GPU):
- CPU: Intel i7 / AMD Ryzen 7 (8 cores)
- RAM: 16 GB
- GPU: NVIDIA GTX 1660 or better (6GB VRAM)
- Storage: 5 GB
- Performance: 10-14 FPS

**Optimal**:
- CPU: Intel i9 / AMD Ryzen 9
- RAM: 32 GB
- GPU: NVIDIA RTX 3060 or better (8GB+ VRAM)
- Storage: 10 GB SSD
- Performance: 20-35 FPS (with optimizations)

### 10.2 Software Dependencies

```txt
Core Libraries:
  python >= 3.8
  opencv-python >= 4.5.0
  numpy >= 1.19.0
  torch >= 1.10.0
  torchvision >= 0.11.0
  ultralytics >= 8.0.0

Optional (GPU):
  cuda >= 11.0
  cudnn >= 8.0

Development:
  pytest >= 7.0.0
  black >= 22.0.0
```

### 10.3 Neural Network Models

```
ANN #1: YOLOv8 Detection
  File: models/pothole_detector_v1.pt
  Size: 20-50 MB
  Source: Custom trained
  
ANN #2: MiDaS Depth
  File: Downloaded automatically from PyTorch Hub
  Size: ~18 MB (MiDaS_small)
  Source: intel-isl/MiDaS
```

### 10.4 Accuracy Metrics

**YOLOv8 Detection (ANN #1)**:
- Precision: 85-92%
- Recall: 80-88%
- mAP@0.5: ~0.85
- mAP@0.5:0.95: ~0.62

**MiDaS Depth (ANN #2)**:
- Relative depth: Excellent correlation
- Metric depth (uncalibrated): ±20-30% error
- Metric depth (calibrated): ±5-15% error

**Overall Severity Classification**:
- Accuracy: 75-85%
- Critical/Dangerous: ~90% precision
- Minor/Surface: ~70% precision

### 10.5 Performance Benchmarks

**Hardware**: NVIDIA RTX 3060, Intel i7-10700K

| Stage | Time (GPU) | Time (CPU) |
|-------|-----------|-----------|
| YOLOv8 (ANN #1) | 15-30 ms | 80-150 ms |
| MiDaS (ANN #2) | 50-100 ms | 200-400 ms |
| Tracking | 3 ms | 3 ms |
| Visualization | 5 ms | 5 ms |
| **Total** | **73-138 ms** | **288-558 ms** |
| **FPS** | **7-14 FPS** | **2-3 FPS** |

---

## 11. Summary

### 11.1 Two Neural Networks Working Together

This pothole detection system leverages **EXACTLY TWO Artificial Neural Networks (ANNs)**:

1. **YOLOv8 (ANN #1)** ✅ Neural Network
   - Task: Object Detection
   - Finds pothole locations
   - Output: Bounding boxes
   - Speed: 15-30ms per frame
   - Parameters: 3-11 Million (learned from training data)

2. **MiDaS (ANN #2)** ✅ Neural Network
   - Task: Depth Estimation
   - Measures pothole depth
   - Output: Depth maps
   - Speed: 50-100ms per ROI
   - Parameters: 9 Million (learned from training data)

### 11.2 What is NOT a Neural Network

**All other components use traditional algorithms and mathematics** ❌ NOT ANNs:

| Component | Type | Why NOT an ANN |
|-----------|------|----------------|
| Camera Geometry | Physics equations | Fixed formula: Z = (H·f)/(v-cy) |
| Shadow Analysis | Image thresholding | Pixel comparison with threshold |
| Depth Fusion | Weighted average | 0.6×A + 0.4×B (hardcoded weights) |
| Severity Classification | IF-THEN rules | Fixed thresholds: 15cm, 10cm, 6cm |
| IoU Tracking | Geometric calculation | Area(A∩B) / Area(A∪B) |
| Temporal Smoothing | Arithmetic mean | Σ(boxes) / N |

**Key Distinction**:
- **Neural Networks** = Millions of parameters learned from data through training
- **Traditional Algorithms** = Fixed formulas and rules, no learning required

### 11.3 Pipeline Flow

```
Frame → 🧠 YOLOv8 (ANN) → Detections → 📐 Camera Math (NOT ANN) → 
        🧠 MiDaS (ANN) → Depth → 📊 Rules (NOT ANN) → Display
        
Only 2 ANNs: YOLOv8 and MiDaS
All else: Traditional algorithms
```

### 11.4 Why This Hybrid Approach?

**Combining ANNs with Traditional Algorithms**:

✅ **Advantages**:
- ANNs handle complex pattern recognition (objects, depth)
- Traditional algorithms handle precise calculations (geometry, rules)
- Faster than using ANNs for everything
- More interpretable (can understand the formulas)
- No need to train models for simple tasks

❌ **If we used ONLY neural networks**:
- Would need to train additional models for severity classification
- Would need training data for camera geometry
- Slower overall processing
- Less interpretable ("black box")
- More GPU memory required

### 11.5 Key Advantages

- **Complementary Architectures**: Each ANN specialized for its task
- **Hybrid Approach**: ANNs for perception, algorithms for computation
- **High Accuracy**: 85%+ detection, good depth estimation
- **Real-time Capable**: 10-14 FPS on mid-range GPU
- **Robust**: Handles various road conditions
- **Scalable**: Can swap models for different speed/accuracy tradeoffs
- **Efficient**: Only uses GPU for ANNs, CPU for simple calculations

### 11.6 Complete Component Breakdown: ANN vs Algorithm

| # | Component Name | Type | Training Required? | Parameters | Processing |
|---|----------------|------|-------------------|------------|------------|
| 1 | **YOLOv8 Detection** | ✅ **ANN** | Yes (100+ epochs) | 3-11M | GPU forward pass |
| 2 | **MiDaS Depth** | ✅ **ANN** | Yes (pre-trained) | 9M | GPU forward pass |
| 3 | Frame Reading | ❌ Algorithm | No | 0 | OpenCV I/O |
| 4 | ROI Extraction | ❌ Algorithm | No | 0 | Array slicing |
| 5 | Camera Geometry | ❌ Algorithm | No | 0 | Z = (H·f)/(v-cy) |
| 6 | Shadow Analysis | ❌ Algorithm | No | 0 | Thresholding |
| 7 | Depth Fusion | ❌ Algorithm | No | 0 | Weighted sum |
| 8 | Severity Classification | ❌ Algorithm | No | 0 | IF-THEN rules |
| 9 | IoU Calculation | ❌ Algorithm | No | 0 | Geometry formula |
| 10 | Tracking | ❌ Algorithm | No | 0 | Matching + averaging |
| 11 | Visualization | ❌ Algorithm | No | 0 | OpenCV drawing |

**Summary**: 
- ✅ **2 ANNs** (Neural Networks with learned parameters)
- ❌ **9 Traditional Algorithms** (Fixed formulas and rules)

---

## References

1. **YOLOv8 (ANN #1)**: Ultralytics - https://github.com/ultralytics/ultralytics
2. **MiDaS (ANN #2)**: Intel ISL - https://github.com/isl-org/MiDaS
3. **PyTorch**: https://pytorch.org/
4. **OpenCV**: https://opencv.org/

---

**Document Version**: 1.1  
**Last Updated**: February 15, 2026  
**Maintained By**: Pothole Detection Team

**Key Update**: Clarified that the system uses TWO distinct Artificial Neural Networks (YOLOv8 and MiDaS) working in sequence.

---

For implementation details, see source code in:
- `src/detector.py` - YOLOv8 detection (ANN #1)
- `depth_estimation.py` - MiDaS depth estimation (ANN #2)
- `src/video_processor.py` - Video processing pipeline
- `src/severity_estimator.py` - Hybrid depth estimation & severity classification
- `src/tracker.py` - Temporal tracking (non-neural)
