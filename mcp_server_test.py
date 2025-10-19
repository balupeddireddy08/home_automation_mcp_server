"""Simplified MCP Server for testing with MCP Inspector."""
from mcp.server.fastmcp import FastMCP

# Create FastMCP server
mcp = FastMCP(
    name="home-automation-mcp",
    instructions="""
    You are a smart home automation assistant. You can control lights, thermostats, locks,
    blinds, fans, garage doors, sprinklers, EV chargers, and other smart home devices.
    
    This is a test server to verify MCP tools are working correctly.
    """
)


@mcp.tool()
def hello_world(name: str = "World") -> str:
    """Simple hello world tool to test MCP is working."""
    return f"Hello, {name}! MCP Server is working!"


@mcp.tool()
def add_numbers(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b


@mcp.tool()
def get_test_status() -> str:
    """Get test status message."""
    return "✅ All MCP tools are functioning correctly!"


if __name__ == "__main__":
    # Run the MCP server with stdio transport
    mcp.run(transport="stdio")

