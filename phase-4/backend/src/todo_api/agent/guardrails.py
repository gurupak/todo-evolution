"""Guardrails for AI agent input and output validation.

This module implements input and output guardrails using the OpenAI Agents SDK
to ensure the chatbot stays on topic and produces valid responses.
"""

from agents import Agent, GuardrailFunctionOutput, Runner, input_guardrail, output_guardrail
from pydantic import BaseModel

# ============================================================================
# Pydantic Models for Structured Guardrail Outputs
# ============================================================================


class TopicValidationOutput(BaseModel):
    """Output schema for topic validation guardrail."""

    is_todo_related: bool
    reasoning: str


class ResponseValidationOutput(BaseModel):
    """Output schema for response validation guardrail."""

    is_valid: bool
    reasoning: str


# ============================================================================
# Guardrail Agents
# ============================================================================

# Topic validation agent (runs as part of input guardrail)
topic_validator_agent = Agent(
    name="Topic Validator",
    instructions=(
        "You are a topic classifier for a todo task management system. "
        "Analyze the user's message and determine if it relates to todo/task management. "
        "\n\n"
        "**Todo-related topics include:**\n"
        "- Creating, adding, or making new tasks\n"
        "- Viewing, listing, or showing tasks\n"
        "- Updating, changing, or editing tasks\n"
        "- Completing, finishing, or marking tasks as done\n"
        "- Deleting or removing tasks\n"
        "- Asking about task status or priorities\n"
        "- Greetings or help requests that mention tasks/todos\n"
        "\n"
        "**NOT todo-related:**\n"
        "- General conversation (weather, news, jokes)\n"
        "- Questions about other topics (politics, sports, etc.)\n"
        "- Requests for information unrelated to task management\n"
        "- Inappropriate or harmful content\n"
        "\n"
        "Set is_todo_related=True if the message is about task management, False otherwise. "
        "Provide a brief reasoning for your decision."
    ),
    output_type=TopicValidationOutput,
)

# Response validation agent (runs as part of output guardrail)
response_validator_agent = Agent(
    name="Response Validator",
    instructions=(
        "You are a response quality validator for a todo task management chatbot. "
        "Analyze the AI's response and ensure it is valid and helpful. "
        "\n\n"
        "**Valid responses:**\n"
        "- Have actual content (not empty or just whitespace)\n"
        "- Provide clear information or confirmation to the user\n"
        "- Include task details when referencing tasks\n"
        "- Offer helpful guidance or clarification when needed\n"
        "- Error messages that explain what went wrong and how to fix it\n"
        "\n"
        "**Invalid responses:**\n"
        "- Empty or whitespace-only content\n"
        "- Generic error messages without context (e.g., 'Error occurred.')\n"
        "- Incomplete or truncated responses\n"
        "- Responses that don't address the user's request\n"
        "\n"
        "Set is_valid=True if the response is helpful and complete, False otherwise. "
        "Provide reasoning for your decision."
    ),
    output_type=ResponseValidationOutput,
)


# ============================================================================
# Input Guardrail: Topic Validation
# ============================================================================


@input_guardrail
async def todo_topic_guard(ctx, agent, input_data):
    """Input guardrail that blocks off-topic messages.

    This guardrail runs before the main agent and validates that the user's
    message is related to todo/task management. If the message is off-topic,
    the tripwire is triggered and the main agent will not execute.

    Args:
        ctx: Guardrail context containing request metadata
        agent: The main agent (not used in this guardrail)
        input_data: The user's message to validate

    Returns:
        GuardrailFunctionOutput with tripwire_triggered=True if off-topic
    """
    # Run the topic validation agent
    result = await Runner.run(topic_validator_agent, input_data, context=ctx.context)

    # Extract structured output
    output = result.final_output_as(TopicValidationOutput)

    # Trigger tripwire if message is NOT todo-related
    return GuardrailFunctionOutput(
        output_info=output, tripwire_triggered=not output.is_todo_related
    )


# ============================================================================
# Output Guardrail: Response Validation
# ============================================================================


@output_guardrail
async def response_validator_guard(ctx, agent, output_data):
    """Output guardrail that validates AI responses.

    This guardrail runs after the main agent and validates that the response
    is helpful, complete, and contains actual content. If the response is
    invalid (empty, unhelpful, or truncated), the tripwire is triggered.

    Args:
        ctx: Guardrail context containing request metadata
        agent: The main agent (not used in this guardrail)
        output_data: The AI's response to validate

    Returns:
        GuardrailFunctionOutput with tripwire_triggered=True if invalid
    """
    # Run the response validation agent
    result = await Runner.run(response_validator_agent, output_data, context=ctx.context)

    # Extract structured output
    output = result.final_output_as(ResponseValidationOutput)

    # Trigger tripwire if response is invalid
    return GuardrailFunctionOutput(output_info=output, tripwire_triggered=not output.is_valid)
