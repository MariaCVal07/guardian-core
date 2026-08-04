from pathlib import Path


def load_spec_file(filename: str, spec_type: str = "prompt") -> str | dict:
    """
    Carga archivos de especificación SDD.
    
    Args:
        filename: Nombre del archivo (ej: "strategy.md" o "strategy.json")
        spec_type: "prompt" para .md, "schema" para .json
        
    Returns:
        Contenido del archivo (str para prompts, dict para schemas)
    """
    agents_dir = Path(__file__).parent.parent / "agents"
    
    spec_path = next(
        agents_dir.rglob(filename),
        None
    )
    
    if spec_path is None or not spec_path.exists():
        raise FileNotFoundError(
            f"No existe el archivo: {filename}"
        )
    
    if spec_type == "prompt":
        return spec_path.read_text(encoding="utf-8")
    elif spec_type == "schema":
        import json
        return json.loads(spec_path.read_text(encoding="utf-8"))
    else:
        raise ValueError(f"spec_type inválido: {spec_type}")


def load_prompt(filename: str) -> str:
    """Carga un archivo de prompt (.md)"""
    return load_spec_file(filename, spec_type="prompt")


def load_schema(filename: str) -> dict:
    """Carga un archivo de schema (.json)"""
    return load_spec_file(filename, spec_type="schema")