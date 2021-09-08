from typing import TYPE_CHECKING, Any, Iterable, Protocol, TypeVar

from pyrogram.filters import Filter

if TYPE_CHECKING:
    from Protector.core import Protector

TypeData = TypeVar("TypeData", covariant=True)


class CustomFilter(Filter):  # skipcq: PYL-W0223
    anjani: "Protector"
    include_bot: bool


class NDArray(Protocol[TypeData]):
    def __getitem__(self, key: int) -> Any: ...  # skipcq: PTC-W0049
    @property
    def size(self) -> int: ...  # skipcq: PTC-W0049


class Pipeline(Protocol):
    def predict(self, X: Iterable[Any], **predict_params: Any) -> NDArray[Any]: ...  # skipcq: PTC-W0049
    def predict_proba(self, X: Iterable[Any]) -> NDArray[Any]: ...  # skipcq: PTC-W0049
