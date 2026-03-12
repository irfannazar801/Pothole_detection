# IEEE Conference Paper - Pothole Detection System

This folder contains the IEEE conference paper for the Pothole Detection System using dual neural networks (YOLOv8 + MiDaS).

## Files

- `main.tex` - Main LaTeX source file (IEEE conference format)
- `README.md` - This file

## How to Compile in Overleaf

### Method 1: Direct Upload

1. Go to [Overleaf](https://www.overleaf.com)
2. Click "New Project" → "Upload Project"
3. Upload the `main.tex` file
4. Overleaf will automatically detect IEEE format and compile

### Method 2: Create New Project

1. Create new project: "New Project" → "Blank Project"
2. Name it: "Pothole Detection IEEE Paper"
3. Copy-paste contents of `main.tex` into the editor
4. Click "Recompile"

## Compiler Settings

- **Compiler**: pdfLaTeX (default)
- **TeX Live version**: 2023 or later
- No additional packages needed (all standard IEEE packages)

## Paper Structure

1. **Title & Abstract** - Overview of dual neural network approach
2. **Introduction** - Motivation and contributions
3. **Related Work** - Survey of existing methods
4. **System Architecture** - Detailed technical description
   - YOLOv8 Detection Network
   - MiDaS Depth Network
   - Hybrid Depth Estimation
   - Severity Classification
   - Temporal Tracking
5. **Implementation** - Software architecture and optimizations
6. **Experimental Results** - Performance metrics and comparisons
7. **Discussion** - Advantages, limitations, applications
8. **Conclusion** - Summary and future work
9. **References** - 13 citations

## Customization Guide

### Before Submitting to a Conference

1. **Update Author Information** (Line 21-26):
   ```latex
   \author{\IEEEauthorblockN{Your Name}
   \IEEEauthorblockA{\textit{Your Department} \\
   \textit{Your University}\\
   City, Country \\
   your.email@university.edu}
   }
   ```

2. **Add Conference Information** (if required):
   ```latex
   \title{... \\ 
   {\footnotesize \textsuperscript{*}Paper submitted to IEEE Conference Name 2026}}
   ```

3. **Update GitHub Repository** (Line 440):
   ```latex
   The complete system is open-sourced at \url{https://github.com/yourusername/pothole-detection}
   ```

4. **Add Acknowledgments** (Line 442):
   Update with your actual funding sources, advisors, etc.

### Adding Figures

To add figures (system diagrams, result plots):

```latex
\begin{figure}[t]
\centering
\includegraphics[width=0.48\textwidth]{figures/system_architecture.png}
\caption{Overall system architecture showing dual neural network pipeline.}
\label{fig:architecture}
\end{figure}
```

Upload images to Overleaf and reference them with `\ref{fig:architecture}`.

### Adding More References

Add to the bibliography section (Line 445+):

```latex
\bibitem{newref} Author et al., ``Title,'' Journal, vol. X, no. Y, pp. Z, Year.
```

## Paper Statistics

- **Pages**: 8 (IEEE standard conference length)
- **Words**: ~6,500
- **Sections**: 9 main sections
- **Tables**: 7
- **Equations**: 6
- **References**: 13

## Key Highlights

✅ **Novel Contributions**:
- Dual neural network architecture (YOLOv8 + MiDaS)
- Hybrid depth estimation (60% neural + 40% geometric)
- Real-time performance (10-14 FPS)
- 5-level severity classification

✅ **Strong Results**:
- 87.3% detection precision
- 2.1 cm depth estimation MAE (23% better than MiDaS alone)
- 78.6% severity classification accuracy

✅ **Practical Application**:
- Monocular camera (low cost)
- GPU/CPU support with performance presets
- Open-source implementation

## Target Conferences

This paper is suitable for:

- IEEE International Conference on Computer Vision (ICCV)
- IEEE Conference on Computer Vision and Pattern Recognition (CVPR)
- IEEE Intelligent Transportation Systems Conference (ITSC)
- IEEE International Conference on Robotics and Automation (ICRA)
- IEEE/CVF Winter Conference on Applications of Computer Vision (WACV)

## Compilation Time

- First compilation: ~10-15 seconds
- Subsequent compilations: ~3-5 seconds

## Troubleshooting

**"Undefined control sequence" error:**
- Ensure all packages are loaded in preamble (lines 5-15)
- Check for typos in LaTeX commands

**"File not found" for figures:**
- Upload images to Overleaf in a `figures/` folder
- Use correct file extensions (.png, .pdf, .jpg)

**Bibliography not showing:**
- Recompile 2-3 times (LaTeX needs multiple passes)
- Check `\begin{thebibliography}` section is complete

## Contact

For questions about the paper content, contact: ajith@example.com

For LaTeX/formatting issues, consult: [Overleaf Documentation](https://www.overleaf.com/learn)

---

**Good luck with your paper submission! 🎓📝**
