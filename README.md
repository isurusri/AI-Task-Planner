# AI Task Planner for Developers

A sophisticated multi-agent planning tool that uses AI to decompose feature requests into detailed, actionable subtasks. Built with Python, OpenAI API, and modern web technologies.

## 🚀 Features

- **Multi-Agent Architecture**: Six specialized AI agents working together
- **Chain-of-Thought Prompting**: Advanced reasoning for task decomposition
- **Autonomous Execution Simulation**: Realistic workflow simulation
- **Modern Web Interface**: Beautiful, responsive UI with real-time updates
- **Task Dependency Management**: Intelligent task ordering and dependency resolution
- **Quality Assessment**: Built-in quality metrics and recommendations

## 🤖 AI Agents

### 1. Strategic Planner
- **Purpose**: Decomposes high-level requirements into detailed tasks
- **Capabilities**: Task decomposition, requirement analysis, work breakdown structure
- **Specialty**: Chain-of-thought reasoning for complex planning

### 2. Technical Analyzer
- **Purpose**: Analyzes requirements and assesses technical feasibility
- **Capabilities**: Risk identification, dependency analysis, performance assessment
- **Specialty**: Technical feasibility and architecture review

### 3. Code Developer
- **Purpose**: Implements features and writes code
- **Capabilities**: Code implementation, feature development, bug fixing
- **Specialty**: Multiple programming languages and frameworks

### 4. Quality Tester
- **Purpose**: Creates test cases and performs quality assurance
- **Capabilities**: Test case creation, automation, performance testing
- **Specialty**: Comprehensive testing strategies

### 5. Code Reviewer
- **Purpose**: Reviews code and assesses quality
- **Capabilities**: Code review, security assessment, best practices validation
- **Specialty**: Quality assurance and mentoring

### 6. Workflow Coordinator
- **Purpose**: Orchestrates multi-agent workflows
- **Capabilities**: Task coordination, dependency management, progress monitoring
- **Specialty**: Workflow optimization and resource allocation

## 🛠️ Technology Stack

- **Backend**: Python 3.8+, FastAPI, Pydantic
- **AI/ML**: OpenAI GPT-4 API
- **Frontend**: HTML5, CSS3, JavaScript, Tailwind CSS
- **Architecture**: Multi-agent system with autonomous execution
- **Deployment**: Uvicorn ASGI server

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- OpenAI API key
- pip package manager

### Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ai-task-planner
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

4. **Run the application**
   ```bash
   python main.py
   ```

5. **Access the web interface**
   Open your browser and navigate to `http://localhost:8000`

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4
MAX_TOKENS=2000
TEMPERATURE=0.7
DEBUG=False
HOST=0.0.0.0
PORT=8000
```

### Model Configuration

- **OpenAI Model**: Configure which GPT model to use (gpt-4, gpt-3.5-turbo)
- **Max Tokens**: Control response length
- **Temperature**: Adjust creativity vs consistency (0.0-1.0)

## 🎯 Usage

### Basic Usage

1. **Describe Your Feature**: Enter a detailed description of what you want to build
2. **Set Context**: Provide additional project context (optional)
3. **Configure Depth**: Choose decomposition depth (2-5 levels)
4. **Decompose**: Click "Decompose into Tasks" to generate detailed tasks
5. **Review Results**: Examine the generated tasks and execution plan
6. **Simulate**: Run autonomous execution simulation
7. **Export**: Download the task plan as JSON

### Example Input

```
Build a user authentication system with JWT tokens, password reset functionality, 
role-based access control, and integration with a React frontend and Node.js backend.
```

### Example Output

The system will generate:
- 15-25 detailed subtasks
- Task dependencies and priorities
- Time estimates for each task
- Agent assignments
- Execution sequence
- Quality metrics

## 🏗️ Architecture

### Multi-Agent System

```
User Input → Task Decomposition Service → Multi-Agent Processing
    ↓
Planner Agent → Analyzer Agent → Developer Agent
    ↓
Tester Agent → Reviewer Agent → Coordinator Agent
    ↓
