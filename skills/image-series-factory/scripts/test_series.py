"""Meaningful offline regression tests; run: python3 -m unittest discover -s scripts -v."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

from PIL import Image

spec = importlib.util.spec_from_file_location("series", Path(__file__).with_name("series.py"))
series = importlib.util.module_from_spec(spec)
spec.loader.exec_module(series)
PACK = Path(__file__).resolve().parents[1] / "assets/style-packs/editorial-pop.json"


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.pack = series.read(PACK)
        self.pack["default_size"] = [72, 128]
        self.pack_path = self.root / "pack.json"
        series.write(self.pack_path, self.pack)
        self.tasks = self.root / "tasks.jsonl"
        self.batch = self.root / "batch"
        self.source = self.root / "source.png"
        Image.new("RGB", (144, 256), "#f2d0a0").save(self.source)

    def compile(self, tasks=None):
        tasks = tasks or [{"id": "001", "topic": "<script>test</script>"}]
        self.tasks.write_text("\n".join(json.dumps(t) for t in tasks), encoding="utf-8-sig")
        series.compile_batch(self.pack_path, self.tasks, self.batch)

    def good_review(self):
        path = self.root / "review.json"
        series.write(path, {"reviewer": "unit-test-fixture", "checks": {
            k: {"pass": True, "evidence": "Synthetic fixture; tests state handling only"}
            for k in self.pack["review_checks"]}})
        return path

    def test_compile_does_not_create_images_or_claim_success(self):
        self.compile()
        r = series.report(self.batch)
        self.assertFalse(r["complete"])
        self.assertEqual(r["passed"], 0)
        self.assertFalse((self.batch / "finals").exists())

    def test_duplicate_and_path_traversal_rejected_before_writing(self):
        for tasks in ([{"id":"../bad", "topic":"x"}],
                      [{"id":"001", "topic":"x"}, {"id":"001", "topic":"y"}]):
            with self.assertRaises(ValueError):
                self.compile(tasks)
            self.assertFalse(self.batch.exists())

    def test_import_requires_review_and_embedded_preview_is_escaped(self):
        self.compile()
        series.ingest(self.batch, "001", self.source)
        r = series.report(self.batch)
        self.assertEqual(r["items"][0]["status"], "pending")
        series.review(self.batch, "001", self.good_review())
        self.assertTrue(series.report(self.batch)["complete"])
        page = (self.batch / "preview.html").read_text()
        self.assertIn("data:image/png;base64,", page)
        self.assertNotIn("<script>test</script>", page)
        self.assertNotIn(str(self.root), page)

    def test_changed_final_and_original_invalidate_completion(self):
        self.compile()
        series.ingest(self.batch, "001", self.source)
        series.review(self.batch, "001", self.good_review())
        Image.new("RGB", (72, 128), "blue").save(self.batch / "finals/001.png")
        (self.batch / "originals/001.png").write_bytes(b"tampered")
        r = series.report(self.batch)
        self.assertFalse(r["complete"])
        self.assertIn("final hash mismatch", r["items"][0]["issues"])
        self.assertIn("original hash mismatch", r["items"][0]["issues"])
        self.assertIn("stale visual review", r["items"][0]["issues"])

    def test_changed_plan_invalidates_review(self):
        self.compile()
        series.ingest(self.batch, "001", self.source)
        series.review(self.batch, "001", self.good_review())
        p = series.read(self.batch / "plan.json")
        p["items"][0]["task"]["topic"] = "new topic"
        series.write(self.batch / "plan.json", p)
        self.assertFalse(series.report(self.batch)["complete"])

    def test_crop_upscale_and_overwrite_guards(self):
        self.compile()
        Image.new("RGB", (100, 100)).save(self.source)
        with self.assertRaises(ValueError):
            series.ingest(self.batch, "001", self.source)
        self.assertFalse((self.batch / "finals/001.png").exists())
        with self.assertRaises(ValueError):
            series.ingest(self.batch, "001", self.source, allow_crop=True)
        series.ingest(self.batch, "001", self.source, allow_crop=True, allow_upscale=True)
        with self.assertRaises(ValueError):
            series.ingest(self.batch, "001", self.source, allow_crop=True, allow_upscale=True)
        with self.assertRaises(ValueError):
            self.compile()

    def test_missing_font_leaves_no_partial_wallpaper(self):
        self.pack.update(category="wallpaper", text_mode="overlay", text_color="#693D2D",
                         review_checks=["style", "semantic", "clean", "text"])
        series.write(self.pack_path, self.pack)
        self.compile([{"id":"001", "topic":"壁纸", "copy":"原文"}])
        with self.assertRaises(ValueError):
            series.ingest(self.batch, "001", self.source)
        self.assertFalse((self.batch / "originals/001.png").exists())
        self.assertFalse((self.batch / "finals/001.png").exists())

    def test_review_requires_actual_boolean_and_evidence(self):
        self.compile()
        series.ingest(self.batch, "001", self.source)
        p = self.good_review()
        r = series.read(p)
        r["checks"]["clean"]["pass"] = "true"
        series.write(p, r)
        with self.assertRaises(ValueError):
            series.review(self.batch, "001", p)
        self.assertFalse((self.batch / "reviews/001.json").exists())


if __name__ == "__main__":
    unittest.main()
