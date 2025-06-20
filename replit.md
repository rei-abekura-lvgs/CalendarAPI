# Japanese Calendar API

## Overview

This is a static Japanese calendar data API project that provides Japanese calendar information in JSON format. The project generates and serves Japanese calendar data including holidays, rokuyō (六曜), daily keywords, recommended teas, and other cultural elements through a static GitHub Pages-hosted API.

## System Architecture

The system follows a **Static Site Generator + API** architecture:

1. **Data Generation Layer**: Python script that generates JSON calendar data
2. **Static Hosting Layer**: GitHub Pages for serving both documentation and API endpoints
3. **Frontend Documentation**: HTML/CSS/JavaScript documentation site
4. **API Layer**: Static JSON files served as RESTful endpoints

### Technology Stack
- **Backend Data Generation**: Python 3.11+
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Styling**: Bootstrap 5.3.0
- **Code Highlighting**: Prism.js
- **Icons**: Font Awesome 6.4.0
- **Hosting**: GitHub Pages
- **Development Environment**: Replit with Streamlit

## Key Components

### Data Generation System
- **File**: `generate_data.py`
- **Purpose**: Generates Japanese calendar data for the specified year (2025)
- **Output**: JSON files organized by month in `/api/2025/` directory
- **Features**: 
  - Japanese holidays calculation
  - Rokuyō (六曜) generation
  - Daily keywords and recommended teas
  - Color themes for each day
  - Weekday information in both Japanese and English

### API Structure
- **Base Path**: `/api/2025/`
- **Monthly Endpoints**: `01.json` through `12.json`
- **Full Year Endpoint**: `all.json`
- **CORS Enabled**: Full cross-origin support for web applications

### Documentation Site
- **Main File**: `index.html`
- **Styling**: `css/style.css`
- **Interactivity**: `js/app.js`
- **Features**:
  - API documentation with live examples
  - Code snippets with syntax highlighting
  - Responsive design
  - Interactive demo section

### Configuration Files
- **GitHub Pages**: `_config.yml` with Jekyll configuration
- **Streamlit**: `.streamlit/config.toml` for development server
- **Replit**: `.replit` with Python 3.11 and Streamlit setup

## Data Flow

1. **Data Generation**:
   - Python script reads master data (holidays, rokuyō patterns, keywords)
   - Calculates calendar data for each day of 2025
   - Outputs structured JSON files for each month
   - Creates aggregated annual data file

2. **API Consumption**:
   - Static JSON files served directly from GitHub Pages
   - CORS headers allow cross-origin requests
   - Clients fetch data via standard HTTP GET requests

3. **Documentation**:
   - Interactive examples demonstrate API usage
   - Real-time data fetching shows current day information
   - Code snippets provide integration examples

## External Dependencies

### Runtime Dependencies
- **Bootstrap 5.3.0**: UI framework for responsive design
- **Prism.js 1.29.0**: Syntax highlighting for code examples
- **Font Awesome 6.4.0**: Icon library for UI elements

### Development Dependencies
- **Python 3.11+**: For data generation scripts
- **Streamlit**: Development server for testing
- **GitHub Pages**: Static hosting platform

### Data Sources
- **Japanese Holidays**: Hardcoded master data (simplified implementation)
- **Rokuyō**: Calculated based on traditional lunar calendar patterns
- **Cultural Elements**: Curated lists of keywords, teas, and color themes

## Deployment Strategy

### GitHub Pages Deployment
- **Trigger**: Push to main branch
- **Build Process**: Jekyll static site generation
- **Served Files**: 
  - Documentation site (`index.html`, CSS, JS)
  - API endpoints (JSON files in `/api/` directory)
  - Error pages (`404.html`)

### Development Environment
- **Primary**: Replit with Streamlit server
- **Local Testing**: Python HTTP server on port 5000
- **Hot Reload**: Streamlit for rapid development iteration

### CORS Configuration
- **Headers**: Configured in `_config.yml`
- **Access-Control-Allow-Origin**: Wildcard for public API
- **Cache-Control**: 1-hour caching for performance

## Changelog
- June 20, 2025. Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.