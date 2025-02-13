# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [SEO-Analyzer-AI](https://github.com/XYLxiria/SEO-Analyzer-AI).

## [Unreleased]

## [6.6]

### Added
- Added numpy for more precise calculations in the diagram.
- Added several error handling improvements.
- Added data for images without alt text in the third analysis box.

## [6.5]

### Added
- Set the installer to administrator mode (Check .iss file).
- Added a new menu bar.

## [6.4]

### Added
- Added caching method to optimize resource usage.
- Fixed bugs in error handling.
- Created the second installer.

## [6.3]

### Added
- Added a menu bar.
- Provided more details in the menu bar.

## [6.2]

### Changed
- Stabilized the analysis results.
- Added and improved visuals.
- Modified several functions.

## [6.1]

### Removed
- Removed spaCy features and libraries related to analysis results.

### Added
- Added several error handling improvements.
- Added an icon to the GUI.

## [5.1]

### Fixed
- Fixed the placement of analysis result boxes.
- Fixed the loading bar and added process text.

## [4.2.1]

### Fixed
- Fixed visual bugs in the PDF output.

## [4.2]

### Added
- Added a timeout response when the web analysis fails.
- Added a directory selection function when saving PDFs.
- Added several regex rules to stabilize the PDF format.

### Fixed
- Fixed several minor bugs.

## [4.1]

### Changed
- Limited the number of keywords displayed in the "Show Analysis Graph" button to a maximum of 30 words.
- Limited the number of keywords displayed in the "Show Specific Analysis" button to a maximum of 20 words.

### Fixed
- Fixed several minor bugs.

## [3.2]

### Fixed
- Fixed horizontal X-axis visualization bugs in specific analysis results.
- Fixed graphical visualization bugs in the first analysis button.

## [3.1]

### Added
- Added spaCy library for keyword detection beyond NLTK.
- Used button functions from version 0.2 for specific analysis results using spaCy.
- Added a new graph to store spaCy analysis results.
- Added a feature to save analysis results as a PDF.

## [2.4]

### Removed
- Removed colors in the alt tag analysis box.
- Removed the back button in the analysis results graph, replaced with a PyQT5 taskbar.

### Fixed
- Fixed several minor bugs.

## [2.3]

### Added
- Added a back button to the analysis results graph.
- Added special colors to the alt tag analysis box.

### Fixed
- Fixed bugs and visual calculation errors in certain cases.

## [2.2]

### Added
- Added an error response for invalid input.
- Added a simple loading animation.

### Fixed
- Fixed several minor bugs.

## [2.1]

### Added
- Added a new box for entering addresses and titles.
- Added additional descriptions to each box.
- Added a new button for future use (still hidden).

## [1.1]

### Added
- Added a new box for alt tag analysis.

### Changed
- Dynamically updated box sizes.

### Fixed
- Fixed several minor bugs.

## [1.0]

### Added
- GUI transitioned to PyQT version 5.
- Added a new button.
- Users can now view graphs for keyword analysis.
- Added several titles to boxes as explanations.
