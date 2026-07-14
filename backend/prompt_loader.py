from pathlib import Path


def load_prompt(*args) -> str:
    """
    Compatible con:

    load_prompt("strategy.md")

    y

    load_prompt(__file__, "strategy.md")
    """

    if len(args) == 1:

        prompt_name = args[0]

        agents_dir = Path(__file__).parent / "agents"

        prompt_path = next(
            agents_dir.rglob(prompt_name),
            None
        )

    elif len(args) == 2:

        agent_file, prompt_name = args

        agent_dir = Path(agent_file).parent

        prompt_path = agent_dir / prompt_name

    else:

        raise TypeError("Parámetros inválidos para load_prompt().")

    if prompt_path is None or not prompt_path.exists():

        raise FileNotFoundError(
            f"No existe el prompt: {prompt_name}"
        )

    return prompt_path.read_text(
        encoding="utf-8"
    )