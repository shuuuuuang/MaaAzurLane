from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

AssetKind = Literal["template", "screenshot", "anchor", "pipeline", "metadata"]
AssetStatus = Literal["placeholder", "copied", "modified", "derived"]
ASSET_KINDS = {"template", "screenshot", "anchor", "pipeline", "metadata"}
ASSET_STATUSES = {"placeholder", "copied", "modified", "derived"}


@dataclass(frozen=True)
class UpstreamSource:
    """External project that may provide reference behavior or assets."""

    id: str
    name: str
    repository: str
    license: str
    license_url: str
    notes: str = ""

    def validate(self) -> None:
        if not self.id:
            raise ValueError("upstream source requires id")
        if not self.name:
            raise ValueError(f"upstream source {self.id} requires name")
        if not self.repository.startswith("https://github.com/"):
            raise ValueError(f"upstream source {self.id} must use a GitHub URL")
        if not self.license:
            raise ValueError(f"upstream source {self.id} requires license")
        if not self.license_url:
            raise ValueError(f"upstream source {self.id} requires license_url")

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> UpstreamSource:
        source = cls(
            id=str(data["id"]),
            name=str(data["name"]),
            repository=str(data["repository"]),
            license=str(data["license"]),
            license_url=str(data["license_url"]),
            notes=str(data.get("notes", "")),
        )
        source.validate()
        return source


@dataclass(frozen=True)
class AssetSource:
    """Source record for one committed or planned reference asset."""

    id: str
    kind: AssetKind
    target_path: str
    upstream: str | None
    source_path: str | None
    license: str
    status: AssetStatus
    usage: str
    notes: str = ""

    def validate(self, upstream_ids: set[str]) -> None:
        if not self.id:
            raise ValueError("asset source requires id")
        if self.kind not in ASSET_KINDS:
            raise ValueError(f"asset source {self.id} has invalid kind")
        if self.status not in ASSET_STATUSES:
            raise ValueError(f"asset source {self.id} has invalid status")
        if not self.target_path:
            raise ValueError(f"asset source {self.id} requires target_path")
        if self.target_path.startswith("/") or "\\" in self.target_path:
            raise ValueError(
                f"asset source {self.id} target_path must be a relative POSIX path"
            )
        if not self.license:
            raise ValueError(f"asset source {self.id} requires license")
        if not self.usage:
            raise ValueError(f"asset source {self.id} requires usage")
        if self.upstream is not None and self.upstream not in upstream_ids:
            raise ValueError(f"asset source {self.id} references unknown upstream")
        if self.status in {"copied", "modified"}:
            if self.upstream is None:
                raise ValueError(f"{self.status} asset {self.id} requires upstream")
            if not self.source_path:
                raise ValueError(f"{self.status} asset {self.id} requires source_path")
        if self.status == "derived" and self.source_path and self.upstream is None:
            raise ValueError(f"derived asset {self.id} with source_path needs upstream")

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> AssetSource:
        upstream = data.get("upstream")
        source_path = data.get("source_path")
        source = cls(
            id=str(data["id"]),
            kind=data["kind"],
            target_path=str(data["target_path"]),
            upstream=None if upstream is None else str(upstream),
            source_path=None if source_path is None else str(source_path),
            license=str(data["license"]),
            status=data["status"],
            usage=str(data["usage"]),
            notes=str(data.get("notes", "")),
        )
        return source


@dataclass(frozen=True)
class SourceIndex:
    """Traceability index for reference assets and upstream repositories."""

    schema_version: int
    upstreams: list[UpstreamSource]
    assets: list[AssetSource]

    def validate(self) -> None:
        if self.schema_version != 1:
            raise ValueError("source index schema_version must be 1")
        upstream_ids = [source.id for source in self.upstreams]
        if len(upstream_ids) != len(set(upstream_ids)):
            raise ValueError("source index contains duplicate upstream ids")
        asset_ids = [asset.id for asset in self.assets]
        if len(asset_ids) != len(set(asset_ids)):
            raise ValueError("source index contains duplicate asset ids")
        ids = set(upstream_ids)
        for source in self.upstreams:
            source.validate()
        for asset in self.assets:
            asset.validate(ids)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SourceIndex:
        index = cls(
            schema_version=int(data["schema_version"]),
            upstreams=[
                UpstreamSource.from_dict(source)
                for source in data.get("upstreams", [])
            ],
            assets=[
                AssetSource.from_dict(asset)
                for asset in data.get("assets", [])
            ],
        )
        index.validate()
        return index

    @classmethod
    def load(cls, path: Path) -> SourceIndex:
        with path.open("r", encoding="utf-8") as file:
            return cls.from_dict(json.load(file))
