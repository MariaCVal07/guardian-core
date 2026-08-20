def normalize_business_model(model: dict) -> dict:

    if not model:
        model = {}

    # -----------------------------
    # Garantizar listas
    # -----------------------------

    list_fields = [
        "actors",
        "entities",
        "relationships",
        "business_rules",
        "constraints",
        "preconditions",
        "postconditions",
        "valid_states",
        "invalid_states",
        "functional_flow",
        "ambiguities",
        "missing_information",
        "invariants",
        "assumptions"
    ]

    for field in list_fields:
        if not isinstance(model.get(field), list):
            model[field] = []

    # -----------------------------
    # Eliminar duplicados simples
    # -----------------------------

    simple_lists = [
        "actors",
        "entities",
        "constraints",
        "preconditions",
        "postconditions",
        "valid_states",
        "invalid_states",
        "functional_flow",
        "invariants",
        "missing_information",
        "assumptions"
    ]

    for field in simple_lists:

        clean = []

        for item in model[field]:

            if isinstance(item, str):

                item = item.strip()

                if item and item not in clean:
                    clean.append(item)

        model[field] = clean

    # -----------------------------
    # Normalizar relationships
    # -----------------------------

    relationships = []

    for rel in model["relationships"]:

        if not isinstance(rel, dict):
            continue

        source = rel.get("source")
        relation = rel.get("relationship")
        target = rel.get("target")

        if source and relation and target:

            relationships.append({
                "source": source.strip(),
                "relationship": relation.strip(),
                "target": target.strip()
            })

    model["relationships"] = relationships

    # -----------------------------
    # Normalizar Business Rules
    # -----------------------------

    rules = []

    for rule in model["business_rules"]:

        if isinstance(rule, dict):

            text = rule.get("rule", "").strip()

            evidence = rule.get("evidence", "").strip()

            if text:

                rules.append({
                    "rule": text,
                    "evidence": evidence
                })

        elif isinstance(rule, str):

            rule = rule.strip()

            if rule:

                rules.append({
                    "rule": rule,
                    "evidence": ""
                })

    model["business_rules"] = rules

    # -----------------------------
    # Eliminar constraints duplicadas
    # -----------------------------

    rule_texts = {
        r["rule"].lower()
        for r in model["business_rules"]
    }

    model["constraints"] = [

        c

        for c in model["constraints"]

        if c.lower() not in rule_texts

    ]

    # -----------------------------
    # Eliminar invariantes duplicados
    # -----------------------------

    model["invariants"] = [

        i

        for i in model["invariants"]

        if i.lower() not in rule_texts

    ]

    return model