"""Read-only audit of history-v1-style batches and an optional checkpoint.

Exit 1 means conflicting/invalid evidence; identical replay is an observation.
Exit 2 means the input could not be read. This is not a full schema validator.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys


def positive(value):
    return type(value) is int and value > 0


def identity(value):
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{32}", value) is not None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="+", type=Path, help="batch directories or roots containing batches")
    parser.add_argument("--checkpoint", type=Path)
    parser.add_argument("--stream-id", help="stream to compare against the checkpoint")
    parser.add_argument("--out", type=Path, help="new JSON report file; also prints JSON")
    args = parser.parse_args()
    manifests = set()
    for path in args.paths:
        path = path.resolve(strict=True)
        if not path.is_dir():
            parser.error(f"not a directory: {path}")
        if (path / "manifest.json").is_file():
            manifests.add(path / "manifest.json")
        else:
            for candidate in path.rglob("manifest.json"):
                if not any(part.startswith(".") for part in candidate.relative_to(path).parts[:-1]):
                    manifests.add(candidate)
    if not manifests:
        parser.error("no published manifest.json files found")
    errors = []
    observations = []
    positions = {}
    deliveries = {}
    streams = {}

    def error(code, **detail):
        errors.append({"code": code, **detail})

    for manifest_path in sorted(manifests):
        batch = str(manifest_path.parent)
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if not isinstance(manifest, dict):
            error("invalid_manifest", batch=batch)
            continue
        stream = manifest.get("stream")
        metadata = manifest.get("events")
        if not isinstance(stream, dict) or not isinstance(metadata, dict):
            error("invalid_manifest", batch=batch)
            continue
        stream_id = stream.get("stream_id")
        if not identity(stream_id):
            error("invalid_stream_id", batch=batch)
            continue
        sequences = streams.setdefault(stream_id, set())
        event_path = metadata.get("path")
        if event_path != "events.jsonl":
            error("unsupported_event_path", batch=batch)
            continue
        content = (manifest_path.parent / "events.jsonl").read_bytes()
        if metadata.get("sha256") is not None and metadata["sha256"] != hashlib.sha256(content).hexdigest():
            error("events_hash_mismatch", batch=batch)
        events = [json.loads(line) for line in content.decode("utf-8").splitlines() if line.strip()]
        count = metadata.get("count")
        if type(count) is not int or count != len(events):
            error("event_count_mismatch", batch=batch)
        start, end = stream.get("sequence_start"), stream.get("sequence_end")
        valid_range = positive(start) and positive(end) and end == start + max(0, len(events) - 1)
        if not valid_range:
            error("invalid_sequence_range", batch=batch)
        for offset, event in enumerate(events):
            if not isinstance(event, dict):
                error("invalid_event", batch=batch, index=offset)
                continue
            seq, event_id = event.get("sequence"), event.get("event_id")
            if not positive(seq) or not identity(event_id):
                error("invalid_event_identity_or_sequence", batch=batch, index=offset)
                continue
            if event.get("stream_id") != stream_id:
                error("event_stream_mismatch", batch=batch, event_id=event_id)
            if valid_range and seq != start + offset:
                error("event_sequence_out_of_order", batch=batch, sequence=seq)
            sequences.add(seq)
            signature = hashlib.sha256(json.dumps(event, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")).hexdigest()
            prior_position = positions.get((stream_id, seq))
            if prior_position is not None and prior_position[0] != signature:
                error("sequence_collision", stream_id=stream_id, sequence=seq,
                      first_batch=prior_position[1], conflicting_batch=batch)
            else:
                positions[(stream_id, seq)] = (signature, batch)
            prior_event = deliveries.get((stream_id, event_id))
            if prior_event is not None:
                if prior_event[0] != signature:
                    error("conflicting_event_delivery", stream_id=stream_id, event_id=event_id,
                          first_batch=prior_event[1], conflicting_batch=batch)
                else:
                    observations.append({"code": "identical_event_replay", "stream_id": stream_id,
                                         "event_id": event_id, "batch": batch})
            else:
                deliveries[(stream_id, event_id)] = (signature, batch)
    for stream_id, sequences in streams.items():
        ordered = sorted(sequences)
        for previous, current in zip(ordered, ordered[1:], strict=False):
            if current != previous + 1:
                error("sequence_gap_in_supplied_batches", stream_id=stream_id, after=previous, before=current)

    if args.checkpoint:
        checkpoint = json.loads(args.checkpoint.read_text(encoding="utf-8"))
        selected = args.stream_id
        if selected is None:
            if len(streams) != 1:
                parser.error("--stream-id is required with multiple streams and a checkpoint")
            selected = next(iter(streams))
        if selected not in streams:
            parser.error("selected stream is not present in the supplied batches")
        if not isinstance(checkpoint, dict) or checkpoint.get("stream_id") != selected:
            error("checkpoint_stream_mismatch", expected_stream_id=selected)
        else:
            next_seq, ids = checkpoint.get("next_sequence"), checkpoint.get("exported_event_ids")
            if not positive(next_seq):
                error("invalid_checkpoint_next_sequence")
            elif streams[selected] and next_seq <= max(streams[selected]):
                error("checkpoint_reuses_published_sequence", next_sequence=next_seq,
                      max_published_sequence=max(streams[selected]))
            if not isinstance(ids, list) or not all(identity(item) for item in ids):
                error("invalid_checkpoint_event_ids")
            elif len(ids) != len(set(ids)):
                error("duplicate_checkpoint_event_ids")
            else:
                published_ids = {event_id for stream, event_id in deliveries if stream == selected}
                missing = published_ids - set(ids)
                if missing:
                    error("published_events_missing_from_checkpoint", count=len(missing))
                if set(ids) - published_ids:
                    observations.append({"code": "checkpoint_events_outside_supplied_batches",
                                         "count": len(set(ids) - published_ids)})
    report = {
        "ok": not errors, "batch_count": len(manifests), "stream_count": len(streams),
        "unique_events": len(deliveries), "errors": errors, "observations": observations,
        "limitation": "Only supplied batches were inspected; no business or full schema validation.",
    }
    rendered = json.dumps(report, indent=2) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        with args.out.open("x", encoding="utf-8") as target:
            target.write(rendered)
    print(rendered, end="")
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, ValueError) as error:
        print(f"delivery audit failed: {error}", file=sys.stderr)
        sys.exit(2)
