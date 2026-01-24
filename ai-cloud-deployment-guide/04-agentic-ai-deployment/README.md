# Chapter 4: Agentic AI Application Deployment

## Overview

Agentic AI systems are AI applications that can:
- **Reason** about complex tasks
- **Use tools** to interact with external systems
- **Make decisions** autonomously
- **Collaborate** with other agents

This chapter covers deploying:
- Single-agent systems with tools
- Multi-agent architectures
- Production patterns for agentic AI

---

## Understanding Agentic AI Architecture

### What Makes an Agent?

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         AGENT COMPONENTS                                 │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │                         LLM BRAIN                                │  │
│   │   • Understands user intent                                      │  │
│   │   • Plans actions                                                │  │
│   │   • Decides which tools to use                                   │  │
│   │   • Synthesizes final response                                   │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│                              │                                          │
│              ┌───────────────┼───────────────┐                         │
│              │               │               │                          │
│              ▼               ▼               ▼                          │
│   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐                 │
│   │    TOOL 1    │  │    TOOL 2    │  │    TOOL 3    │                 │
│   │  (Search)    │  │  (Calculator)│  │   (API)      │                 │
│   └──────────────┘  └──────────────┘  └──────────────┘                 │
│                                                                         │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │                         MEMORY                                   │  │
│   │   • Short-term: Current conversation                             │  │
│   │   • Long-term: Past interactions, learned preferences            │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Agent Execution Flow (ReAct Pattern)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    ReAct (Reasoning + Acting) LOOP                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   User: "What's the weather in NYC and should I bring an umbrella?"     │
│                                    │                                    │
│                                    ▼                                    │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │ THOUGHT 1: I need to get the current weather for NYC.           │  │
│   │ ACTION 1: Call weather_tool("New York City")                    │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│                                    │                                    │
│                                    ▼                                    │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │ OBSERVATION 1: {"temp": 65, "condition": "Partly cloudy",       │  │
│   │                 "rain_chance": 70%}                             │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│                                    │                                    │
│                                    ▼                                    │
│   ┌─────────────────────────────────────────────────────────────────┐  │
│   │ THOUGHT 2: There's a 70% chance of rain. User should bring      │  │
│   │            an umbrella.                                         │  │
│   │ ACTION 2: respond_to_user                                       │  │
│   └─────────────────────────────────────────────────────────────────┘  │
│                                    │                                    │
│                                    ▼                                    │
│   Final Answer: "It's 65°F and partly cloudy in NYC. With a 70%         │
│                  chance of rain, I'd recommend bringing an umbrella."   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Single Agent Deployment

### Tool-Using Agent Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    TOOL-USING AGENT ARCHITECTURE                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌──────────┐     ┌──────────────┐     ┌─────────────────────────┐    │
│   │  Client  │────►│ API Gateway  │────►│   Agent Service         │    │
│   │  (App)   │     │              │     │   (ECS/Cloud Run)       │    │
│   └──────────┘     └──────────────┘     └───────────┬─────────────┘    │
│                                                     │                   │
│                     ┌───────────────────────────────┤                   │
│                     │                               │                   │
│                     ▼                               ▼                   │
│   ┌────────────────────────────┐     ┌────────────────────────────┐    │
│   │      LLM Service           │     │       Tool Registry        │    │
│   │  (Bedrock/Vertex AI)       │     │                            │    │
│   │                            │     │  ┌──────┐  ┌──────┐       │    │
│   │  • Function calling        │     │  │Search│  │ DB   │       │    │
│   │  • Reasoning               │     │  │ API  │  │Query │       │    │
│   │  • Response generation     │     │  └──────┘  └──────┘       │    │
│   └────────────────────────────┘     │  ┌──────┐  ┌──────┐       │    │
│                                      │  │Email │  │Custom│       │    │
│                                      │  │ API  │  │ Tool │       │    │
│                                      │  └──────┘  └──────┘       │    │
│                                      └────────────────────────────┘    │
│                                                                         │
│   ┌────────────────────────────────────────────────────────────────┐   │
│   │                     Memory Store                                │   │
│   │   (DynamoDB/Firestore + Redis for session)                     │   │
│   └────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Building a Tool-Using Agent

