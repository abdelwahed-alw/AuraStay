
# 🏡 AuraStay – Guest House Management System

AuraStay is a lightweight, high-performance desktop application built with **Python**, **Tkinter**, and **SQLite3**. It is designed for small to medium-sized guest houses and boutique hotels to manage reservations, rooms, and clients with a focus on speed and a modern user experience.

### ✨ Key Features

* **Modern UI:** A refined dark theme inspired by high-end productivity tools, featuring a sidebar navigation and a responsive dashboard.
* **Bilingual Support:** Full support for **Français** and **English**, togglable instantly within the app.
* **Dashboard Analytics:** Real-time KPIs (Key Performance Indicators) for total clients, active bookings, room availability, and total revenue.
* **Full CRUD Operations:**
* **Reservations:** Easily manage check-ins, check-outs, and status updates.
* **Room Management:** Track room types (Simple, Double, Suite), prices, and real-time status.
* **Client Database:** Maintain a searchable record of all guests and contact info.


* **Smart Automation:** Automatically calculates total booking amounts based on nightly rates and updates room availability when bookings are made or cancelled.
* **SQLite Integration:** Zero configuration required; the database initializes itself on the first run.

### 🛠 Tech Stack

* **Language:** Python 3.x
* **GUI Framework:** Tkinter / ttk (Custom styled)
* **Database:** SQLite3 (Local storage)
* **Design:** Modern CSS-inspired color palette for dark mode.

### 🚀 Getting Started

#### Prerequisites

Ensure you have Python 3 installed on your machine.

```bash
python --version

```

#### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/aurastay.git
cd aurastay

```


2. **Run the application:**
No external dependencies (like `pip install`) are required as it uses standard Python libraries!
```bash
python main.py

```



### 📁 Database Structure

The app automatically creates `maison_hote.db` with the following schema:

* `chambres`: Room details, pricing, and availability.
* `clients`: Guest names and contact information.
* `reservations`: Booking dates, status, and financial records.

---

### 🎨 Color Palette Reference

The application uses a specific high-contrast palette for accessibility and aesthetics:

* **Background:** `#0F1923`
* **Accent:** `#FF4C6E` (Vibrant Pink)
* **Success:** `#34D399` (Emerald Green)
* **Links/Headers:** `#60A5FA` (Soft Blue)

---

*Created by Abdelwahed Abdellaoui*





Analyze the GitHub repository at [REPOSITORY_URL] and provide:

1. **Repository Overview**
   - Owner, visibility, creation date, last update
   - Repository ID and default branch
   - License and topics/tags

2. **Tech Stack & Language Composition**
   - Primary languages with percentages
   - Technology dependencies

3. **Project Description**
   - Project purpose and main goals
   - Type of project (web app, library, API, etc.)
   - Problem it solves

4. **Key Features & Functionality**
   - Main features and capabilities
   - Core components or modules
   - Notable integrations

5. **Project Structure**
   - Directory and file organization
   - Important files and their purposes
   - Size breakdown of key files

6. **Setup & Getting Started**
   - Installation instructions
   - Required dependencies
   - How to run the project
   - Port/URL to access if applicable

7. **Usage Examples**
   - How to use the main features
   - Example commands or code snippets
   - Testing endpoints if applicable

8. **Statistics**
   - Repository size
   - Open issues/PRs
   - Forks, stars, watchers
   - Contributor count if available

9. **Additional Context**
   - README content summary
   - Any special configurations
   - Notable files (.env, config, etc.)
