import csv
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

from build_combined_dictionary import build_dictionary


class CombinedDictionaryTest(unittest.TestCase):
    def test_combines_dictionary_layers_for_one_word(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            ecdict = root / "ecdict.csv"
            with ecdict.open("w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(
                    f,
                    fieldnames=[
                        "word",
                        "phonetic",
                        "definition",
                        "translation",
                        "pos",
                        "collins",
                        "oxford",
                        "tag",
                        "bnc",
                        "frq",
                        "exchange",
                        "detail",
                        "audio",
                    ],
                )
                writer.writeheader()
                writer.writerow(
                    {
                        "word": "resign",
                        "phonetic": "ri'zain",
                        "definition": "v. accept as inevitable",
                        "translation": "vt. 辞职, 放弃, 使顺从",
                        "pos": "v",
                        "collins": "3",
                        "oxford": "",
                        "tag": "cet4 cet6",
                        "bnc": "2549",
                        "frq": "3390",
                        "exchange": "p:resigned/d:resigned/i:resigning/3:resigns",
                        "detail": "",
                        "audio": "",
                    }
                )

            roots = root / "wordroot.txt"
            roots.write_text(
                json.dumps(
                    {
                        "sign": {
                            "root": "sign",
                            "meaning": "mark, sign",
                            "class": "root",
                            "words": ["resign", "design"],
                        }
                    }
                ),
                encoding="utf-8",
            )

            resemble = root / "resemble.txt"
            resemble.write_text(
                "% resign, submit, surrender\n"
                "- resign: 指被迫或无奈地接受，也可指辞职。\n"
                "- submit: 强调服从或提交。\n",
                encoding="utf-8",
            )

            lemma = root / "lemma.en.txt"
            lemma.write_text("resigned resign\nresigning resign\n", encoding="utf-8")

            wn = root / "wordnet"
            (wn / "dict").mkdir(parents=True)
            for name in ["index.noun", "index.adj", "index.adv", "data.noun", "data.adj", "data.adv"]:
                (wn / "dict" / name).write_text("", encoding="utf-8")
            (wn / "dict" / "index.verb").write_text(
                "resign v 1 1 @ 1 1 00732394  \n", encoding="utf-8"
            )
            (wn / "dict" / "data.verb").write_text(
                '00732394 31 v 03 resign 0 reconcile 0 submit 0 000 | accept as inevitable; "He resigned himself to his fate"  \n',
                encoding="utf-8",
            )

            learning = root / "learning.sqlite3"
            with sqlite3.connect(learning) as c:
                c.executescript(
                    """
                    CREATE TABLE items(id TEXT PRIMARY KEY,kind TEXT,title TEXT,meaning TEXT,body TEXT,source TEXT,created TEXT);
                    CREATE TABLE collections(id TEXT PRIMARY KEY,title TEXT,metadata TEXT);
                    CREATE TABLE collection_items(collection_id TEXT,item_id TEXT,position INTEGER,body TEXT);
                    INSERT INTO items VALUES('w1','word','resign','辞职；接受不可避免','body','source','now');
                    INSERT INTO collections VALUES('cet4','四级','{}');
                    INSERT INTO collection_items VALUES('cet4','w1',1,'## 资料例句（未逐句审校）\n\n> A hospital administrator resigned.\n\n一位医院主管辞职了。\n\n## 关联搭配（不等于必考词组）\n\n- resign from：辞职');
                    INSERT INTO items VALUES('p1','phrase','resign from','辞职','phrase body','source','now');
                    INSERT INTO collection_items VALUES('cet4','p1',2,'## 资料含义\n\n辞职\n\n来自词目：resign');
                    """
                )

            out = root / "combined.sqlite3"
            report = build_dictionary(
                output=out,
                ecdict_csv=ecdict,
                wordroot=roots,
                resemble=resemble,
                lemma=lemma,
                wordnet_dir=wn / "dict",
                learning_db=learning,
            )

            self.assertEqual(report["entries"], 1)
            with sqlite3.connect(out) as c:
                c.row_factory = sqlite3.Row
                row = c.execute("SELECT * FROM entries WHERE word='resign'").fetchone()
                self.assertIn("辞职", row["translation"])
                self.assertIn("accept as inevitable", row["definition"])
                self.assertIn("resigning", row["exchange"])
                wn_row = c.execute("SELECT * FROM wordnet_senses WHERE word='resign'").fetchone()
                self.assertIn("He resigned himself to his fate", wn_row["examples"])
                syns = [r["related_word"] for r in c.execute("SELECT related_word FROM relations WHERE word='resign' AND relation='synonym'")]
                self.assertIn("submit", syns)
                root_row = c.execute("SELECT * FROM roots WHERE word='resign'").fetchone()
                self.assertEqual(root_row["root"], "sign")
                phrase = c.execute("SELECT * FROM phrases WHERE headword='resign'").fetchone()
                self.assertEqual(phrase["phrase"], "resign from")
                example = c.execute("SELECT * FROM examples WHERE headword='resign'").fetchone()
                self.assertIn("administrator resigned", example["english"])
                note = c.execute("SELECT * FROM resemble_notes WHERE word='resign'").fetchone()
                self.assertIn("无奈地接受", note["note"])


if __name__ == "__main__":
    unittest.main()