#### Step 1: Define Tools

```python
# tools.py
from typing import Callable, Dict, Any
from pydantic import BaseModel, Field
import httpx

class ToolDefinition(BaseModel):
    """Schema for tool definition"""
    name: str
    description: str
    parameters: Dict[str, Any]
    function: Callable = None
    
    class Config:
        arbitrary_types_allowed = True

# Example tools
def search_web(query: str) -> str:
    """Search the web for information"""
    # In production, use a real search API
    response = httpx.get(
        "https://api.search.example.com/search",
        params={"q": query}
    )
    return response.json()

def get_weather(location: str) -> Dict:
    """Get current weather for a location"""
    response = httpx.get(
        "https://api.weather.example.com/current",
        params={"location": location}
    )
    return response.json()

def calculate(expression: str) -> float:
    """Safely evaluate a mathematical expression"""
    # Use a safe evaluator
    import ast
    import operator
    
    operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
    }
    
    def eval_expr(node):
        if isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.BinOp):
            return operators[type(node.op)](
                eval_expr(node.left), 
                eval_expr(node.right)
            )
        else:
            raise ValueError(f"Unsupported operation")
    
    tree = ast.parse(expression, mode='eval')
    return eval_expr(tree.body)

def query_database(sql: str) -> list:
    """Execute a read-only SQL query"""
    # Implement with your database connection
    # IMPORTANT: Sanitize and validate SQL!
    pass

# Tool registry
TOOLS = {
    "search_web": ToolDefinition(
        name="search_web",
        description="Search the web for current information",
        parameters={
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query"
                }
            },
            "required": ["query"]
        },
        function=search_web
    ),
    "get_weather": ToolDefinition(
        name="get_weather",
        description="Get current weather for a location",
        parameters={
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City name or coordinates"
                }
            },
            "required": ["location"]
        },
        function=get_weather
    ),
    "calculate": ToolDefinition(
        name="calculate",
        description="Perform mathematical calculations",
        parameters={
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Mathematical expression to evaluate"
                }
            },
            "required": ["expression"]
        },
        function=calculate
    )
}
```

#### Step 2: Build the Agent

```python
# agent.py
import json
from typing import List, Dict, Any, Optional
import boto3  # or use vertexai

class ToolUsingAgent:
    def __init__(self, tools: Dict[str, 'ToolDefinition'], model_id: str = 'anthropic.claude-3-sonnet-20240229-v1:0'):
        self.tools = tools
        self.model_id = model_id
        self.bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
        self.conversation_history = []
        self.max_iterations = 10
    
    def _format_tools_for_llm(self) -> List[Dict]:
        """Format tools for Claude's tool_use format"""
        return [
            {
                "name": tool.name,
                "description": tool.description,
                "input_schema": tool.parameters
            }
            for tool in self.tools.values()
        ]
    
    def _call_llm(self, messages: List[Dict], tools: List[Dict]) -> Dict:
        """Call Bedrock with messages and tools"""
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 4096,
            "messages": messages,
            "tools": tools
        })
        
        response = self.bedrock.invoke_model(
            modelId=self.model_id,
            body=body
        )
        
        return json.loads(response['body'].read())
    
    def _execute_tool(self, tool_name: str, tool_input: Dict) -> Any:
        """Execute a tool and return the result"""
        if tool_name not in self.tools:
            return {"error": f"Unknown tool: {tool_name}"}
        
        tool = self.tools[tool_name]
        try:
            result = tool.function(**tool_input)
            return result
        except Exception as e:
            return {"error": str(e)}
    
    def run(self, user_message: str) -> str:
        """Run the agent with a user message"""
        
        # Add user message to history
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        tools = self._format_tools_for_llm()
        
        for iteration in range(self.max_iterations):
            # Call LLM
            response = self._call_llm(self.conversation_history, tools)
            
            # Check stop reason
            stop_reason = response.get('stop_reason')
            content = response.get('content', [])
            
            # Add assistant response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": content
            })
            
            # If no tool use, return the text response
            if stop_reason == 'end_turn':
                # Extract text from content
                for block in content:
                    if block.get('type') == 'text':
                        return block.get('text', '')
                return ""
            
            # If tool use, execute tools
            if stop_reason == 'tool_use':
                tool_results = []
                
                for block in content:
                    if block.get('type') == 'tool_use':
                        tool_name = block.get('name')
                        tool_input = block.get('input', {})
                        tool_id = block.get('id')
                        
                        # Execute tool
                        result = self._execute_tool(tool_name, tool_input)
                        
                        tool_results.append({
                            "type": "tool_result",
                            "tool_use_id": tool_id,
                            "content": json.dumps(result)
                        })
                
                # Add tool results to history
                self.conversation_history.append({
                    "role": "user",
                    "content": tool_results
                })
        
        return "Agent reached maximum iterations without completing."

# Usage
if __name__ == "__main__":
    from tools import TOOLS
    
    agent = ToolUsingAgent(tools=TOOLS)
    
    response = agent.run("What's the weather in San Francisco and what's 25 * 4?")
    print(response)
```

