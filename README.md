# WebGantt

## 📺 Demo Video

<video width="100%" controls style="max-width: 800px; margin: 20px 0; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
  <source src="artifacts/DEMO_WEBGANTT_20260801_215124.mp4" type="video/mp4">
  Your browser does not support the video tag. <a href="artifacts/DEMO_WEBGANTT_20260801_215124.mp4">Download the demo video</a>
</video>

---

WebGantt is a modern, lightweight, and fully web-based Gantt chart application designed to seamlessly read, edit, and save **GanttProject** (`.gan`) files directly in your browser. 

Built with pure HTML, CSS, and JavaScript, it requires no backend or server to run. You can manage your projects, resources, and task schedules with an intuitive and responsive user interface.


## 🙏 Acknowledgements to GanttProject

WebGantt relies on the robust `.gan` file format defined by [GanttProject](https://www.ganttproject.biz/). We would like to warmly thank **Alexandre Thomas**, who created GanttProject in 2003, as well as **Dmitry Barashev** and **Maarten Bezemer**, who have brilliantly maintained and evolved this project ever since. GanttProject has been a true reference tool in project management for over twenty years.

To help developers build applications that are interoperable with `.gan` files, we provide several reference tools in our assets:
- [example.gan](https://github.com/yuntux/webGantt/blob/main/specs/001-ganttproject-features/assets/example.gan) : A comprehensive sample project file.
- [ganttproject.xsd](https://github.com/yuntux/webGantt/blob/main/specs/001-ganttproject-features/assets/ganttproject.xsd) : The XML schema (XSD) defining the structure.
- [format-gan.md](https://github.com/yuntux/webGantt/blob/main/specs/001-ganttproject-features/assets/gan-format.md) : Detailed documentation of the format's architecture.

## 📚 User Documentation

For a comprehensive user guide, including a detailed description of the application and all its preference settings (functional impacts, possible values, and XML storage), please refer to the [doc.md](https://github.com/yuntux/webGantt/blob/main/doc.md) file.


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
