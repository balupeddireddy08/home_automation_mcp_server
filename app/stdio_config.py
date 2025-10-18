"""Configuration for MCP stdio server integration with Claude Desktop and other AI assistants."""
import json
from pathlib import Path


def get_claude_desktop_config():
    """
    Generate configuration for Claude Desktop integration.
    
    Add this to your Claude Desktop config file:
    - Windows: %APPDATA%/Claude/claude_desktop_config.json
    - macOS: ~/Library/Application Support/Claude/claude_desktop_config.json
    - Linux: ~/.config/Claude/claude_desktop_config.json
    """
    
    project_root = Path(__file__).parent.parent
    mcp_server_path = project_root / "app" / "mcp_server_stdio.py"
    
    config = {
        "mcpServers": {
            "home-automation": {
                "command": "python",
                "args": [str(mcp_server_path)],
                "env": {}
            }
        }
    }
    
    return json.dumps(config, indent=2)


if __name__ == "__main__":
    print("=== Claude Desktop Configuration ===\n")
    print("Add this to your Claude Desktop config file:\n")
    print(get_claude_desktop_config())
    print("\n=== Configuration file locations ===")
    print("Windows: %APPDATA%/Claude/claude_desktop_config.json")
    print("macOS: ~/Library/Application Support/Claude/claude_desktop_config.json")
    print("Linux: ~/.config/Claude/claude_desktop_config.json")