Execution Simulation → Results & Recommendations
```

### Key Components

- **Models**: Pydantic models for data validation
- **Agents**: Specialized AI agents with unique capabilities
- **Services**: Core business logic and orchestration
- **API**: FastAPI REST endpoints
- **Frontend**: Modern web interface with real-time updates

## 🔍 API Endpoints

### Task Decomposition
```http
POST /api/decompose
Content-Type: application/json

{
  "user_input": "Build a user authentication system...",
  "project_context": "E-commerce platform using React and Node.js",
  "max_depth": 3,
  "include_estimates": true
}
```

### Execution Simulation
```http
POST /api/simulate
Content-Type: application/json

{
  "project_id": "uuid",
  "simulation_mode": true,
  "max_concurrent_tasks": 3
}
```

### Health Check
```http
GET /api/health
```

### Agent Information
```http
GET /api/agents
```

## 🧪 Chain-of-Thought Prompting

The system uses advanced chain-of-thought prompting to ensure high-quality task decomposition:

1. **Analysis**: Understand the requirement deeply
2. **Decomposition**: Break down into logical components
3. **Task Creation**: Generate specific, actionable tasks
4. **Validation**: Review for completeness and feasibility

## 📊 Quality Metrics

The system provides comprehensive quality metrics:

- **Description Coverage**: Percentage of tasks with detailed descriptions
- **Estimation Coverage**: Percentage of tasks with time estimates
- **Dependency Coverage**: Percentage of tasks with defined dependencies
- **Complexity Distribution**: Low/Medium/High complexity task breakdown
- **Agent Utilization**: Workload distribution across agents

## 🚀 Advanced Features

### Autonomous Execution Simulation

- Realistic timing based on task complexity
- Agent workload management
- Dependency resolution
- Progress tracking and reporting
- Error handling and recovery

### Task Dependency Management

- Automatic dependency detection
- Critical path analysis
- Bottleneck identification
- Optimization recommendations

### Quality Assurance

- Built-in code review capabilities
- Security assessment
- Performance analysis
- Best practices validation

## 🔧 Development

### Project Structure

```
ai-task-planner/
├── agents/                 # AI agent implementations
│   ├── base_agent.py      # Base agent class
│   ├── planner_agent.py   # Strategic planning agent
│   ├── analyzer_agent.py  # Technical analysis agent
│   ├── developer_agent.py # Code development agent
│   ├── tester_agent.py    # Quality testing agent
│   ├── reviewer_agent.py  # Code review agent
│   └── coordinator_agent.py # Workflow coordination agent
├── services/              # Core business services
│   ├── openai_service.py  # OpenAI API integration
│   ├── task_decomposition_service.py # Task decomposition logic
│   └── execution_simulation_service.py # Execution simulation
├── models.py              # Pydantic data models
├── config.py              # Configuration management
├── main.py                # FastAPI application
├── templates/             # HTML templates
│   └── index.html         # Main web interface
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

### Adding New Agents

1. Create a new agent class inheriting from `BaseAgent`
2. Implement required methods: `process_task()`, `get_capabilities()`
3. Register the agent in the coordinator
4. Update the agent registry

### Customizing Prompts

Modify the prompt templates in each agent's `_build_*_prompt()` methods to customize the AI behavior.

## 🐛 Troubleshooting

### Common Issues

1. **OpenAI API Errors**
   - Verify API key is correct
   - Check API quota and billing
   - Ensure model is available

2. **Import Errors**
   - Verify all dependencies are installed
   - Check Python version compatibility

3. **Agent Processing Errors**
   - Check OpenAI API response format
   - Verify prompt templates are valid
   - Review error logs for details

### Debug Mode

Enable debug mode by setting `DEBUG=True` in your `.env` file for detailed logging.

## 📈 Performance

### Optimization Tips

- Use appropriate decomposition depth (3-4 levels recommended)
- Limit concurrent tasks based on available resources
- Monitor OpenAI API usage and costs
- Cache frequently used responses

### Scaling

- Implement database storage for projects
- Add Redis for caching
- Use async processing for large projects
- Consider horizontal scaling with load balancers

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- OpenAI for providing the GPT API
- FastAPI for the excellent web framework
- Tailwind CSS for the beautiful UI components
- The open-source community for inspiration and tools

## 📞 Support

For support, please open an issue in the GitHub repository or contact the development team.

---

**Built with ❤️ for developers who want to plan better and build faster.**

