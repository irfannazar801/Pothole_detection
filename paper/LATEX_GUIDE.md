# LaTeX Quick Reference for IEEE Paper

## Essential LaTeX Commands

### Document Structure
```latex
\section{Section Name}           % Main section
\subsection{Subsection Name}     % Subsection
\subsubsection{Sub-subsection}   % Sub-subsection (use sparingly)
```

### Text Formatting
```latex
\textbf{Bold text}
\textit{Italic text}
\texttt{Monospace (code)}
\emph{Emphasis}
\underline{Underlined}
```

### Lists
```latex
% Bulleted list
\begin{itemize}
    \item First item
    \item Second item
\end{itemize}

% Numbered list
\begin{enumerate}
    \item First item
    \item Second item
\end{enumerate}
```

### Mathematics

#### Inline Math
```latex
The equation $E = mc^2$ shows...
```

#### Display Math (Numbered)
```latex
\begin{equation}
D_{final} = \alpha \cdot D_{neural} + \beta \cdot D_{geometric}
\end{equation}
```

#### Display Math (Unnumbered)
```latex
\begin{equation*}
y = mx + b
\end{equation*}
```

#### Common Math Symbols
```latex
\alpha, \beta, \gamma          % Greek letters
\sum, \int, \prod              % Operators
\leq, \geq, \neq              % Relations
\cdot, \times, \div           % Multiplication/division
\frac{a}{b}                   % Fraction
x^2, x_i                      % Superscript/subscript
\sqrt{x}                      % Square root
```

### Tables

```latex
\begin{table}[h]
\centering
\caption{Table Title}
\begin{tabular}{@{}lll@{}}
\toprule
\textbf{Column 1} & \textbf{Column 2} & \textbf{Column 3} \\ \midrule
Data 1 & Data 2 & Data 3 \\
Data 4 & Data 5 & Data 6 \\ \bottomrule
\end{tabular}
\label{tab:mylabel}
\end{table}
```

### Figures

```latex
\begin{figure}[t]
\centering
\includegraphics[width=0.48\textwidth]{image.png}
\caption{Figure description}
\label{fig:mylabel}
\end{figure}
```

### Citations and References

```latex
% Cite a reference
This is discussed in \cite{author2023}.

% Multiple citations
Research shows \cite{ref1, ref2, ref3}...

% Reference a figure
As shown in Fig.~\ref{fig:architecture}...

% Reference a table
Table~\ref{tab:results} presents...

% Reference an equation
Equation~(\ref{eq:depth}) defines...
```

### Code Blocks

```latex
\begin{verbatim}
def detect_pothole(image):
    results = model(image)
    return results
\end{verbatim}
```

### URLs and Hyperlinks

```latex
% URL
\url{https://github.com/username/repo}

% Hyperlink with custom text
\href{https://example.com}{Link Text}
```

### Special Characters

```latex
\%    % Percent sign
\$    % Dollar sign
\&    % Ampersand
\_    % Underscore
\#    % Hash
\{    % Left brace
\}    % Right brace
\~{}  % Tilde
```

## IEEE Conference Specific

### Title and Authors

```latex
\title{Your Paper Title\\
{\footnotesize \textsuperscript{*}Note: Optional subtitle}}

\author{
\IEEEauthorblockN{First Author\IEEEauthorrefmark{1}, 
Second Author\IEEEauthorrefmark{2}}
\IEEEauthorblockA{\IEEEauthorrefmark{1}First Institution\\
Email: first@email.com}
\IEEEauthorblockA{\IEEEauthorrefmark{2}Second Institution\\
Email: second@email.com}
}
```

### Multiple Columns

```latex
% Switch to one column (for wide figures/tables)
\begin{figure*}[t]
\centering
\includegraphics[width=0.9\textwidth]{wide_image.png}
\caption{Wide figure spanning both columns}
\end{figure*}
```

### Abstract and Keywords