#### Step 3: Create FastAPI Service

```python
# app.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import uuid
import logging

from agent import ToolUsingAgent
from tools import TOOLS

app = FastAPI(title="Agent API")
logger = logging.getLogger(__name__)

# Store agents by session
agents: dict = {}

class ChatRequest(BaseModel):
    session_id: Optional[str] = None
    message: str

class ChatResponse(BaseModel):
    session_id: str
    response: str
    tool_calls: List[dict] = []

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    # Get or create session
    session_id = request.session_id or str(uuid.uuid4())
    
    if session_id not in agents:
        agents[session_id] = ToolUsingAgent(tools=TOOLS)
    
    agent = agents[session_id]
    
    try:
        response = agent.run(request.message)
        
        return ChatResponse(
            session_id=session_id,
            response=response,
            tool_calls=[]  # Could extract from agent history
        )
    except Exception as e:
        logger.error(f"Agent error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/session/{session_id}")
async def delete_session(session_id: str):
    if session_id in agents:
        del agents[session_id]
    return {"message": "Session deleted"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
```

---

## Multi-Agent Systems

### Multi-Agent Architecture Patterns

#### Pattern 1: Hierarchical (Manager-Worker)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    HIERARCHICAL MULTI-AGENT SYSTEM                       │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│                         ┌───────────────────┐                           │
│                         │   MANAGER AGENT   │                           │
│                         │   (Orchestrator)  │                           │
│                         │                   │                           │
│                         │ • Breaks down task│                           │
│                         │ • Assigns to      │                           │
│                         │   specialists     │                           │
│                         │ • Synthesizes     │                           │
│                         │   results         │                           │
│                         └─────────┬─────────┘                           │
│                                   │                                     │
│                   ┌───────────────┼───────────────┐                     │
│                   │               │               │                     │
│                   ▼               ▼               ▼                     │
│   ┌───────────────────┐ ┌───────────────────┐ ┌───────────────────┐    │
│   │  RESEARCH AGENT   │ │   WRITER AGENT    │ │  REVIEWER AGENT   │    │
│   │                   │ │                   │ │                   │    │
│   │ • Web search      │ │ • Content writing │ │ • Quality check   │    │
│   │ • Data gathering  │ │ • Formatting      │ │ • Fact verify     │    │
│   └───────────────────┘ └───────────────────┘ └───────────────────┘    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

