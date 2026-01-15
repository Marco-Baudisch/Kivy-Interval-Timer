# Kivy Interval Timer

A practical interval training application developed with **Python** and **KivyMD**. This project was created to solve a personal need for a customizable workout timer while practicing mobile-oriented UI logic.

## Key Features
- **Customizable Intervals:** Users can define the number of repetitions, duration of repetitions, and rest intervals.
- **Real-time Status:** Automatic updates and notifications for current training phases (Work/Rest).
- **Automated Calculations:** The app calculates total session time based on user input.

## Tech Stack
- **Language:** Python
- **Frameworks:** Kivy & KivyMD
- **IDE:** PyCharm

### Known Technical Issues:
- **Button Logic:** Multiple rapid clicks on the start button can cause conflicts with the pause functionality.
- **Timer Precision:** Frequent toggling of the pause button can lead to slight speed-up of the countdown.
- **State Management:** The timer is currently non-pausable during the initial 5-second countdown.

### Planned Enhancements:
- **Audio Integration:** Implementing sound for interval transitions.
- **UI Polishing:** Refining the visual interface for a more intuitive user experience.
- **Debug button:** Remove debug button in final app
- **Android Port:** Finalizing the build process for Android devices.
