import 'package:flutter/material.dart';

void main() {
  runApp(TaskManagerApp());
}

class Task {
  final String title;
  bool isCompleted;

  Task({required this.title, this.isCompleted = false});
}

class TaskManagerApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Task Manager 📝',
      theme: ThemeData(
        primarySwatch: Colors.deepPurple,
        useMaterial3: true,
      ),
      home: TaskManagerScreen(),
    );
  }
}

class TaskManagerScreen extends StatefulWidget {
  @override
  _TaskManagerScreenState createState() => _TaskManagerScreenState();
}

class _TaskManagerScreenState extends State<TaskManagerScreen> {
  final List<Task> _tasks = [];
  final TextEditingController _controller = TextEditingController();

  void _addTask() {
    String title = _controller.text.trim();
    if (title.isNotEmpty) {
      setState(() {
        _tasks.add(Task(title: title));
      });
      _controller.clear();
    }
  }

  void _toggleTask(int index) {
    setState(() {
      _tasks[index].isCompleted = !_tasks[index].isCompleted;
    });
  }

  void _deleteTask(int index) {
    setState(() {
      _tasks.removeAt(index);
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Flutter Task Manager 🧠'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          children: [
            // Input field and add button
            Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _controller,
                    decoration: InputDecoration(
                      labelText: 'Enter a new task',
                      border: OutlineInputBorder(),
                    ),
                    onSubmitted: (_) => _addTask(),
                  ),
                ),
                SizedBox(width: 8),
                ElevatedButton(
                  onPressed: _addTask,
                  child: Text('Add'),
                ),
              ],
            ),
            SizedBox(height: 16),

            // List of tasks
            Expanded(
              child: _tasks.isEmpty
                  ? Center(child: Text("No tasks yet. Let's add some! 🚀"))
                  : ListView.builder(
                      itemCount: _tasks.length,
                      itemBuilder: (context, index) {
                        final task = _tasks[index];
                        return Card(
                          child: CheckboxListTile(
                            value: task.isCompleted,
                            title: Text(
                              task.title,
                              style: TextStyle(
                                decoration: task.isCompleted
                                    ? TextDecoration.lineThrough
                                    : TextDecoration.none,
                              ),
                            ),
                            onChanged: (_) => _toggleTask(index),
                            secondary: IconButton(
                              icon: Icon(Icons.delete, color: Colors.red),
                              onPressed: () => _deleteTask(index),
                            ),
                          ),
                        );
                      },
                    ),
            ),
          ],
        ),
      ),
    );
  }
}