#### Pattern 2: Collaborative (Peer-to-Peer)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    COLLABORATIVE MULTI-AGENT SYSTEM                      │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌───────────────────┐                     ┌───────────────────┐       │
│   │   AGENT A         │◄───────────────────►│     AGENT B       │       │
│   │   (Analyst)       │    Message Bus      │    (Planner)      │       │
│   └─────────┬─────────┘                     └─────────┬─────────┘       │
│             │                                         │                 │
│             │         ┌───────────────────┐           │                 │
│             └────────►│   SHARED STATE    │◄──────────┘                 │
│                       │   (Redis/DB)      │                             │
│             ┌────────►│                   │◄──────────┐                 │
│             │         └───────────────────┘           │                 │
│             │                                         │                 │
│   ┌─────────┴─────────┐                     ┌─────────┴─────────┐       │
│   │   AGENT C         │◄───────────────────►│     AGENT D       │       │
│   │   (Executor)      │    Message Bus      │    (Validator)    │       │
│   └───────────────────┘                     └───────────────────┘       │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

#### Pattern 3: Pipeline (Sequential)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                      PIPELINE MULTI-AGENT SYSTEM                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   Input                                                                 │
│     │                                                                   │
│     ▼                                                                   │
│   ┌───────────────────┐                                                 │
│   │   AGENT 1         │                                                 │
│   │   (Parser)        │──► Extract structured data                      │
│   └─────────┬─────────┘                                                 │
│             │                                                           │
│             ▼                                                           │
│   ┌───────────────────┐                                                 │
│   │   AGENT 2         │                                                 │
│   │   (Enricher)      │──► Add context, lookup references               │
│   └─────────┬─────────┘                                                 │
│             │                                                           │
│             ▼                                                           │
│   ┌───────────────────┐                                                 │
│   │   AGENT 3         │                                                 │
│   │   (Analyzer)      │──► Generate insights                            │
│   └─────────┬─────────┘                                                 │
│             │                                                           │
│             ▼                                                           │
│   ┌───────────────────┐                                                 │
│   │   AGENT 4         │                                                 │
│   │   (Formatter)     │──► Create final output                          │
│   └─────────┬─────────┘                                                 │
│             │                                                           │
│             ▼                                                           │
│   Output                                                                │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### Implementing Multi-Agent System

