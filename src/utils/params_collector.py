from typing import Any, Dict


class ParamsCollector:
    def __init__(self, init_params: Dict[str, Any] | None = None) -> None:
        self.params = init_params or {}

    def get_param(self, key: str) -> Any:
        return self.params.get(key)

    def add_param(self, key: str, value: Any, exclude_none: bool = False) -> None:
        if exclude_none:
            if value is None:
                return
        self.params[key] = value

    def update_param(self, key: str, updated_value: Any) -> None:
        if key in self.params:
            self.params[key] = updated_value

    def delete_param(self, key: str) -> None:
        if key in self.params:
            del self.params[key]

    def __repr__(self) -> str:
        return f"<ParamsCollector params={self.params}>"
