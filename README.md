# WebGantt

WebGantt is a modern, lightweight, and fully web-based Gantt chart application designed to seamlessly read, edit, and save **GanttProject** (`.gan`) files directly in your browser. 

Built with pure HTML, CSS, and JavaScript, it requires no backend or server to run. You can manage your projects, resources, and task schedules with an intuitive and responsive user interface.

## 🚀 Features

* **Full `.gan` File Compatibility**: Open, edit, and save XML files compatible with GanttProject.
* **Interactive WBS (Work Breakdown Structure)**: 
  * Hierarchical task management with subtasks.
  * Drag-and-drop support and keyboard shortcuts for indentation.
  * Dynamic column visibility.
* **Advanced Task Management**:
  * Edit task details, duration, start/end dates, priorities, and completion rates.
  * Manage milestones and task colors/shapes.
* **Resource Allocation**:
  * Define roles and project resources.
  * Assign resources to tasks with specific workload loads.
* **Dependencies & Predecessors**:
  * Create Finish-to-Start (FS), Start-to-Start (SS), and other dependencies.
  * Visualize the **Critical Path** dynamically on the Gantt chart.
* **Custom Properties**:
  * Support for custom fields (Text, Integer, Date, Boolean).
  * Real-time evaluation of calculated fields (Double/Decimal) based on formulas (e.g., `cost * 1.5`).
* **Modern UI**:
  * Clean, responsive interface with a resizable split-pane layout.
  * Dark Mode / Light Mode support.
  * Dynamic task filtering (Today, Late, In Progress, etc.).

## 🛠️ Usage

Since WebGantt is entirely client-side, you can simply open the `webGantt.html` file in your favorite modern web browser.

1. Clone or download this repository.
2. Open `webGantt.html` in your browser.
3. Click the **Open** button to load a `.gan` file from your computer.
4. Manage your project using the interactive table and timeline.
5. Click **Save** to download your modified `.gan` file, ready to be used in GanttProject or other compatible software.

## 📁 Repository Structure

* `webGantt.html`: The core application containing the UI, SVG rendering logic, and state management.
* `specs/`: Contains detailed functional specifications, XML format documentation, and roadmap tasks.
  * `assets/example.gan`: A sample project file showcasing all features (custom fields, roles, allocations, constraints).
  * `tasks.md`: The development backlog and feature tracking.

## 🤝 Contributing

Contributions, bug reports, and feature requests are welcome! Feel free to open an issue or submit a pull request if you want to improve the application.

## 📜 License

This project is open-source and available under the standard MIT License.