```python
# multi_agent.py
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum
import json
import asyncio

class AgentRole(Enum):
    MANAGER = "manager"
    RESEARCHER = "researcher"
    WRITER = "writer"
    REVIEWER = "reviewer"

@dataclass
class AgentMessage:
    from_agent: str
    to_agent: str
    content: str
    metadata: Dict = None

class BaseAgent:
    def __init__(self, name: str, role: AgentRole, llm_client):
        self.name = name
        self.role = role
        self.llm = llm_client
        self.system_prompt = self._get_system_prompt()
    
    def _get_system_prompt(self) -> str:
        prompts = {
            AgentRole.MANAGER: """You are a project manager agent. Your job is to:
1. Break down complex tasks into subtasks
2. Assign subtasks to specialist agents
3. Coordinate work and synthesize results
4. Ensure quality and completeness""",
            
            AgentRole.RESEARCHER: """You are a research agent. Your job is to:
1. Gather information from various sources
2. Analyze and summarize findings
3. Provide accurate, cited information""",
            
            AgentRole.WRITER: """You are a writing agent. Your job is to:
1. Create clear, well-structured content
2. Follow style guidelines
3. Incorporate feedback and revisions""",
            
            AgentRole.REVIEWER: """You are a review agent. Your job is to:
1. Check content for accuracy and quality
2. Identify issues and suggest improvements
3. Ensure requirements are met"""
        }
        return prompts.get(self.role, "You are a helpful AI assistant.")
    
    async def process(self, message: str, context: Dict = None) -> str:
        """Process a message and return response"""
        prompt = f"{self.system_prompt}\n\nContext: {json.dumps(context or {})}\n\nTask: {message}"
        response = await self.llm.generate(prompt)
        return response

class MultiAgentOrchestrator:
    def __init__(self, llm_client):
        self.llm = llm_client
        self.agents: Dict[str, BaseAgent] = {}
        self.message_queue: List[AgentMessage] = []
        self.shared_state: Dict = {}
    
    def register_agent(self, agent: BaseAgent):
        """Register an agent with the orchestrator"""
        self.agents[agent.name] = agent
    
    async def run_task(self, task: str) -> str:
        """Run a complex task using multiple agents"""
        
        # 1. Manager breaks down the task
        manager = self.agents.get("manager")
        if not manager:
            raise ValueError("No manager agent registered")
        
        plan = await manager.process(
            f"Break down this task into subtasks for researcher, writer, and reviewer agents: {task}"
        )
        
        # 2. Parse the plan and execute subtasks
        subtasks = self._parse_plan(plan)
        results = {}
        
        for subtask in subtasks:
            agent_name = subtask.get("agent")
            agent = self.agents.get(agent_name)
            
            if agent:
                result = await agent.process(
                    subtask.get("task"),
                    context={"previous_results": results}
                )
                results[agent_name] = result
        
        # 3. Manager synthesizes final result
        final_result = await manager.process(
            f"Synthesize these results into a final response: {json.dumps(results)}"
        )
        
        return final_result
    
    def _parse_plan(self, plan: str) -> List[Dict]:
        """Parse manager's plan into subtasks"""
        # Simple parsing - in production, use structured output
        subtasks = []
        for line in plan.split("\n"):
            if "researcher:" in line.lower():
                subtasks.append({"agent": "researcher", "task": line})
            elif "writer:" in line.lower():
                subtasks.append({"agent": "writer", "task": line})
            elif "reviewer:" in line.lower():
                subtasks.append({"agent": "reviewer", "task": line})
        return subtasks

# Example usage
async def main():
    # Initialize LLM client (your implementation)
    llm_client = YourLLMClient()
    
    # Create orchestrator
    orchestrator = MultiAgentOrchestrator(llm_client)
    
    # Create and register agents
    orchestrator.register_agent(BaseAgent("manager", AgentRole.MANAGER, llm_client))
    orchestrator.register_agent(BaseAgent("researcher", AgentRole.RESEARCHER, llm_client))
    orchestrator.register_agent(BaseAgent("writer", AgentRole.WRITER, llm_client))
    orchestrator.register_agent(BaseAgent("reviewer", AgentRole.REVIEWER, llm_client))
    
    # Run a task
    result = await orchestrator.run_task(
        "Write a comprehensive blog post about the benefits of cloud computing"
    )
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

---

## Cloud Deployment for Agentic Systems

### AWS Architecture for Multi-Agent System

```
┌─────────────────────────────────────────────────────────────────────────┐
│                AWS MULTI-AGENT DEPLOYMENT ARCHITECTURE                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌──────────┐     ┌──────────────┐     ┌─────────────────────────┐    │
│   │  Client  │────►│ API Gateway  │────►│   Lambda / ECS          │    │
│   │          │     │              │     │   (Orchestrator)        │    │
│   └──────────┘     └──────────────┘     └───────────┬─────────────┘    │
│                                                     │                   │
│                     ┌───────────────────────────────┤                   │
│                     │                               │                   │
│                     ▼                               ▼                   │
│   ┌────────────────────────────┐     ┌────────────────────────────┐    │
│   │   Step Functions           │     │       SQS Queues           │    │
│   │   (Agent Workflow)         │     │   (Agent Communication)    │    │
│   │                            │     │                            │    │
│   │   ┌─────┐ ┌─────┐ ┌─────┐ │     │  ┌────────┐ ┌────────┐    │    │
│   │   │Step1│►│Step2│►│Step3│ │     │  │Agent A │ │Agent B │    │    │
│   │   └─────┘ └─────┘ └─────┘ │     │  │ Queue  │ │ Queue  │    │    │
│   └────────────────────────────┘     │  └────────┘ └────────┘    │    │
│                                      └────────────────────────────┘    │
│                                                                         │
│   ┌────────────────────────────┐     ┌────────────────────────────┐    │
│   │   Bedrock                  │     │   DynamoDB                 │    │
│   │   (LLM for all agents)     │     │   (Agent State & Memory)   │    │
│   └────────────────────────────┘     └────────────────────────────┘    │
│                                                                         │
│   ┌────────────────────────────────────────────────────────────────┐   │
│   │                     CloudWatch                                  │   │
│   │   (Logging, Metrics, Tracing for all agent interactions)       │   │
│   └────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

