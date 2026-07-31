# webGantt Documentation

**webGantt** is a web application for editing and visualizing Gantt charts, designed to be 100% compatible with the `.gan` XML format of the open-source reference application, GanttProject.

This documentation aims to present the overall operation of the application and the advanced configurations available via the preferences menu.

---

## Chapter 1: Introduction & Application Architecture

### 1.1 Principle and Interoperability
**webGantt** is designed to run entirely and autonomously within your web browser. It uses no server-side database, which guarantees the total confidentiality of your schedules. The application engine directly reads, interprets, and generates XML files with the `.gan` extension.
This approach guarantees absolute interoperability with the open-source desktop software **GanttProject** (an industry standard in project management).

### 1.2 The Main Interface
The workspace is structured around a dynamic resizer (*splitter*):
- **Left (WBS Pane)**: The task tree or your list of resources. It generally takes up 30% to 40% of the screen.
- **Right (Graphical Pane)**: The dynamic timeline displaying the Gantt chart or the resource allocation map.

### 1.3 Global Toolbar Actions
The top toolbar gathers the vital controls for the project lifecycle:
- **Open**: Instantly parses and loads a local `.gan` file.
- **Save**: Compiles the current state of your screen (including graphical preferences) and triggers the download of a new valid XML file.
- **Theme Button (Light/Dark)**: Toggles the CSS variables of the application to offer a deep dark mode (ideal to reduce eye strain) or a classic light mode.
- **Project Properties**: Allows defining global metadata (Project Name, Company, URL) as well as the calendars for general weekends and holidays that will impact all tasks.

---

## Chapter 2: The Work Breakdown Structure (WBS)

The *Work Breakdown Structure* (WBS) is the structural dashboard of your project.

### 2.1 Task Manipulation
- **Quick Add**: Click on "Add a task". If a task is already selected, the new row will be inserted immediately below the selection, inheriting its direct parent. A unique task identifier (`id`) is automatically generated in the background.
- **Inline Editing**: A double-click on certain columns (like the Name) allows instant editing without opening the advanced properties.
- **Hide the pane**: If you want to focus on the calendar aspect, the collapse button (◀) located at the top of the WBS pane allows hiding it to switch the Gantt chart to full screen.

### 2.2 Hierarchy and Structure
The WBS dedicated toolbar (located above the task list) offers structural movement tools. Graying out rules (enable/disable) ensure the structure remains logically coherent.
- **Indent (Right arrow →)**: Shifts the selected task to the right. The task immediately above then becomes a "parent task" (or phase summary). **Warning**: The dates of a parent task are automatically calculated based on its children. You can no longer manually edit the dates of a parent task.
- **Outdent (Left arrow ←)**: Brings the subtask up a level (sibling of its former parent).
- **Move Up (↑) / Move Down (↓)**: Modifies the vertical display order of two tasks with the same parent and the same depth level.

### 2.3 Multi-selection
The interface handles multi-selection: hold the `Ctrl` key (or `Cmd` on Mac) to select multiple scattered tasks, or `Shift` to select an entire block. This is particularly useful for applying mass links (see Chapter 3) or deleting a batch.

---

## Chapter 3: Gantt Chart and Dependencies

The right pane converts your WBS data into a clear temporal representation.

### 3.1 Visual Representations
- **Standard Tasks**: Colored rectangles (blue by default).
- **Parent Tasks (Groups)**: Black or dark bars with beveled ends temporally encompassing all their subtasks.
- **Milestones**: Tasks whose duration is 0 days (marking the end of a phase, for example, a deliverable submission) are automatically represented by a diamond.

### 3.2 Dependency Management (Chaining)
Instead of manually modifying the dates of each task, the application uses a constraint engine:
- **Link (🔗)**: Chronologically select several tasks in the WBS using the `Ctrl` key. Click on "Link": "Finish-to-Start" (FS) relationships will be created. Task B cannot start before the end of Task A.
- **Unlink (⛓️‍💥)**: Allows breaking all relationships between the currently selected tasks.
*Technical note: The engine recalculates the entire schedule in real-time if task "A" experiences a delay.*

### 3.3 Advanced Graphical Controls
- **Zoom (+ / -)**: Dynamically adjusts the time scale (X-axis). You can switch from a detailed "Days / Weeks" view to a "Months / Years" view for long-term projects.
- **Filtering (Funnel)**: Opens a dropdown menu allowing you to filter the chart.
  - *Not completed*: Hides what is at 100% progress.
  - *To do today* / *Late*: Relies on the current system date to target urgency.
- **Critical Path**: Activate the critical path icon to display in solid red the unalterable time path of the project. Any task located on this path (which has no safety margin) will shift the final delivery date of the project if its own duration extends.

---

## Chapter 4: Human and Material Resource Management

Resources are at the heart of capacity planning in **webGantt**.

