#!/usr/bin/env python3
"""Offline image-series planner, exact-text compositor and evidence-based reporter."""
from __future__ import annotations

import argparse
import base64
import hashlib
import html
import io
import json
import re
import shutil
import sys
from pathlib import Path

VERSION = "1.0.0"
ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}\Z")


def read(path):
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def value_hash(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


def require(ok, message):
    if not ok:
        raise ValueError(message)


def size_ok(size):
    return (isinstance(size, list) and len(size) == 2
            and all(type(n) is int and 64 <= n <= 8192 for n in size))


def validate_pack(p):
    require(p.get("schema_version") == 1, "Unsupported style schema")
    require(isinstance(p.get("id"), str) and ID.fullmatch(p["id"]), "Invalid style ID")
    for key in ("name", "version", "style_prompt"):
        require(isinstance(p.get(key), str) and p[key].strip(), f"Missing {key}")
    require(p.get("category") in ("illustration", "wallpaper", "photo-cover"), "Unsupported category")
    require(size_ok(p.get("default_size")), "Invalid default_size")
    require(p.get("text_mode") in ("none", "overlay"), "Invalid text_mode")
    for key in ("avoid", "composition_presets", "review_checks"):
        require(isinstance(p.get(key), list) and p[key] and
                all(isinstance(s, str) and s.strip() for s in p[key]), f"Invalid {key}")
    require(set(("style", "semantic", "clean")) <= set(p["review_checks"]), "Missing base review checks")
    if p["text_mode"] == "overlay":
        require(p["category"] == "wallpaper", "overlay requires wallpaper category")
        require("text" in p["review_checks"], "overlay requires text review")
        require(re.fullmatch(r"#[0-9a-fA-F]{6}", p.get("text_color", "")), "Invalid text_color")
        area = p.get("text_area", [.12, .25, .88, .75])
        require(isinstance(area, list) and len(area) == 4 and
                all(type(v) in (int, float) and 0 <= v <= 1 for v in area) and
                area[0] < area[2] and area[1] < area[3], "Invalid text_area")


def compile_batch(pack_path, tasks_path, out):
    p = read(pack_path)
    validate_pack(p)
    tasks = [json.loads(line) for line in Path(tasks_path).read_text(encoding="utf-8-sig").splitlines() if line.strip()]
    require(tasks, "Empty task list")
    seen, manifests = set(), []
    for i, task in enumerate(tasks):
        require(isinstance(task, dict), "Task must be an object")
        tid = task.get("id")
        require(isinstance(tid, str) and ID.fullmatch(tid), "Unsafe task ID")
        require(tid not in seen, f"Duplicate ID: {tid}")
        seen.add(tid)
        require(isinstance(task.get("topic"), str) and task["topic"].strip(), f"Missing topic: {tid}")
        for key in ("scene", "composition", "character_lock"):
            require(key not in task or isinstance(task[key], str), f"Invalid {key}: {tid}")
        must = task.get("must_show", [])
        require(isinstance(must, list) and all(isinstance(s, str) and s.strip() for s in must), "Invalid must_show")
        size = task.get("size", p["default_size"])
        require(size_ok(size), f"Invalid size: {tid}")
        if p["text_mode"] == "overlay":
            require(isinstance(task.get("copy"), str) and task["copy"].strip(), f"Missing exact copy: {tid}")
            require(task.get("copy_layout", "center") in ("center", "vertical"), "Invalid copy_layout")
            require(all(s.strip() for s in task["copy"].split("\n")), "Blank copy lines unsupported")
        else:
            require(not task.get("copy"), "This style has text_mode=none; create a text-enabled style for copy")
        composition = task.get("composition") or p["composition_presets"][i % len(p["composition_presets"])]
        prompt = (f"Create ONE complete {size[0]}x{size[1]} image; compose for this actual aspect ratio.\n"
                  f"Style: {p['style_prompt']}\nTopic: {task['topic']}\n"
                  f"Scene: {task.get('scene') or task['topic']}\nComposition: {composition}\n")
        if task.get("character_lock"):
            prompt += f"Preserve character identity: {task['character_lock']}\n"
        if must:
            prompt += "Must clearly show: " + "; ".join(must) + "\n"
        prompt += "Avoid: " + "; ".join(p["avoid"]) + "\n"
        if p["text_mode"] == "overlay":
            prompt += "Generate the BACKGROUND ONLY. No letters, calligraphy, pseudo-text, numbers or symbols. Keep the text area quiet; exact typography will be composited later.\n"
        m = {"id": tid, "task": task, "size": size, "composition": composition,
             "style_id": p["id"], "style_version": p["version"],
             "generation_prompt": prompt, "status": "planned"}
        manifests.append(m)
    out = Path(out)
    require(not out.exists(), f"Output already exists: {out}; use a new batch version")
    out.mkdir(parents=True)
    plan = {"tool_version": VERSION, "style": p, "items": manifests}
    write(out / "plan.json", plan)
    for m in manifests:
        write(out / "manifests" / (m["id"] + ".json"), m)
    print(f"Compiled {len(manifests)} tasks; no images generated: {out}")


def get_item(batch, tid):
    require(isinstance(tid, str) and ID.fullmatch(tid), "Unsafe task ID")
    plan = read(Path(batch) / "plan.json")
    validate_pack(plan["style"])
    matches = [m for m in plan["items"] if m["id"] == tid]
    require(len(matches) == 1, f"Unknown or duplicate ID: {tid}")
    require(size_ok(matches[0]["size"]), "Invalid manifest size")
    return plan, matches[0]


def composite_text(image, text, pack, font_path, font_index, layout):
    from PIL import ImageDraw, ImageFont
    require(font_path and Path(font_path).is_file(), "Wallpaper needs --font pointing to a licensed CJK font")
    # Font cmap is checked with Pillow's glyph masks; missing glyphs map to .notdef.
    probe = ImageFont.truetype(str(font_path), 48, index=font_index)
    missing = bytes(probe.getmask(chr(0x10FFFF)))
    for char in set(text) - {"\n", " ", "\t"}:
        require(bytes(probe.getmask(char)) != missing, f"Font does not support character: {char}")
    draw = ImageDraw.Draw(image)
    w, h = image.size
    area = pack.get("text_area", [.12, .25, .88, .75])
    left, top, right, bottom = [round(v * n) for v, n in zip(area, (w, h, w, h))]
    lines = text.split("\n")
    placements = None
    chosen = None
    for size in range(round(w * .14), max(15, round(w * .025)), -1):
        font = ImageFont.truetype(str(font_path), size, index=font_index)
        if layout == "vertical":
            step, col_step = round(size * 1.2), round(size * 1.65)
            width = (len(lines) - 1) * col_step + size
            height = max(len(s) for s in lines) * step
            if width > right-left or height > bottom-top:
                continue
            placements = []
            for i, line in enumerate(lines):
                x = (left+right)/2 + width/2 - size/2 - i*col_step
                y0 = (top+bottom)/2 - len(line)*step/2
                for j, char in enumerate(line):
                    b = draw.textbbox((0, 0), char, font=font)
                    placements.append((char, (round(x-(b[2]-b[0])/2-b[0]), round(y0+j*step-b[1]))))
        else:
            boxes = [draw.textbbox((0, 0), s, font=font) for s in lines]
            gap = round(size * .55)
            height = sum(b[3]-b[1] for b in boxes) + gap*(len(lines)-1)
            if max(b[2]-b[0] for b in boxes) > right-left or height > bottom-top:
                continue
            y = (top+bottom-height)/2
            placements = []
            for line, b in zip(lines, boxes):
                placements.append((line, (round((left+right-(b[2]-b[0]))/2-b[0]), round(y-b[1]))))
                y += b[3]-b[1]+gap
        actual = [draw.textbbox(xy, s, font=font) for s, xy in placements]
        if all(left <= b[0] <= b[2] <= right and top <= b[1] <= b[3] <= bottom for b in actual):
            chosen = (font, size, actual)
            break
    require(chosen is not None, "Copy does not fit; shorten copy or revise layout explicitly")
    font, size, boxes = chosen
    for s, xy in placements:
        draw.text(xy, s, font=font, fill=pack["text_color"])
    return {"copy": text, "layout": layout, "font_sha256": digest(font_path), "font_index": font_index,
            "font_size": size, "text_area_px": [left, top, right, bottom], "boxes": boxes}


def ingest(batch, tid, image_path, font=None, font_index=0, allow_crop=False, allow_upscale=False):
    from PIL import Image, ImageOps
    batch, source = Path(batch), Path(image_path)
    plan, item = get_item(batch, tid)
    final = batch / "finals" / (tid + ".png")
    record_path = batch / "records" / (tid + ".json")
    require(not final.exists() and not record_path.exists(), "Already imported; use a new revision batch")
    require(source.is_file(), "Source image missing")
    with Image.open(source) as opened:
        original_format = opened.format
        require(original_format in ("PNG", "JPEG", "WEBP"), "Only PNG, JPEG, WEBP sources supported")
        require(not getattr(opened, "is_animated", False), "Animated sources unsupported")
        raw = ImageOps.exif_transpose(opened).convert("RGB")
    sw, sh = raw.size
    tw, th = item["size"]
    retained_w = min(sw, sh*tw/th)
    retained_h = min(sh, sw*th/tw)
    crop = [1-retained_w/sw, 1-retained_h/sh]
    require(max(crop) <= .02 or allow_crop, "Aspect mismatch crops over 2%; recompose or explicitly --allow-crop")
    upscale = tw > retained_w+.001 or th > retained_h+.001
    require(not upscale or allow_upscale, "Upscaling requires --allow-upscale; interpolation adds no real detail")
    rendered = ImageOps.fit(raw, (tw, th), method=Image.Resampling.LANCZOS)
    typography = None
    if plan["style"]["text_mode"] == "overlay":
        typography = composite_text(rendered, item["task"]["copy"], plan["style"], font,
                                    font_index, item["task"].get("copy_layout", "center"))
    suffix = {"PNG": ".png", "JPEG": ".jpg", "WEBP": ".webp"}[original_format]
    original = batch / "originals" / (tid + suffix)
    require(not original.exists(), "Original already exists; use a new revision batch")
    original.parent.mkdir(parents=True, exist_ok=True)
    final.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, original)
    rendered.save(final, "PNG", optimize=True)
    record = {"id": tid, "plan_sha256": value_hash(plan), "input_sha256": digest(original),
              "final_sha256": digest(final), "original": original.relative_to(batch).as_posix(),
              "source_size": [sw, sh], "size": [tw, th], "crop_fractions": crop,
              "upscaled": upscale, "typography": typography}
    write(record_path, record)
    print(f"Imported {tid}: {tw}x{th}; visual review pending")