### AWS Step Functions for Agent Workflow

```json
{
  "Comment": "Multi-Agent Workflow",
  "StartAt": "ManagerAgent",
  "States": {
    "ManagerAgent": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:us-east-1:xxx:function:manager-agent",
      "Next": "ParallelAgents"
    },
    "ParallelAgents": {
      "Type": "Parallel",
      "Branches": [
        {
          "StartAt": "ResearcherAgent",
          "States": {
            "ResearcherAgent": {
              "Type": "Task",
              "Resource": "arn:aws:lambda:us-east-1:xxx:function:researcher-agent",
              "End": true
            }
          }
        },
        {
          "StartAt": "WriterAgent",
          "States": {
            "WriterAgent": {
              "Type": "Task",
              "Resource": "arn:aws:lambda:us-east-1:xxx:function:writer-agent",
              "End": true
            }
          }
        }
      ],
      "Next": "ReviewerAgent"
    },
    "ReviewerAgent": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:us-east-1:xxx:function:reviewer-agent",
      "Next": "SynthesizeResults"
    },
    "SynthesizeResults": {
      "Type": "Task",
      "Resource": "arn:aws:lambda:us-east-1:xxx:function:synthesize-results",
      "End": true
    }
  }
}
```

### GCP Architecture for Multi-Agent System

```
┌─────────────────────────────────────────────────────────────────────────┐
│                GCP MULTI-AGENT DEPLOYMENT ARCHITECTURE                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│   ┌──────────┐     ┌──────────────┐     ┌─────────────────────────┐    │
│   │  Client  │────►│Cloud Endpoints│───►│   Cloud Run             │    │
│   │          │     │              │     │   (Orchestrator)        │    │
│   └──────────┘     └──────────────┘     └───────────┬─────────────┘    │
│                                                     │                   │
│                     ┌───────────────────────────────┤                   │
│                     │                               │                   │
│                     ▼                               ▼                   │
│   ┌────────────────────────────┐     ┌────────────────────────────┐    │
│   │   Cloud Workflows          │     │       Pub/Sub              │    │
│   │   (Agent Orchestration)    │     │   (Agent Messaging)        │    │
│   │                            │     │                            │    │
│   │   Sequential or parallel   │     │  Topics for each agent     │    │
│   │   agent execution          │     │  type or task type         │    │
│   └────────────────────────────┘     └────────────────────────────┘    │
│                                                                         │
│   ┌────────────────────────────┐     ┌────────────────────────────┐    │
│   │   Vertex AI                │     │   Firestore                │    │
│   │   (Gemini for agents)      │     │   (Agent State & Memory)   │    │
│   └────────────────────────────┘     └────────────────────────────┘    │
│                                                                         │
│   ┌────────────────────────────────────────────────────────────────┐   │
│   │                 Cloud Monitoring + Cloud Trace                  │   │
│   │   (Observability for agent interactions)                       │   │
│   └────────────────────────────────────────────────────────────────┘   │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Production Considerations for Agents

### 1. Safety and Guardrails

```python
# guardrails.py
from typing import Callable, Any
import re

class AgentGuardrails:
    """Safety guardrails for agent actions"""
    
    def __init__(self):
        self.blocked_patterns = [
            r"rm\s+-rf",
            r"DROP\s+TABLE",
            r"DELETE\s+FROM.*WHERE\s+1=1",
        ]
        self.max_tool_calls = 20
        self.max_tokens_per_response = 4096
        self.allowed_domains = ["api.weather.com", "api.search.com"]
    
    def validate_tool_input(self, tool_name: str, input_data: dict) -> bool:
        """Validate tool inputs before execution"""
        input_str = str(input_data)
        
        # Check for dangerous patterns
        for pattern in self.blocked_patterns:
            if re.search(pattern, input_str, re.IGNORECASE):
                return False
        
        # Check URL domains for web tools
        if tool_name == "fetch_url":
            url = input_data.get("url", "")
            if not any(domain in url for domain in self.allowed_domains):
                return False
        
        return True
    
    def validate_output(self, output: str) -> str:
        """Sanitize agent output"""
        # Remove potential PII
        output = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '[SSN REDACTED]', output)
        output = re.sub(r'\b\d{16}\b', '[CARD REDACTED]', output)
        return output