### 4.1 The Resource Base
- Switch to the "Resources" space (at the bottom or via the dedicated view tab) to list your team.
- Add new resources by defining contact data (Name, Email, Phone).
- You can define a **Standard Rate** (hourly or daily rate) which, coupled with the duration of the tasks, will be used for the automated calculation of the total project cost.

### 4.2 Roles
Roles standardize job titles (e.g., *Cloud Architect*, *QA Engineer*, *Functional Consultant*).
- They are created globally via the **Project Properties** menu.
- Once created, you can assign a default Role to each resource. This allows grouping the team by profession.

### 4.3 Individual Vacation Days (Resource Calendar)
Besides the project calendar (weekends and global holidays), webGantt manages individual unavailability.
- In the details of a resource, access its **Vacation days calendar**.
- Any range declared as vacation will suspend the work of this resource on the Gantt chart. Tasks that are exclusively assigned to them will automatically see an extension of their actual duration (jumping over the vacations).

---

## Chapter 5: Assignment, Workload and Planning

### 5.1 Assign a resource
Open the **Advanced task properties** pane (gear icon on a WBS row, or double-click).
- In the **Resources** tab, you can select a contributor from the list.
- You must define a **Workload (Units)** in percentage. A rate of `100%` means full-time employment of the individual on the task. A rate of `50%` indicates part-time workload.
- **Coordinator**: The "Coordinator" option allows specifically designating one person (among those assigned) as the lead of the task.

### 5.2 The Occupancy Chart and Overload
In the resources pane, the timeline does not display tasks, but **occupancy bars**.
- These bars mathematically accumulate a person's workload if they are assigned to multiple overlapping tasks.
- If the cumulative daily workload exceeds **100%**, the bar turns red (*Overloaded*). This indicates a schedule conflict that will need to be resolved (by smoothing out dates or reducing the workload).
- *(Note: the alert colors, normal workload, and underload colors are customizable in the Project Preferences).*

---

## Chapter 6: Columns, Custom Fields and Baselines

### 6.1 The WBS Column Selector (⚙️)
The task list has a gear button in its header. It triggers a contextual menu allowing you to dynamically show or hide any system attribute (Start Date, End Date, % Complete, Cost, Duration). 
*The display state of the columns is temporary to optimize visual space.*

### 6.2 Custom Properties
If the standard is not enough for your profession, webGantt allows you to create metadata:
- Go to **Project Properties** > **Custom Fields** tab.
- Create a field (e.g., "Jira Ticket", "Validation Phase", "Estimated Budget").
- You must choose a strict type: *Text*, *Date*, *Integer*, *Boolean*, or *Double*.
- Once created, these fields automatically appear as new columns in the WBS tree and new input fields in the detail of each task.

### 6.3 Baselines
Planning is an iterative profession. Once the schedule is validated, you can create a **Baseline**.
- A baseline takes a silent "snapshot" of the planned dates of all tasks at time T.
- As the project progresses, if tasks get delayed, you can display the baseline on the Gantt chart. The interface will overlay (usually in gray) the original dates' rectangle under the current colored rectangle, visually exposing the slippage or advance of the schedule.

---

## Chapter 7: Project Preferences

The **Preferences** window allows for fine-tuning the display of the interface, the Gantt chart components, and the resource planner. These preferences are directly persisted in your `.gan` file and apply portably (if the file is opened by another user or in GanttProject, the graphical configuration is retained).

The window is divided into three tabs: **General**, **Gantt Chart Properties**, and **Resource Chart Properties**.

### 7.1 "General" Tab

This tab controls the overall appearance of the software (UI) as well as regional formats (language, date format).

| Field Name | Possible Values | Parameter Effect | XPath in the .gan file |
| --- | --- | --- | --- |
| Appearance | `Plastic`, etc. | Global visual theme of the interface. | `//view[@id='gantt-chart']/option[@id='general.appearance']/@value` |
| Application Fonts | List of fonts (e.g., `default`) | Defines the font used for the UI. | `//view[@id='gantt-chart']/option[@id='general.appFont']/@value` |
| (Application font size) | `1` to `5` (integer) | Adjusts the text size of the graphical interface. | `//view[@id='gantt-chart']/option[@id='general.appFontSize']/@value` |
| Chart Base Fonts | List of fonts (e.g., `default`) | Defines the font used for the SVG drawing of the chart. | `//view[@id='gantt-chart']/option[@id='general.chartFont']/@value` |
| (Chart font size) | `1` to `5` (integer) | Adjusts the text size inside the SVG chart. | `//view[@id='gantt-chart']/option[@id='general.chartFontSize']/@value` |
| Table Row Spacing | Decimal number (e.g., `20.0`, `32`) | Modifies the height (in pixels) of each row in the tree (WBS) and the chart. | `//view[@id='gantt-chart']/option[@id='general.rowSpacing']/@value` |
| DPI | Number (e.g., `96`) | Simulated pixel density for font definition and printing. | `//view[@id='gantt-chart']/option[@id='general.dpi']/@value` |
| Language | `fr`, `en`, etc. | Localization language for months, days of the week, and UI labels. | `//view[@id='gantt-chart']/option[@id='general.language']/@value` |
| Use Date Format | `default` or `custom` | Choice between the format dictated by the system or a manually entered format. | `//view[@id='gantt-chart']/option[@id='general.dateFormatType']/@value` |
| Custom Short Date Format | Format string (e.g., `dd/MM/y`) | Formatting syntax applied to the display of project dates. | `//view[@id='gantt-chart']/option[@id='general.dateFormat']/@value` |
| Logo File | Absolute or relative file path | Logo displayed on reports and project export (for printing). | `//view[@id='gantt-chart']/option[@id='general.logo']/@value` |

