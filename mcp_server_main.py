"""
MCP Server with Calculator Tools
A Model Context Protocol server that provides basic calculator operations.
"""

from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("calculator-server")


@mcp.tool()
def add(a: float, b: float) -> float:
    """
    Add two numbers together.

    Args:
        a: First number
        b: Second number

    Returns:
        Sum of a and b
    """
    return a + b


@mcp.tool()
def subtract(a: float, b: float) -> float:
    """
    Subtract second number from first number.

    Args:
        a: First number (minuend)
        b: Second number (subtrahend)

    Returns:
        Difference of a and b
    """
    return a - b


@mcp.tool()
def multiply(a: float, b: float) -> float:
    """
    Multiply two numbers together.

    Args:
        a: First number
        b: Second number

    Returns:
        Product of a and b
    """
    return a * b


@mcp.tool()
def divide(a: float, b: float) -> float:
    """
    Divide first number by second number.

    Args:
        a: Numerator
        b: Denominator

    Returns:
        Quotient of a divided by b

    Raises:
        ValueError: If b is zero
    """
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


@mcp.tool()
def power(base: float, exponent: float) -> float:
    """
    Raise base to the power of exponent.

    Args:
        base: Base number
        exponent: Exponent (power)

    Returns:
        Result of base raised to exponent
    """
    return base ** exponent


@mcp.tool()
def modulo(a: float, b: float) -> float:
    """
    Calculate remainder of division.

    Args:
        a: Dividend
        b: Divisor

    Returns:
        Remainder of a divided by b

    Raises:
        ValueError: If b is zero
    """
    print("------------------------------------------------------------------------------")
    if b == 0:
        raise ValueError("Cannot perform modulo with zero divisor")
    return a % b


@mcp.tool()
def square_root(n: float) -> float:
    """
    Calculate square root of a number.

    Args:
        n: Number to find square root of

    Returns:
        Square root of n

    Raises:
        ValueError: If n is negative
    """
    if n < 0:
        raise ValueError("Cannot calculate square root of negative number")
    return n ** 0.5


@mcp.tool()
def absolute(n: float) -> float:
    """
    Get absolute value of a number.

    Args:
        n: Input number

    Returns:
        Absolute value of n
    """
    return abs(n)


if __name__ == "__main__":
    # Run the MCP server
    mcp.run()
