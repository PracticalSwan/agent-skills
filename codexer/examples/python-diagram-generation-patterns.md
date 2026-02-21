# Python Diagram Generation Patterns (Graphviz)

Python patterns for generating ER diagrams and flowcharts with Graphviz, tailored for the Recipe Sharing System diagram scripts.

## Use Case
This project uses Python for diagram generation only (ER models, data flow, and flowcharts).

## Recommended Stack
- Python 3.11+
- graphviz Python package
- Graphviz system binary installed and in PATH

```bash
pip install graphviz
```

## Basic Graphviz Flowchart

```python
from graphviz import Digraph


def generate_app_flowchart(output_path: str = "application_flowchart") -> None:
    graph = Digraph("RecipeSharingFlow", format="png")
    graph.attr(rankdir="LR", fontsize="12")

    graph.node("U", "User", shape="oval")
    graph.node("F", "React Frontend", shape="box")
    graph.node("A", "PHP API", shape="box")
    graph.node("D", "MySQL Database", shape="cylinder")

    graph.edge("U", "F", label="interact")
    graph.edge("F", "A", label="HTTP/JSON")
    graph.edge("A", "D", label="SQL")
    graph.edge("D", "A", label="result")
    graph.edge("A", "F", label="JSON response")

    graph.render(output_path, cleanup=True)


if __name__ == "__main__":
    generate_app_flowchart()
```

## ER Logical Diagram Pattern

```python
from graphviz import Digraph


def add_entity(graph: Digraph, name: str, fields: list[str]) -> None:
    label = "{\n" + name + "|\n" + "\n".join(fields) + "\n}"
    graph.node(name, label=label, shape="record")


def generate_er_logical(output_path: str = "er_logical") -> None:
    graph = Digraph("ERLogical", format="png")
    graph.attr(rankdir="LR")

    add_entity(graph, "user", [
        "id (PK)",
        "username",
        "email",
        "password_hash",
        "role",
        "status",
        "created_at",
        "updated_at",
    ])

    add_entity(graph, "recipe", [
        "id (PK)",
        "title",
        "description",
        "category",
        "difficulty",
        "author_id (FK -> user.id)",
        "status",
        "created_at",
        "updated_at",
    ])

    add_entity(graph, "review", [
        "id (PK)",
        "user_id (FK -> user.id)",
        "recipe_id (FK -> recipe.id)",
        "rating",
        "comment",
        "created_at",
        "updated_at",
    ])

    graph.edge("user", "recipe", label="1:N", arrowhead="crow")
    graph.edge("user", "review", label="1:N", arrowhead="crow")
    graph.edge("recipe", "review", label="1:N", arrowhead="crow")

    graph.render(output_path, cleanup=True)


if __name__ == "__main__":
    generate_er_logical()
```

## Diagram Generation Best Practices
- Keep node IDs stable for diff-friendly output.
- Separate diagram structure from rendering function.
- Use helper functions (`add_entity`, `add_relation`) for consistency.
- Generate to a deterministic path under `python_diagrams/`.
- Keep labels concise; put full docs in markdown.

## File Organization Pattern

```text
python_diagrams/
  data_flow_graphviz.py
  er_recipe_conceptual_graphviz.py
  er_recipe_logical_graphviz.py
  flowchart_graphviz.py
```

## CLI Entrypoint Pattern

```python
import argparse


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate Recipe Sharing diagrams")
    parser.add_argument("--type", choices=["flow", "er-logical", "er-conceptual"], required=True)
    parser.add_argument("--output", default="diagram")
    args = parser.parse_args()

    if args.type == "flow":
        generate_app_flowchart(args.output)
    elif args.type == "er-logical":
        generate_er_logical(args.output)
    else:
        generate_er_conceptual(args.output)


if __name__ == "__main__":
    main()
```

## Common Issues

### Graphviz executable not found
- Error: `ExecutableNotFound: failed to execute 'dot'`
- Fix: install Graphviz and add `dot` binary to PATH.

### Unicode rendering issues
- Set font explicitly in graph attributes:

```python
graph.attr(fontname="Arial")
graph.node_attr.update(fontname="Arial")
graph.edge_attr.update(fontname="Arial")
```

### Output file not updating
- Use `cleanup=True` in `render()`.
- Ensure output path is writable.

## References
- Python docs: https://docs.python.org/3/
- Graphviz package: https://graphviz.readthedocs.io/
- Graphviz DOT language: https://graphviz.org/doc/info/lang.html