# Usage in agent
guardrails = AgentGuardrails()

def safe_execute_tool(tool_name: str, tool_input: dict) -> Any:
    if not guardrails.validate_tool_input(tool_name, tool_input):
        raise ValueError(f"Tool input validation failed for {tool_name}")
    
    result = execute_tool(tool_name, tool_input)
    return guardrails.validate_output(str(result))
```

### 2. State Management

```python
# state_manager.py
import boto3
from datetime import datetime
import json

class AgentStateManager:
    """Manage agent state in DynamoDB"""
    
    def __init__(self, table_name: str):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(table_name)
    
    def save_state(self, session_id: str, agent_name: str, state: dict):
        """Save agent state"""
        self.table.put_item(Item={
            'session_id': session_id,
            'agent_name': agent_name,
            'state': json.dumps(state),
            'timestamp': datetime.utcnow().isoformat()
        })
    
    def get_state(self, session_id: str, agent_name: str) -> dict:
        """Retrieve agent state"""
        response = self.table.get_item(Key={
            'session_id': session_id,
            'agent_name': agent_name
        })
        if 'Item' in response:
            return json.loads(response['Item']['state'])
        return {}
    
    def save_conversation(self, session_id: str, messages: list):
        """Save conversation history"""
        self.table.put_item(Item={
            'session_id': session_id,
            'agent_name': '_conversation',
            'state': json.dumps(messages),
            'timestamp': datetime.utcnow().isoformat()
        })
```

### 3. Observability

```python
# observability.py
import logging
import time
from functools import wraps
from typing import Callable
import json

# Configure structured logging
logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def trace_agent_call(func: Callable) -> Callable:
    """Decorator to trace agent calls"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        agent_name = kwargs.get('agent_name', 'unknown')
        
        logger.info(json.dumps({
            'event': 'agent_call_start',
            'agent': agent_name,
            'input': str(args)[:200]  # Truncate for logging
        }))
        
        try:
            result = await func(*args, **kwargs)
            
            duration = time.time() - start_time
            logger.info(json.dumps({
                'event': 'agent_call_end',
                'agent': agent_name,
                'duration_ms': round(duration * 1000, 2),
                'status': 'success'
            }))
            
            return result
            
        except Exception as e:
            duration = time.time() - start_time
            logger.error(json.dumps({
                'event': 'agent_call_error',
                'agent': agent_name,
                'duration_ms': round(duration * 1000, 2),
                'error': str(e)
            }))
            raise
    
    return wrapper

def track_tool_usage(tool_name: str, duration_ms: float, success: bool):
    """Track tool usage metrics"""
    logger.info(json.dumps({
        'event': 'tool_usage',
        'tool': tool_name,
        'duration_ms': duration_ms,
        'success': success
    }))
```

---

## Summary: Deployment Patterns

| Pattern | When to Use | AWS Services | GCP Services |
|---------|-------------|--------------|--------------|
| Single Agent | Simple tasks, single domain | Lambda + Bedrock | Cloud Run + Vertex AI |
| Hierarchical | Complex tasks, clear delegation | Step Functions + Lambda | Workflows + Cloud Functions |
| Collaborative | Peer review, consensus needed | SQS + ECS | Pub/Sub + Cloud Run |
| Pipeline | Sequential processing | Step Functions | Workflows |

---

## Next Steps

Continue to [Chapter 5: Best Practices](../05-best-practices/README.md) to learn about security, scalability, and monitoring for AI deployments.