### 7.2 "Gantt Chart Properties" Tab

These options modify the native behavior of tasks and the textual or visual information drawn around them.

| Field Name | Possible Values | Parameter Effect | XPath in the .gan file |
| --- | --- | --- | --- |
| Task Name Prefix | Free text (e.g., `task`) | Prefix automatically used when creating a new task. | `//view[@id='gantt-chart']/option[@id='gantt.taskPrefix']/@value` |
| Name Format for Copied Tasks | Tokenized format (e.g., `{0}_{1}`) | Automation template used to rename a duplicated task. | `//view[@id='gantt-chart']/option[@id='gantt.taskCopyFormat']/@value` |
| New Task | Hex color (e.g., `#8cb6ce`) | Default background color applied to newly created tasks. | `//view[@id='gantt-chart']/option[@id='gantt.newTaskColor']/@value` |
| Constraint | `Strong` or `Rubber` | Default chaining constraint type. A "Strong" constraint automatically moves a task in case of a delay. | `//view[@id='gantt-chart']/option[@id='gantt.constraint']/@value` |
| Show Today with a Red Line | `yes` or `no` | If enabled, a vertical red line crosses the chart at today's date. | `//view[@id='gantt-chart']/option[@id='gantt.todayLine']/@value` |
| Project Start/End Dates | `yes` or `no` | If enabled, explicitly marks the global limits of the project on the timeline. | `//view[@id='gantt-chart']/option[@id='gantt.projectDates']/@value` |
| Weekend Display Style | `default` (grayed out), etc. | Defines whether weekends and non-working days are hatched, grayed out, or hidden. | `//view[@id='gantt-chart']/option[@id='gantt.weekendStyle']/@value` |
| Week Numbering | `default` (ISO), etc. | Numbering mode used in the header of the chart's timeline. | `//view[@id='gantt-chart']/option[@id='gantt.weekNumbering']/@value` |
| Show All Milestones | Checkbox (`true` or `false`) | Indicates if tasks with a duration of 0 (milestones) should be rendered (diamond) in the SVG. | `//view[@id='gantt-chart']/option[@id='gantt.showMilestones']/@value` |
| (Details) Above | `name`, `resources`, `progress`, `duration`, ` ` | Defines the metric displayed *above* the SVG rectangular bar of the task. | `//view[@id='gantt-chart']/option[@id='gantt.detailTop']/@value` |
| (Details) Below | `name`, `resources`, `progress`, `duration`, ` ` | Defines the metric displayed *below* the SVG rectangular bar of the task. | `//view[@id='gantt-chart']/option[@id='gantt.detailBottom']/@value` |
| (Details) Left | `name`, `resources`, `progress`, `duration`, ` ` | Defines the metric displayed *to the left* of the SVG rectangular bar of the task. | `//view[@id='gantt-chart']/option[@id='gantt.detailLeft']/@value` |
| (Details) Right | `name`, `resources`, `progress`, `duration`, ` ` | Defines the metric displayed *to the right* of the SVG rectangular bar of the task. | `//view[@id='gantt-chart']/option[@id='gantt.detailRight']/@value` |

### 7.3 "Resource Chart Properties" Tab

This third tab is used to configure the bottom pane of the application (the tree and timeline of material or human resources), and in particular the conditional coloring related to the weekly workload of these resources.

| Field Name | Possible Values | Parameter Effect | XPath in the .gan file |
| --- | --- | --- | --- |
| Resources | Hex color (e.g., `#90b6d3`) | Standard background color for intervals where the resource works normally (load <= 100%). | `//view[@id='resource-table']/option[@id='res.color']/@value` |
| Resources (Overloaded) | Hex color (e.g., `#e14436`) | Alert color for periods when the resource is assigned to more than 100% (schedule conflicts). | `//view[@id='resource-table']/option[@id='res.overloadedColor']/@value` |
| Resources (Underloaded) | Hex color (e.g., `#3bd93b`) | Color marking periods when the resource does not meet the expected hours quota (optional). | `//view[@id='resource-table']/option[@id='res.underloadedColor']/@value` |
| Vacation Days | Hex color (e.g., `#ffff55`) | Color used to draw the background of inactivity or vacation periods reported for this resource. | `//view[@id='resource-table']/option[@id='res.vacationColor']/@value` |
