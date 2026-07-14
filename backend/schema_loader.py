from pathlib import Path


def load_schema(*args) -> dict:
    """
    Compatible con:

    load_schema("strategy.json")

    y

    load_schema(__file__, "strategy.json")
    """

    if len(args) == 1:

        schema_name = args[0]

        agents_dir = Path(__file__).parent / "agents"

        schema_path = next(
            agents_dir.rglob(schema_name),
            None
        )

    elif len(args) == 2:

        agent_file, schema_name = args

        agent_dir = Path(agent_file).parent

        schema_path = agent_dir / schema_name

    else:

        raise TypeError("Parámetros inválidos para load_schema().")

    if schema_path is None or not schema_path.exists():

        raise FileNotFoundError(
            f"No existe el schema: {schema_name}"
        )

    return schema_path.read_text(
        encoding="utf-8"
    )