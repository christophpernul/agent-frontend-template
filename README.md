# agent-frontend-template

This is a template repository for building a frontend interface for an AI agent using Gradio or Chainlit.
It provides a basic structure and example code to help you get started quickly.

## Run Agents

1. **Install dependencies:**
   ```bash
   uv sync
   ```

2. **Set up environment variables:**
   Create a `.env` file in the project root:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

### Gradio

Run Gradio application with this command:
```bash
   python run_gradio.py
```

### Chainlit

Run chainlit application with this command:
```bash
   chainlit run run_chainlit.py -w
```

## Links

### Docus
- [openai-agents-python Docu](https://openai.github.io/openai-agents-python/)
- [OpenAI Agents Docu](https://platform.openai.com/docs/guides/agents)
- [LangGraph Docu](https://docs.langchain.com/oss/python/langgraph/overview)


### Prompting & Architecture

- [Claude Cookbook](https://github.com/anthropics/claude-cookbooks/tree/main/patterns/agents)
- [Anthropic - Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents#agents)

### Models

- [OpenAI](https://platform.openai.com/settings/organization/general)
- [Gemini](https://aistudio.google.com/projects)

### MCP Server Catalogs
- [MCP.so](https://mcp.so)
- [Glama](https://glama.ai/mcp)
- [Smithery](https://smithery.ai/)
- [Huggingface Top11](https://huggingface.co/blog/LLMhacker/top-11-essential-mcp-libraries)

### MCP Servers
- [Polygon Stock Data](https://massive.com/)
- [Brave search](https://brave.com/search/api/)
- [Knowledge Graph Memory](https://github.com/modelcontextprotocol/servers/tree/main/src/memory)

### Blogs
- [Why MCP?](https://huggingface.co/blog/Kseniase/mcp)
- [12-factor-agents](https://github.com/humanlayer/12-factor-agents?ref=blog.langchain.com)
