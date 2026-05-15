% Style file for one column research/project reports

\NeedsTeXFormat{LaTeX2e}[1994/06/01]
\ProvidesClass{practical-report}[2023/07/18 v.1.0]

%====================================================================
%===================== release notes ================================

% 2023-07-18: v1.0

%======================= Outline ====================================
%====================================================================

% OUTLINE OF THIS CLASS FILE
%   option declarations
%   required packages
%   bibliography, links and color
%   metadata
%   page dimensions
%   title
%   sectioning
%   footnotes
%   other environments

%=====================================================================
%======================== option declarations ========================

\DeclareOption*{\PassOptionsToClass{\CurrentOption}{article}}

\ProcessOptions\relax
\LoadClass[11pt,oneside]{article}



%=====================================================================
%============================= typography ============================

% Left alignment
\RequirePackage[document]{ragged2e}

% amsmath must be loaded before unicode-math
\RequirePackage[leqno,tbtags]{amsmath}
\RequirePackage{unicode-math}

% Set main serif fonts
\setmainfont{Equity A}[Numbers={Lowercase,Proportional}, Contextuals=Alternate, SmallCapsFeatures={LetterSpace=3, Renderer=Basic}]
\newcommand\liningfont{\addfontfeatures{Numbers={Uppercase, Proportional}}}
\newfontfamily{\rmsc}{Equity A Caps}[Letters=UppercaseSmallCaps, Numbers={Uppercase,Proportional}, SmallCapsFeatures={LetterSpace=3, Renderer=Basic}]
\newfontfamily{\rmcs}{Equity A Caps}[Numbers={Uppercase,Proportional}]

% IPA, monospace, and math fonts
\newfontfamily{\ipa}{Charis SIL}
\setmonofont[Scale=MatchLowercase]{Triplicate A Code}
\setmathfont[Path=/Users/venkat/Library/Fonts/, Extension=.otf,Scale=MatchLowercase,Ligatures=TeX, BoldFont=XCharter-Bold,
    ItalicFont=XCharter-Italic, Numbers={Uppercase,Monospaced}]{XCharter-Roman}

% Oldstyle tabular numbers inside tabular environment
\AtBeginEnvironment{tabular}{\addfontfeatures{Numbers={Uppercase, Monospaced}}\small}
\renewcommand{\theequation}{ {\addfontfeatures{Numbers={Uppercase, Monospaced}}\small\arabic{equation}}}

% Set linespacing to 1.1 times the point size
\RequirePackage{setspace}
\setstretch{1.1}

% Strong widow and orphan control - avoid any widows and orphans
\clubpenalty10000
\widowpenalty10000

% French Spacing - single spacing between sentences
\frenchspacing

%=====================================================================
%========================= required packages =========================

% For quotes
\RequirePackage{csquotes}

% Loading figures
\RequirePackage{graphicx}

% Align tables and figures
\RequirePackage{float}

% Pretty tables
\RequirePackage{booktabs}

% Removes indentation at beginning of paragraphs
\RequirePackage{parskip}

% microtype handles punctuation at the right margin.
\IfFileExists{microtype.sty}{%
  \RequirePackage[final,protrusion={true,compatibility}, expansion=true]{microtype}
}{}

%=====================================================================
%=================== Bibliography, color & links =====================

% Handles line breaks within urls
\RequirePackage[hyphens]{url}
\def\UrlFont{\tt}

% Bibliography settings
\RequirePackage[backend=biber,
                style=my-style,
                natbib,
                maxcitenames=1,
                maxbibnames=999]{biblatex}

\RequirePackage[usenames,dvipsnames,table]{xcolor}

% Colors for links
\definecolor{bluelinkcolor}{HTML}{0366D6}
\definecolor{graylinkcolor}{HTML}{404040}

% Hyperref setup
\RequirePackage{hyperref}
\hypersetup{
    colorlinks,
    breaklinks,
    linkcolor=black,
    urlcolor=bluelinkcolor,
    citecolor=bluelinkcolor,
    filecolor=graylinkcolor,
    plainpages=false,
    pdfpagelabels,
    bookmarks=false,
    pdfstartview=FitH
}