```latex
\begin{abstract}
Your abstract text here...
\end{abstract}

\begin{IEEEkeywords}
keyword1, keyword2, keyword3
\end{IEEEkeywords}
```

## Common LaTeX Errors and Fixes

### Error: "Undefined control sequence"
**Cause:** Typo in command or missing package
**Fix:** Check spelling, ensure packages loaded in preamble

### Error: "Missing $ inserted"
**Cause:** Math symbols used outside math mode
**Fix:** Wrap in `$...$` or `\begin{equation}...\end{equation}`

### Error: "File not found"
**Cause:** Image file not uploaded or wrong path
**Fix:** Upload file to Overleaf, check filename matches exactly

### Error: "Overfull \hbox"
**Cause:** Text/equation too wide for column
**Fix:** Rephrase text, break equation into multiple lines, or use smaller font

### Warning: "Citation undefined"
**Cause:** Referenced citation not in bibliography
**Fix:** Add to `\begin{thebibliography}`, recompile twice

### Warning: "Reference undefined"
**Cause:** Label referenced before it's defined
**Fix:** Recompile 2-3 times (LaTeX needs multiple passes)

## Overleaf Keyboard Shortcuts

- **Ctrl/Cmd + B**: Bold
- **Ctrl/Cmd + I**: Italic
- **Ctrl/Cmd + /**: Comment/uncomment
- **Ctrl/Cmd + Enter**: Compile
- **Ctrl/Cmd + F**: Find
- **Ctrl/Cmd + Shift + F**: Find and replace

## Best Practices

### 1. Organize with Comments
```latex
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Section 3: System Architecture
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
```

### 2. Consistent Naming
```latex
\label{fig:architecture}    % Figures: fig:
\label{tab:results}         % Tables: tab:
\label{eq:depth}           % Equations: eq:
\label{sec:intro}          % Sections: sec:
```

### 3. Line Breaks for Readability
```latex
% Good - each sentence on new line
This is the first sentence.
This is the second sentence.
This makes version control easier.

% Bad - all on one line
This is the first sentence. This is the second sentence. This makes version control harder.
```

### 4. Use Non-Breaking Spaces
```latex
Fig.~\ref{fig:test}        % ~ prevents line break between Fig. and number
Table~\ref{tab:results}
Section~\ref{sec:intro}
```

### 5. Percentage Formatting
```latex
87.3\%      % Correct - escaped percent
$87.3\%$    % In math mode
```

## Useful Packages (Already Included)

```latex
\usepackage{cite}           % Better citation formatting
\usepackage{amsmath}        % Advanced math
\usepackage{graphicx}       % Images
\usepackage{booktabs}       % Professional tables
\usepackage{hyperref}       % Clickable links
\usepackage{algorithm}      % Algorithms (if needed)
```

## Quick Paper Checklist

Before submission:
- [ ] All author names and affiliations correct
- [ ] Abstract under 250 words
- [ ] All figures have captions and are referenced in text
- [ ] All tables have captions and are referenced in text
- [ ] All equations are numbered and referenced
- [ ] All citations in bibliography
- [ ] No "undefined reference" warnings
- [ ] Compiled without errors
- [ ] Page limit met (usually 6-8 pages for IEEE conferences)
- [ ] Proper copyright notice (if required by conference)
- [ ] PDF generated successfully

## Resources

- **Overleaf Documentation**: https://www.overleaf.com/learn
- **LaTeX Wikibook**: https://en.wikibooks.org/wiki/LaTeX
- **IEEE Templates**: https://www.ieee.org/conferences/publishing/templates.html
- **Detexify** (draw symbol to find LaTeX): http://detexify.kirelabs.org/classify.html
- **Table Generator**: https://www.tablesgenerator.com/

## Getting Help

1. **Overleaf Help**: Click "Help" icon in top-right
2. **Stack Exchange**: https://tex.stackexchange.com/
3. **LaTeX Community**: https://latex.org/forum/

---

**Happy writing! 📝✨**