def review(batch, tid, checks_path):
    batch = Path(batch)
    plan, _ = get_item(batch, tid)
    target = batch / "reviews" / (tid + ".json")
    require(not target.exists(), "Review already exists; use a new revision batch")
    r = read(checks_path)
    require(isinstance(r.get("reviewer"), str) and r["reviewer"].strip(), "Reviewer required")
    require(isinstance(r.get("checks"), dict), "checks object required")
    for key in plan["style"]["review_checks"]:
        c = r["checks"].get(key, {})
        require(type(c.get("pass")) is bool and isinstance(c.get("evidence"), str)
                and c["evidence"].strip(), f"Missing boolean and visual evidence: {key}")
    final = batch / "finals" / (tid + ".png")
    require(final.is_file(), "Cannot review a missing final")
    r.update(id=tid, plan_sha256=value_hash(plan), final_sha256=digest(final))
    write(target, r)
    print(f"Recorded visual review: {tid}")


def report(batch):
    from PIL import Image, ImageDraw
    batch = Path(batch)
    plan = read(batch / "plan.json")
    validate_pack(plan["style"])
    rows, cards, thumbs = [], [], []
    for item in plan["items"]:
        tid = item["id"]
        require(isinstance(tid, str) and ID.fullmatch(tid), "Unsafe task ID")
        errors, pending = [], []
        final = batch / "finals" / (tid + ".png")
        record_path = batch / "records" / (tid + ".json")
        review_path = batch / "reviews" / (tid + ".json")
        uri = ""
        if not final.is_file() or not record_path.is_file():
            errors.append("missing image or import record")
        else:
            record = read(record_path)
            original_rel = Path(record["original"])
            require(not original_rel.is_absolute() and ".." not in original_rel.parts, "Unsafe original path")
            original = batch / original_rel
            if not original.is_file() or digest(original) != record["input_sha256"]:
                errors.append("original hash mismatch")
            if digest(final) != record["final_sha256"]:
                errors.append("final hash mismatch")
            if value_hash(plan) != record["plan_sha256"]:
                errors.append("plan changed since import")
            with Image.open(final) as image:
                image.load()
                if list(image.size) != item["size"]:
                    errors.append("wrong actual size")
                thumb = image.convert("RGB")
                thumb.thumbnail((224, 320))
                thumbs.append((tid, thumb.copy()))
            if plan["style"]["text_mode"] == "overlay":
                t = record.get("typography") or {}
                if t.get("copy") != item["task"]["copy"]:
                    errors.append("copy record mismatch")
                area = t.get("text_area_px", [0, 0, 0, 0])
                if not t.get("boxes") or not all(area[0] <= b[0] <= b[2] <= area[2] and
                                                area[1] <= b[1] <= b[3] <= area[3] for b in t["boxes"]):
                    errors.append("text outside layout")
            uri = "data:image/png;base64," + base64.b64encode(final.read_bytes()).decode()
            if not review_path.is_file():
                pending.append("visual review missing")
            else:
                r = read(review_path)
                if r.get("final_sha256") != digest(final) or r.get("plan_sha256") != value_hash(plan):
                    errors.append("stale visual review")
                for key in plan["style"]["review_checks"]:
                    c = r.get("checks", {}).get(key, {})
                    if c.get("pass") is not True or not isinstance(c.get("evidence"), str) or not c["evidence"].strip():
                        errors.append("visual check not passed: " + key)
        status = "failed" if errors else "pending" if pending else "passed"
        rows.append({"id": tid, "topic": item["task"]["topic"], "status": status,
                     "technical_errors": [e for e in errors if not e.startswith("visual")],
                     "issues": errors+pending})
        description = html.escape(item["task"]["topic"])
        cards.append(f'<article><h2>{html.escape(tid)} · {description}</h2><p>{status}</p>'
                     + (f'<img class="preview-image" src="{uri}" alt="{description}" tabindex="0" role="button" aria-label="查看大图：{description}">' if uri else '<p>尚未生成</p>')
                     + f'<pre>{html.escape(chr(10).join(errors+pending))}</pre></article>')
    passed = sum(r["status"] == "passed" for r in rows)
    result = {"tool_version": VERSION, "style_id": plan["style"]["id"], "style_version": plan["style"]["version"],
              "requested": len(rows), "passed": passed, "complete": passed == len(rows) and bool(rows), "items": rows}
    write(batch / "report.json", result)
    if thumbs:
        cols = min(len(thumbs), 4)
        sheet = Image.new("RGB", (cols*248, ((len(thumbs)+cols-1)//cols)*360), "#f4f1e9")
        draw = ImageDraw.Draw(sheet)
        for i, (tid, thumb) in enumerate(thumbs):
            x, y = (i % cols)*248, (i // cols)*360
            sheet.paste(thumb, (x+(248-thumb.width)//2, y+10))
            draw.text((x+12, y+334), tid, fill="#333333")
        sheet.save(batch / "contact-sheet.jpg", quality=90)
    title = html.escape(plan["style"]["name"])
    page = ('<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{title}</title><style>body{{margin:0;padding:24px;background:#f4f1e9;color:#253331;font-family:system-ui}}'
            'main{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:20px}article{background:white;padding:16px;border-radius:14px}'
            'img{width:100%;height:auto;max-height:70vh;object-fit:contain}.preview-image{cursor:zoom-in}h2{font-size:17px}pre{white-space:pre-wrap}'
            'dialog{border:0;padding:16px;border-radius:12px;max-width:94vw}dialog::backdrop{background:#162421d9}dialog img{width:auto;max-width:88vw;max-height:85vh;display:block}button{margin-bottom:12px}</style>'
            f'<h1>{title}</h1><p>{passed}/{len(rows)} 已通过 · 图片内嵌，可离线转发 · 点击图片查看原尺寸</p><main>'
            + ''.join(cards) + '</main><dialog id="viewer"><button id="close" type="button">关闭 ×</button><img id="large" alt="大图"></dialog>'
            '<script>(()=>{const d=document.getElementById("viewer"),l=document.getElementById("large");'
            'document.querySelectorAll(".preview-image").forEach(i=>{const show=()=>{l.src=i.src;l.alt=i.alt;d.showModal()};'
            'i.addEventListener("click",show);i.addEventListener("keydown",e=>{if(e.key==="Enter"||e.key===" "){e.preventDefault();show()}})});'
            'document.getElementById("close").onclick=()=>d.close();d.addEventListener("click",e=>{if(e.target===d)d.close()})})();</script></html>')
    (batch / "preview.html").write_text(page, encoding="utf-8")
    print(f"{passed}/{len(rows)} passed; complete={result['complete']}")
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", action="version", version=VERSION)
    subs = parser.add_subparsers(dest="command", required=True)
    p = subs.add_parser("compile", help="Compile a plan without generating images")
    p.add_argument("--pack", required=True)
    p.add_argument("--tasks", required=True)
    p.add_argument("--out", required=True)
    p = subs.add_parser("ingest", help="Import one image; visual review remains pending")
    p.add_argument("--batch", required=True)
    p.add_argument("--id", required=True)
    p.add_argument("--image", required=True)
    p.add_argument("--font")
    p.add_argument("--font-index", type=int, default=0)
    p.add_argument("--allow-crop", action="store_true")
    p.add_argument("--allow-upscale", action="store_true")
    p = subs.add_parser("review", help="Record actual visual inspection bound to image hash")
    p.add_argument("--batch", required=True)
    p.add_argument("--id", required=True)
    p.add_argument("--checks", required=True)
    p = subs.add_parser("report", help="Verify files and export an offline embedded gallery")
    p.add_argument("--batch", required=True)
    p.add_argument("--require-complete", action="store_true")
    a = parser.parse_args()
    try:
        if a.command == "compile":
            compile_batch(a.pack, a.tasks, a.out)
        elif a.command == "ingest":
            ingest(a.batch, a.id, a.image, a.font, a.font_index, a.allow_crop, a.allow_upscale)
        elif a.command == "review":
            review(a.batch, a.id, a.checks)
        else:
            result = report(a.batch)
            if a.require_complete and not result["complete"]:
                return 1
    except (ValueError, OSError, KeyError, TypeError, json.JSONDecodeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
