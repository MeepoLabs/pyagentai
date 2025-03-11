"""Core functionality for your_package_name."""

from typing import Any


class YourClass:
    """A sample class for demonstration purposes.

    This class serves as a template for creating your own classes.

    Attributes:
        parameter: A sample parameter to demonstrate class initialization.
    """

    def __init__(self, parameter: str) -> None:
        """Initialize the YourClass instance.

        Args:
            parameter: A sample parameter to store.
        """
        self.parameter = parameter

    def method(self) -> str:
        """Perform a sample operation.

        Returns:
            A string result from the operation.
        """
        return f"Operation completed with parameter: {self.parameter}"


def your_function(input_data: str) -> dict[str, Any]:
    """Process the input data and return a result.

    This function serves as a template for creating your own functions.

    Args:
        input_data: The input data to process.

    Returns:
        A dictionary containing the processing results.
    """
    return {
        "input": input_data,
        "processed": True,
        "result": f"Processed: {input_data}",
    }