\newcommand{\doi}[1]{\url{https://doi.org/#1}}

%=====================================================================
%============================= metadata ==============================

\def\@pdfauthor{\relax}
\newcommand{\pdfauthor}[1]{\gdef\@pdfauthor{#1}}
\def\@pdftitle{\relax}
\newcommand{\pdftitle}[1]{\gdef\@pdftitle{#1}}
\def\@pdfkeywords{\relax}
\newcommand{\pdfkeywords}[1]{\gdef\@pdfkeywords{#1}}

\hypersetup{pdfauthor=\@pdfauthor,
            pdftitle=\@pdftitle,
            pdfkeywords=\@pdfkeywords}

%=====================================================================
%========================== page dimensions ==========================

\RequirePackage{geometry}
% Set textwidth to 2.5 times length of alphabet approx. 77 characters
\newlength{\alphabet}
\settowidth{\alphabet}{\normalfont abcdefghijklmnopqrstuvwxyz}
\geometry{paper=a4paper, top=1in, bottom=1in, textwidth=2.5\alphabet, includefoot}

%=====================================================================
%============================== title ================================

\renewcommand*{\title}[2][]{\gdef\@shorttitle{#1}\gdef\@title{#2}}
\renewcommand*{\author}[2][]{\gdef\@shortauthor{#1}\gdef\@author{#2}}

\def\@maketitle{%
   \vbox{
        \parskip=0.1\baselineskip
        \liningfont
        \raggedright
        {\LARGE\bfseries\@title}
        \vskip\baselineskip
        \ifdefempty{\@shortauthor}{\@author}{\@author, \@shortauthor}\@@par
        \@shorttitle\@@par
        \@date
   }
}

%=====================================================================
%============================ sectioning =============================

\RequirePackage[compact]{titlesec}
\titleformat{\section}{\Large\bfseries\liningfont}{\thesection}{1em}{}
\titleformat{\subsection}{\large\bfseries\liningfont}{\thesubsection}{.8em}{}
\titleformat{\subsubsection}{\normalsize\bfseries\liningfont}{\thesubsubsection}{.6em}{}{\itshape}

\titleformat{\paragraph}[runin]{\bfseries}{\liningfont\theparagraph}{0.4em}{\liningfont}

\titlespacing*{\section}{0pt}{2\baselineskip}{1\baselineskip}
\titlespacing*{\subsection}{0pt}{1\baselineskip}{1\baselineskip}
\titlespacing*{\subsubsection}{0pt}{0.8\baselineskip}{0.6\baselineskip}

%=====================================================================
%============================ footnotes ==============================

\renewcommand{\@makefntext}[1]{%
  \noindent \hbox to \z@{\hss{\textsuperscript{\@thefnmark}} \hfil}#1
}

%=====================================================================
%============================= Captions ==============================

%% Modify caption labels
\RequirePackage{caption}
\DeclareCaptionLabelFormat{lc}{\rmsc{#1}~{#2}}
\captionsetup{font=small, format=plain, labelformat=lc}
\captionsetup[subfigure]{labelsep=colon, labelfont=sc, labelformat=simple}

%=====================================================================
%=========================== useful macros ===========================

\def\co{\colon\thinspace}

\DeclareRobustCommand\dash{%
  \unskip\nobreak\thinspace\textemdash\thinspace\ignorespaces}
\pdfstringdefDisableCommands{\renewcommand{\dash}{ - }}

% based on \url defined in hyperref.sty
\DeclareRobustCommand*{\http}{\hyper@normalise\http@}
\def\http@#1{\hyper@linkurl{\Hurl{#1}}{http://#1}}

\newcommand{\email}[1]{\href{mailto:#1}{\ttfamily #1}}

\newcommand\blfootnote[1]{%
  \begingroup
  \renewcommand\thefootnote{}\footnote{#1}%
  \addtocounter{footnote}{-1}%
  \endgroup
}

\providecommand{\sv}[1]{\ensuremath{\llbracket{#1}\rrbracket}}

%=====================================================================
%============================= list settings =========================

%% Modify list
\RequirePackage{enumitem}
\setlist{noitemsep}
\setlist{nosep}
\setlist[1]{labelindent=\parindent} % < Usually a good idea
%% Have to remove the bold and indent labels at the edge, text will still be
%% aligned at \parindent
\setlist[description]{font=\normalfont\rmsc, labelindent=0pt}

\RequirePackage{linguex}%
\renewcommand{\firstrefdash}{}%
\AtBeginDocument{\settowidth{\Exlabelwidth}{(110)}}

%================================ fin ================================
%=====================================================================
